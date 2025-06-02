from flask import Flask, request, jsonify, Response
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import json
import os
from datetime import datetime
from werkzeug.utils import secure_filename
from diem_converter import convert_excel_to_json
from create_simplified_diem import create_simplified_diem_json

from LLM.utils import get_khaosat_data_from_file, get_diem_data_from_file
from LLM.prompts import generate_prompt1_payload, generate_prompt2_payload, generate_prompt3_payload
from LLM.enhanced_prompts import EnhancedEducationConsultant
from LLM.ollama_session_manager import OllamaSessionManager, session_manager
from LLM.quick_response_templates import QuickResponseTemplates, quick_templates
from LLM.ollama_interactions import call_ollama_stream_logic, ollama_chat_streaming

app = Flask(__name__)
CORS(app)

# --- Configuration ---
OLLAMA_API_URL = "http://192.168.2.114:11434/api/chat" 
OLLAMA_MODEL = "gemma3:latest"
PATH_KHAOSAT = '../../Database/khaosat.json' 
PATH_DIEM = '../../Database/diem.json'
PATH_DIEM_SIMPLIFIED = '../../Database/diem_simplified.json' 

llm_analysis_results = {
    "stage1_khaosat": "",
    "stage2_diem": "",
    "stage3_tonghop": ""
}
llm_conversation_history_stage3 = []

# Initialize enhanced systems
enhanced_consultant = EnhancedEducationConsultant()
response_mode = "enhanced"  # Options: "enhanced", "quick", "template", "basic"

# Ensure the Database directory exists (ngang hàng với Backend)
os.makedirs('../../Database', exist_ok=True)

def calculate_percentage(scores, total_questions):
    """
    Tính toán phần trăm điểm cho một phần khảo sát
    Args:
        scores: Danh sách điểm số
        total_questions: Tổng số câu hỏi
    Returns:
        float: Phần trăm điểm đã làm tròn đến 2 chữ số thập phân
    """
    total_score = sum(scores)
    max_possible_score = total_questions * 5
    percentage = (total_score / max_possible_score) * 100
    return round(percentage, 2)

@app.route('/api/submit-survey', methods=['POST'])
def submit_survey():
    """
    API endpoint xử lý việc gửi khảo sát
    - Thu thập thông tin cá nhân
    - Xử lý điểm số từng phần
    - Lưu kết quả vào file JSON
    """
    try:
        data = request.json
        
        # Extract personal information
        personal_info = {
            "ma_so_sinh_vien": data.get("ma_so_sinh_vien"),
            "gioi_tinh": data.get("gioi_tinh"),
            "khoa": data.get("khoa"),
            "nam_hoc": data.get("nam_hoc"),
            "ho_ten": data.get("ho_va_ten")
        }
        
        # Process each section
        results = {
            "thong_tin_ca_nhan": personal_info,
            "thoi_gian_nop": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Define sections and their question counts
        sections = {
            "I": {"name": "Thai_do_hoc_tap", "count": 5},
            "II": {"name": "Su_dung_mang_xa_hoi", "count": 5},
            "III": {"name": "Gia_dinh_Xa_hoi", "count": 5},
            "IV": {"name": "Ban_be", "count": 5},
            "V": {"name": "Moi_truong_hoc_tap", "count": 5},
            "VI": {"name": "Quan_ly_thoi_gian", "count": 4},
            "VII": {"name": "Tu_hoc", "count": 4},
            "VIII": {"name": "Hop_tac_nhom", "count": 4},
            "IX": {"name": "Tu_duy_phan_bien", "count": 4},
            "X": {"name": "Tiep_thu_xu_ly_kien_thuc", "count": 4}
        }
        
        # Process each section's scores
        for section_key, section_info in sections.items():
            section_scores = []
            for i in range(1, section_info["count"] + 1):
                score = data.get(f"{section_key}_{i}")
                if score is not None:
                    # Attempt to convert score to int, handle potential errors
                    try:
                         section_scores.append(int(score))
                    except ValueError:
                         print(f"Warning: Could not convert score '{score}' to int for {section_key}_{i}")
                         # Optionally handle the error differently, e.g., skip or use a default value

            if section_scores: # Ensure list is not empty
                 percentage = calculate_percentage(section_scores, section_info["count"])
                 results[section_info["name"]] = {
                     "tong_so_cau_hoi": section_info["count"],
                     "phan_tram_diem": percentage
                 }
        
        # Save to JSON file - overwrite instead of append
        file_path = PATH_KHAOSAT
        
        # Write only the new results
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump([results], f, ensure_ascii=False, indent=4)
        
        return jsonify({"message": "Survey submitted successfully", "data": results}), 200
        
    except Exception as e:
        print(f"Error in submit_survey: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/upload-file', methods=['POST'])
def upload_file():
    """
    API endpoint xử lý việc upload file bảng điểm
    - Kiểm tra file hợp lệ
    - Lưu file Excel
    - Chuyển đổi sang JSON
    """
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and file.filename.endswith('.xlsx'):
        try:
            # Save the file
            filename = secure_filename('diem.xlsx')
            file_path = os.path.join('..', '..', 'Database', filename)
            file.save(file_path)
            
            # Process the Excel file to JSON using the new converter
            json_path = PATH_DIEM
            success, message = convert_excel_to_json(file_path, json_path)
            
            if success:
                # Tự động tạo file đơn giản hóa sau khi xử lý thành công
                simplified_success, simplified_message = create_simplified_diem_json(PATH_DIEM, PATH_DIEM_SIMPLIFIED)
                
                if simplified_success:
                    return jsonify({
                        'message': 'File uploaded and processed successfully',
                        'simplified_file_created': True,
                        'simplified_message': simplified_message
                    }), 200
                else:
                    # Vẫn trả về thành công nhưng cảnh báo về file đơn giản hóa
                    return jsonify({
                        'message': 'File uploaded and processed successfully',
                        'simplified_file_created': False,
                        'warning': f'Không thể tạo file đơn giản hóa: {simplified_message}'
                    }), 200
            else:
                return jsonify({'error': message}), 500
                
        except Exception as e:
            print(f"Error in upload_file: {e}")
            return jsonify({'error': str(e)}), 500
    
    return jsonify({'error': 'Invalid file format'}), 400

@app.route('/api/get-data', methods=['GET'])
def get_data(): # Diem data
    """
    API endpoint lấy dữ liệu điểm số
    - Đọc file JSON điểm
    - Trả về dữ liệu cho client
    """
    try:
        json_path = PATH_DIEM
        if not os.path.exists(json_path):
            return jsonify({'error': 'No data file found'}), 404
            
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return jsonify(data)
    except Exception as e:
        print(f"Error in get_data: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/get-simplified-data', methods=['GET'])
def get_simplified_data():
    """
    API endpoint lấy dữ liệu điểm số đơn giản hóa
    - Đọc file JSON điểm đơn giản hóa
    - Trả về dữ liệu cho trực quan hóa
    """
    try:
        json_path = PATH_DIEM_SIMPLIFIED
        if not os.path.exists(json_path):
            # Nếu file đơn giản hóa chưa tồn tại, tạo từ file gốc
            if os.path.exists(PATH_DIEM):
                success, message = create_simplified_diem_json(PATH_DIEM, PATH_DIEM_SIMPLIFIED)
                if not success:
                    return jsonify({'error': f'Không thể tạo file đơn giản hóa: {message}'}), 500
            else:
                return jsonify({'error': 'No data file found'}), 404
            
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return jsonify(data)
    except Exception as e:
        print(f"Error in get_simplified_data: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/get-khaosat-summary', methods=['GET'])
def get_khaosat_summary():
    """
    API endpoint để lấy dữ liệu tóm tắt khảo sát.
    Hiện tại, trả về bản ghi khảo sát đầu tiên (hoặc duy nhất).
    """
    try:
        if not os.path.exists(PATH_KHAOSAT):
            return jsonify({'error': 'Không tìm thấy file dữ liệu khảo sát.'}), 404
            
        with open(PATH_KHAOSAT, 'r', encoding='utf-8') as f:
            khaosat_data_list = json.load(f)
        
        if not khaosat_data_list:
            return jsonify({'error': 'File khảo sát rỗng.'}), 404
            
        # Trả về bản ghi đầu tiên (giả định là mới nhất hoặc duy nhất)
        return jsonify(khaosat_data_list[0]) 
    except Exception as e:
        print(f"Error in get_khaosat_summary: {e}")
        return jsonify({'error': str(e)}), 500

# --- New LLM Endpoints ---

@app.route('/api/start-llm-analysis', methods=['GET', 'POST'])
def start_llm_analysis_route():
    """
    Enhanced API endpoint bắt đầu phân tích LLM với support cho enhanced features
    - Hỗ trợ multiple response modes: enhanced, quick, template, basic
    - Tích hợp RAG, Cache và Template systems
    - Stream kết quả về client với metadata
    """
    global llm_analysis_results, llm_conversation_history_stage3, response_mode

    # Get parameters
    use_enhanced = request.args.get('enhanced', 'true').lower() == 'true'
    mode = request.args.get('mode', response_mode)  # Use global mode as default
    use_cache = request.args.get('cache', 'true').lower() == 'true'
    use_rag = request.args.get('rag', 'true').lower() == 'true'
    
    # Reset results for new analysis
    llm_analysis_results = {
        "stage1_khaosat": "",
        "stage2_diem": "",
        "stage3_tonghop": ""
    }
    llm_conversation_history_stage3 = []

    khaosat_data = get_khaosat_data_from_file(PATH_KHAOSAT)
    if not khaosat_data:
        return Response(f"data: {json.dumps({'stage': 'setup', 'error': 'Không thể đọc dữ liệu khảo sát.'})}\n\n", mimetype='text/event-stream')

    diem_data = get_diem_data_from_file(PATH_DIEM_SIMPLIFIED)
    if not diem_data:
        return Response(f"data: {json.dumps({'stage': 'setup', 'error': 'Không thể đọc dữ liệu điểm.'})}\n\n", mimetype='text/event-stream')

    def enhanced_combined_stream():
        """
        Enhanced streaming function với multiple response modes
        """
        global llm_conversation_history_stage3
        
        try:
            # Emit analysis start with mode info
            print(f"🔄 Starting analysis - mode: {mode}, enhanced: {use_enhanced}")
            yield f"data: {json.dumps({'stage': 'setup', 'mode': mode, 'enhanced': use_enhanced})}\n\n"
            
            # Quick mode - try template first
            print(f"🔄 Checking mode: {mode}")
            if mode in ['quick', 'template']:
                print("🔄 Processing template/quick mode...")
                pattern_info = enhanced_consultant.analyze_student_pattern(khaosat_data, diem_data)
                print(f"🔄 Pattern analysis complete: {pattern_info}")
                
                analysis_data = {
                    **pattern_info,
                    "major": khaosat_data.get("thong_tin_ca_nhan", {}).get("khoa", ""),
                    "weak_skills_detail": {},
                    "best_subjects": [],
                    "top_skills": []
                }
                
                # Extract skills detail for template matching
                skills_fields = [
                    "Thai_do_hoc_tap", "Su_dung_mang_xa_hoi", "Gia_dinh_Xa_hoi", "Ban_be",
                    "Moi_truong_hoc_tap", "Quan_ly_thoi_gian", "Tu_hoc", "Hop_tac_nhom",
                    "Tu_duy_phan_bien", "Tiep_thu_xu_ly_kien_thuc"
                ]
                
                for field in skills_fields:
                    skill_data = khaosat_data.get(field, {})
                    if isinstance(skill_data, dict) and "phan_tram_diem" in skill_data:
                        score = skill_data["phan_tram_diem"]
                        if score < 70:
                            analysis_data["weak_skills_detail"][field] = score
                
                template_response = quick_templates.generate_quick_response(analysis_data)
                
                if template_response and mode == 'template':
                    # Return template response only
                    yield f"data: {json.dumps({'stage': 'template_complete', 'template_name': template_response['template_name']})}\n\n"
                    
                    # Split response into chunks for streaming effect
                    response_chunks = template_response['response'].split('\n\n')
                    for i, chunk in enumerate(response_chunks):
                        if chunk.strip():
                            chunk_content = chunk + '\n\n'
                            yield f"data: {json.dumps({'stage': 'stage1_khaosat', 'content': chunk_content, 'chunk': i+1, 'total_chunks': len(response_chunks)})}\n\n"
                    
                    llm_analysis_results["stage1_khaosat"] = template_response['response']
                    llm_analysis_results["stage2_diem"] = "Template response - no separate stage 2"
                    llm_analysis_results["stage3_tonghop"] = "Template response - comprehensive analysis provided"
                    
                    yield f"data: {json.dumps({'status': 'template_complete', 'metadata': {'confidence': template_response['confidence'], 'source': 'template'}})}\n\n"
                    return
                
                elif template_response and mode == 'quick':
                    # Use template as stage 1, then proceed normally
                    yield f"data: {json.dumps({'stage': 'quick_stage1', 'template_name': template_response['template_name']})}\n\n"
                    
                    response_chunks = template_response['response'].split('\n\n')
                    for chunk in response_chunks:
                        if chunk.strip():
                            content_data = chunk + '\n\n'
                            yield f"data: {json.dumps({'stage': 'stage1_khaosat', 'content': content_data})}\n\n"
                    
                    llm_analysis_results["stage1_khaosat"] = template_response['response']
                    
                    # Continue with enhanced stage 2 and 3
                    # Set enhanced mode for remaining stages
                    pass  # Enhanced processing will continue below

            # Standard/Enhanced processing
            # Determine enhanced mode based on mode parameter
            use_enhanced_mode = use_enhanced and mode not in ['basic']
            
            if not use_enhanced_mode or mode == 'basic':
                # Use original prompts
                payload1 = generate_prompt1_payload(khaosat_data, OLLAMA_MODEL)
                payload2 = generate_prompt2_payload(diem_data, khaosat_data, OLLAMA_MODEL)
                
                # Execute basic analysis
                yield from call_ollama_stream_logic(OLLAMA_API_URL, payload1, "stage1_khaosat", llm_analysis_results, llm_conversation_history_stage3)
                
                if llm_analysis_results.get("stage1_khaosat", "").startswith("<p style='color:red;'>"):
                    yield f"data: {json.dumps({'status': 'error_stage1'})}\n\n"
                    return
                
                yield from call_ollama_stream_logic(OLLAMA_API_URL, payload2, "stage2_diem", llm_analysis_results, llm_conversation_history_stage3)
                
                if llm_analysis_results.get("stage2_diem", "").startswith("<p style='color:red;'>"):
                    yield f"data: {json.dumps({'status': 'error_stage2'})}\n\n"
                    return
                
                # Stage 3 basic
                payload3 = generate_prompt3_payload(
                    llm_analysis_results.get("stage1_khaosat", ""),
                    llm_analysis_results.get("stage2_diem", ""), 
                    OLLAMA_MODEL
                )
                llm_conversation_history_stage3.clear()
                yield from call_ollama_stream_logic(OLLAMA_API_URL, payload3, "stage3_tonghop", llm_analysis_results, llm_conversation_history_stage3)
                
            else:
                # Use enhanced prompts with RAG and Cache
                if not llm_analysis_results.get("stage1_khaosat"):  # Not already filled by template
                    stage1_result = enhanced_consultant.enhanced_stage1_consultation(
                        khaosat_data, OLLAMA_MODEL, use_cache, use_rag
                    )
                    
                    if 'response' in stage1_result:
                        # Cached response
                        yield f"data: {json.dumps({'stage': 'cache_hit_stage1', 'confidence': stage1_result['metadata']['confidence']})}\n\n"
                        
                        response_chunks = stage1_result['response'].split('\n\n')
                        for chunk in response_chunks:
                            if chunk.strip():
                                content_data = chunk + '\n\n'
                                yield f"data: {json.dumps({'stage': 'stage1_khaosat', 'content': content_data})}\n\n"
                        
                        llm_analysis_results["stage1_khaosat"] = stage1_result['response']
                    else:
                        # Need LLM call
                        payload1 = stage1_result['payload']
                        yield from call_ollama_stream_logic(OLLAMA_API_URL, payload1, "stage1_khaosat", llm_analysis_results, llm_conversation_history_stage3)
                        
                        # Cache successful result if configured
                        if stage1_result.get('cache_enabled') and not llm_analysis_results.get("stage1_khaosat", "").startswith("<p style='color:red;'>"):
                            enhanced_consultant.cache_system.cache_response(
                                stage1_result['signature'], 'stage1', 
                                llm_analysis_results["stage1_khaosat"], 80
                            )

                if llm_analysis_results.get("stage1_khaosat", "").startswith("<p style='color:red;'>"):
                    yield f"data: {json.dumps({'status': 'error_stage1'})}\n\n"
                    return

                # Stage 2 Enhanced
                stage2_result = enhanced_consultant.enhanced_stage2_consultation(
                    khaosat_data, diem_data, OLLAMA_MODEL, use_cache, use_rag
                )
                
                if 'response' in stage2_result:
                    # Cached response
                    yield f"data: {json.dumps({'stage': 'cache_hit_stage2', 'confidence': stage2_result['metadata']['confidence']})}\n\n"
                    
                    response_chunks = stage2_result['response'].split('\n\n')
                    for chunk in response_chunks:
                        if chunk.strip():
                            content_data = chunk + '\n\n'
                            yield f"data: {json.dumps({'stage': 'stage2_diem', 'content': content_data})}\n\n"
                    
                    llm_analysis_results["stage2_diem"] = stage2_result['response']
                else:
                    # Need LLM call
                    payload2 = stage2_result['payload']
                    yield from call_ollama_stream_logic(OLLAMA_API_URL, payload2, "stage2_diem", llm_analysis_results, llm_conversation_history_stage3)
                    
                    # Cache successful result
                    if stage2_result.get('cache_enabled') and not llm_analysis_results.get("stage2_diem", "").startswith("<p style='color:red;'>"):
                        enhanced_consultant.cache_system.cache_response(
                            stage2_result['signature'], 'stage2', 
                            llm_analysis_results["stage2_diem"], 80
                        )

                if llm_analysis_results.get("stage2_diem", "").startswith("<p style='color:red;'>"):
                    yield f"data: {json.dumps({'status': 'error_stage2'})}\n\n"
                    return

                # Stage 3 Enhanced
                stage1_text = llm_analysis_results.get("stage1_khaosat", "")
                stage2_text = llm_analysis_results.get("stage2_diem", "")
                
                stage3_result = enhanced_consultant.enhanced_stage3_consultation(
                    khaosat_data, diem_data, stage1_text, stage2_text, 
                    OLLAMA_MODEL, use_cache, use_rag
                )
                
                if 'response' in stage3_result:
                    # Cached response
                    yield f"data: {json.dumps({'stage': 'cache_hit_stage3', 'confidence': stage3_result['metadata']['confidence']})}\n\n"
                    
                    response_chunks = stage3_result['response'].split('\n\n')
                    for chunk in response_chunks:
                        if chunk.strip():
                            content_data = chunk + '\n\n'
                            yield f"data: {json.dumps({'stage': 'stage3_tonghop', 'content': content_data})}\n\n"
                    
                    llm_analysis_results["stage3_tonghop"] = stage3_result['response']
                else:
                    # Need LLM call
                    payload3 = stage3_result['payload']
                    llm_conversation_history_stage3.clear()
                    yield from call_ollama_stream_logic(OLLAMA_API_URL, payload3, "stage3_tonghop", llm_analysis_results, llm_conversation_history_stage3)
                    
                    # Cache successful result
                    if stage3_result.get('cache_enabled') and not llm_analysis_results.get("stage3_tonghop", "").startswith("<p style='color:red;'>"):
                        enhanced_consultant.cache_system.cache_response(
                            stage3_result['signature'], 'stage3', 
                            llm_analysis_results["stage3_tonghop"], 80
                        )
            
            # Final success message with performance stats
            stats = enhanced_consultant.get_performance_stats()
            yield f"data: {json.dumps({'status': 'all_done', 'performance_stats': stats})}\n\n"
            
        except Exception as e:
            print(f"Error in enhanced_combined_stream: {e}")
            yield f"data: {json.dumps({'status': 'error', 'message': str(e)})}\n\n"

    return Response(enhanced_combined_stream(), mimetype='text/event-stream')

@app.route('/api/llm-chat', methods=['POST'])
def llm_chat_route():
    """
    API endpoint xử lý chat với LLM
    - Nhận tin nhắn từ người dùng
    - Stream phản hồi từ LLM
    """
    global llm_conversation_history_stage3
    user_message_content = request.json.get('message')

    if not user_message_content:
        return jsonify({"error": "No message provided"}), 400
    
    if not llm_conversation_history_stage3:
         return jsonify({"error": "Phân tích ban đầu chưa được thực hiện hoặc đã xảy ra lỗi. Vui lòng chạy lại phân tích."}), 400

    # Reuse the streaming function from ollama_interactions
    return Response(ollama_chat_streaming(OLLAMA_API_URL, OLLAMA_MODEL, llm_conversation_history_stage3, user_message_content), mimetype='text/event-stream')

# --- End LLM Endpoints ---

# --- Enhanced LLM Endpoints với RAG, Cache và Template Support ---

@app.route('/api/enhanced-analysis', methods=['POST'])
def enhanced_analysis():
    """
    Enhanced API endpoint với RAG, Cache và Template support
    Body parameters:
    - response_mode: "enhanced", "quick", "template", "basic"
    - use_cache: boolean
    - use_rag: boolean
    - force_template: boolean
    - stage: "stage1", "stage2", "stage3"
    """
    try:
        data = request.get_json()
        mode = data.get('response_mode', 'enhanced')
        use_cache = data.get('use_cache', True)
        use_rag = data.get('use_rag', True)
        force_template = data.get('force_template', False)
        stage = data.get('stage', 'stage1')
        
        # Get student data
        khaosat_data = get_khaosat_data_from_file(PATH_KHAOSAT)
        if not khaosat_data:
            return jsonify({'error': 'Không thể đọc dữ liệu khảo sát.'}), 400
        
        diem_data = get_diem_data_from_file(PATH_DIEM_SIMPLIFIED) if stage in ['stage2', 'stage3'] else None
        
        response = None
        metadata = {}
        
        # Quick template response mode
        if mode == "quick" or force_template:
            # Analyze student pattern for template matching
            pattern_info = enhanced_consultant.analyze_student_pattern(khaosat_data, diem_data)
            analysis_data = {
                **pattern_info,
                "major": khaosat_data.get("thong_tin_ca_nhan", {}).get("khoa", ""),
                "weak_skills_detail": {},
                "grade_distribution": {}
            }
            
            # Extract detailed weak skills
            skills_fields = [
                "Thai_do_hoc_tap", "Su_dung_mang_xa_hoi", "Gia_dinh_Xa_hoi", "Ban_be",
                "Moi_truong_hoc_tap", "Quan_ly_thoi_gian", "Tu_hoc", "Hop_tac_nhom",
                "Tu_duy_phan_bien", "Tiep_thu_xu_ly_kien_thuc"
            ]
            
            for field in skills_fields:
                skill_data = khaosat_data.get(field, {})
                if isinstance(skill_data, dict) and "phan_tram_diem" in skill_data:
                    score = skill_data["phan_tram_diem"]
                    if score < 70:
                        analysis_data["weak_skills_detail"][field] = score
            
            template_response = quick_templates.generate_quick_response(analysis_data)
            
            if template_response:
                return jsonify({
                    'success': True,
                    'response': template_response['response'],
                    'metadata': {
                        'source': 'quick_template',
                        'template_name': template_response['template_name'],
                        'confidence': template_response['confidence'],
                        'response_time': 0.1  # Template responses are instant
                    }
                })
        
        # Enhanced consultation modes
        if stage == "stage1":
            result = enhanced_consultant.enhanced_stage1_consultation(
                khaosat_data, OLLAMA_MODEL, use_cache, use_rag, force_template
            )
        elif stage == "stage2":
            result = enhanced_consultant.enhanced_stage2_consultation(
                khaosat_data, diem_data, OLLAMA_MODEL, use_cache, use_rag
            )
        elif stage == "stage3":
            stage1_result = llm_analysis_results.get("stage1_khaosat", "")
            stage2_result = llm_analysis_results.get("stage2_diem", "")
            result = enhanced_consultant.enhanced_stage3_consultation(
                khaosat_data, diem_data, stage1_result, stage2_result, 
                OLLAMA_MODEL, use_cache, use_rag
            )
        
        # Return result based on whether it's cached or needs LLM call
        if 'response' in result:
            # Cached response
            return jsonify({
                'success': True,
                'response': result['response'],
                'metadata': result['metadata']
            })
        else:
            # Need to call LLM - return payload for streaming
            return jsonify({
                'success': True,
                'requires_llm': True,
                'payload': result['payload'],
                'metadata': result['metadata'],
                'signature': result.get('signature'),
                'cache_enabled': result.get('cache_enabled', False)
            })
            
    except Exception as e:
        print(f"Error in enhanced_analysis: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/quick-response', methods=['POST'])
def quick_response():
    """
    API endpoint cho quick template responses
    Trả về instant response cho common patterns
    """
    try:
        data = request.get_json()
        template_name = data.get('template_name')  # Optional specific template
        
        khaosat_data = get_khaosat_data_from_file(PATH_KHAOSAT)
        if not khaosat_data:
            return jsonify({'error': 'Không thể đọc dữ liệu khảo sát.'}), 400
        
        diem_data = get_diem_data_from_file(PATH_DIEM_SIMPLIFIED)
        
        # Analyze student pattern
        pattern_info = enhanced_consultant.analyze_student_pattern(khaosat_data, diem_data)
        
        # Prepare analysis data for template matching
        analysis_data = {
            **pattern_info,
            "major": khaosat_data.get("thong_tin_ca_nhan", {}).get("khoa", ""),
            "weak_skills_detail": {},
            "best_subjects": [],
            "top_skills": [],
            "weak_areas": []
        }
        
        # Extract detailed skills data
        skills_fields = [
            "Thai_do_hoc_tap", "Su_dung_mang_xa_hoi", "Gia_dinh_Xa_hoi", "Ban_be",
            "Moi_truong_hoc_tap", "Quan_ly_thoi_gian", "Tu_hoc", "Hop_tac_nhom",
            "Tu_duy_phan_bien", "Tiep_thu_xu_ly_kien_thuc"
        ]
        
        skill_scores = {}
        for field in skills_fields:
            skill_data = khaosat_data.get(field, {})
            if isinstance(skill_data, dict) and "phan_tram_diem" in skill_data:
                score = skill_data["phan_tram_diem"]
                skill_scores[field] = score
                if score < 70:
                    analysis_data["weak_skills_detail"][field] = score
                    analysis_data["weak_areas"].append(field.replace("_", " "))
        
        # Get top skills
        sorted_skills = sorted(skill_scores.items(), key=lambda x: x[1], reverse=True)
        analysis_data["top_skills"] = [skill.replace("_", " ") for skill, _ in sorted_skills[:3]]
        
        # Get best subjects from grades
        if diem_data:
            grade_values = {"A+": 95, "A": 90, "B+": 85, "B": 80, "C+": 75, "C": 70}
            subject_scores = []
            
            for subject in diem_data:
                if "diem_tk_chu" in subject and subject["diem_tk_chu"] in grade_values:
                    subject_scores.append((
                        subject.get("ten_mon_hoc", "Unknown"), 
                        grade_values[subject["diem_tk_chu"]]
                    ))
            
            subject_scores.sort(key=lambda x: x[1], reverse=True)
            analysis_data["best_subjects"] = [subj for subj, _ in subject_scores[:3]]
        
        # Generate quick response
        template_response = quick_templates.generate_quick_response(analysis_data, template_name)
        
        if template_response:
            return jsonify({
                'success': True,
                'response': template_response['response'],
                'template_name': template_response['template_name'],
                'confidence': template_response['confidence'],
                'metadata': {
                    'source': 'quick_template',
                    'response_time': 0.05,  # Templates are instant
                    'pattern_matched': True
                }
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Không tìm thấy template phù hợp',
                'available_templates': list(quick_templates.templates.keys())
            })
            
    except Exception as e:
        print(f"Error in quick_response: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/session-command', methods=['POST'])
def session_command():
    """
    API endpoint xử lý Ollama session commands
    Commands: /save, /load, /clear, /list, /delete, /template, /finetune, /export
    """
    try:
        data = request.get_json()
        command = data.get('command', '')
        
        if not command.startswith('/'):
            return jsonify({'error': 'Command phải bắt đầu với /'}), 400
        
        # Process command through session manager
        result = session_manager.process_command(command)
        
        return jsonify(result)
        
    except Exception as e:
        print(f"Error in session_command: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/cache-feedback', methods=['POST'])
def cache_feedback():
    """
    API endpoint để lưu feedback và cập nhật cache
    """
    try:
        data = request.get_json()
        signature = data.get('signature')
        stage = data.get('stage')
        response = data.get('response')
        feedback_score = data.get('feedback_score')  # 1-5 scale
        
        if not all([signature, stage, response, feedback_score]):
            return jsonify({'error': 'Missing required parameters'}), 400
        
        # Save successful consultation to cache and RAG
        enhanced_consultant.save_successful_consultation(
            signature, stage, response, feedback_score
        )
        
        return jsonify({
            'success': True,
            'message': 'Feedback saved successfully',
            'cached': feedback_score >= 4
        })
        
    except Exception as e:
        print(f"Error in cache_feedback: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/system-stats', methods=['GET'])
def system_stats():
    """
    API endpoint để lấy thống kê hệ thống
    """
    try:
        consultant_stats = enhanced_consultant.get_performance_stats()
        template_stats = quick_templates.get_usage_statistics()
        
        return jsonify({
            'enhanced_consultant': consultant_stats,
            'template_system': template_stats,
            'session_info': {
                'current_session': session_manager.current_session is not None,
                'active_model': session_manager.active_model
            }
        })
        
    except Exception as e:
        print(f"Error in system_stats: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/knowledge-base', methods=['GET', 'POST'])
def knowledge_base_management():
    """
    API endpoint để quản lý knowledge base
    GET: Search knowledge base
    POST: Add new knowledge
    """
    try:
        if request.method == 'GET':
            query = request.args.get('query', '')
            top_k = int(request.args.get('top_k', 5))
            
            if not query:
                return jsonify({'error': 'Query parameter required'}), 400
            
            results = enhanced_consultant.rag_system.search_relevant_knowledge(query, top_k)
            
            return jsonify({
                'success': True,
                'query': query,
                'results': results,
                'total_documents': len(enhanced_consultant.rag_system.documents)
            })
        
        elif request.method == 'POST':
            data = request.get_json()
            content = data.get('content')
            metadata = data.get('metadata', {})
            
            if not content:
                return jsonify({'error': 'Content required'}), 400
            
            enhanced_consultant.rag_system.add_knowledge(content, metadata)
            
            return jsonify({
                'success': True,
                'message': 'Knowledge added successfully',
                'total_documents': len(enhanced_consultant.rag_system.documents)
            })
            
    except Exception as e:
        print(f"Error in knowledge_base_management: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/response-mode', methods=['GET', 'POST'])
def response_mode_management():
    """
    API endpoint để quản lý response mode
    GET: Get current mode
    POST: Set new mode
    """
    global response_mode
    
    try:
        if request.method == 'GET':
            return jsonify({
                'current_mode': response_mode,
                'available_modes': ['enhanced', 'quick', 'template', 'basic'],
                'mode_descriptions': {
                    'enhanced': 'Full RAG + Cache + LLM consultation',
                    'quick': 'Smart template with fallback to enhanced',
                    'template': 'Template-only responses (fastest)',
                    'basic': 'Original prompt system (no enhancements)'
                }
            })
        
        elif request.method == 'POST':
            data = request.get_json()
            new_mode = data.get('mode')
            
            valid_modes = ['enhanced', 'quick', 'template', 'basic']
            if new_mode not in valid_modes:
                return jsonify({
                    'error': f'Invalid mode. Available: {valid_modes}'
                }), 400
            
            response_mode = new_mode
            
            return jsonify({
                'success': True,
                'new_mode': response_mode,
                'message': f'Response mode changed to {response_mode}'
            })
            
    except Exception as e:
        print(f"Error in response_mode_management: {e}")
        return jsonify({'error': str(e)}), 500

# --- Cập nhật existing LLM endpoint để support enhanced features ---

# Main execution block
if __name__ == '__main__':
    print("🚀 Starting Enhanced Education Consultant System...")
    print("=" * 60)
    print(f"📊 Mode: {response_mode}")
    print(f"🤖 Model: {OLLAMA_MODEL}")
    print(f"🔗 Ollama URL: {OLLAMA_API_URL}")
    print(f"💾 Database: {PATH_KHAOSAT}, {PATH_DIEM_SIMPLIFIED}")
    print("=" * 60)
    
    # Start Flask development server
    app.run(
        debug=True,
        host='0.0.0.0',
        port=5000,
        threaded=True
    )