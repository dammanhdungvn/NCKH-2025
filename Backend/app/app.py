from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import json
import os
from datetime import datetime
from werkzeug.utils import secure_filename
from diem_converter import convert_excel_to_json

# --- LLM Integration Imports ---
# Assuming LLM files are in Backend/app/LLM relative to this file
from LLM.utils import get_khaosat_data_from_file, get_diem_data_from_file
from LLM.prompts import generate_prompt1_payload, generate_prompt2_payload, generate_prompt3_payload
from LLM.ollama_interactions import call_ollama_stream_logic, ollama_chat_streaming

app = Flask(__name__)
CORS(app)

# --- Configuration ---
# LLM Config (Update OLLAMA_API_URL if needed)
OLLAMA_API_URL = "http://192.168.2.114:11434/api/chat" # Make sure this is accessible from the backend server
OLLAMA_MODEL = "gemma2:2b"
PATH_KHAOSAT = '../Database/khaosat.json' # Adjusted path
PATH_DIEM = '../Database/diem.json' # Adjusted path

# --- Global States for LLM ---
llm_analysis_results = {
    "stage1_khaosat": "",
    "stage2_diem": "",
    "stage3_tonghop": ""
}
llm_conversation_history_stage3 = []

# Ensure the Database directory exists
os.makedirs('../Database', exist_ok=True)

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
            file_path = os.path.join('..', 'Database', filename)
            file.save(file_path)
            
            # Process the Excel file to JSON using the new converter
            json_path = PATH_DIEM
            success, message = convert_excel_to_json(file_path, json_path)
            
            if success:
                return jsonify({'message': 'File uploaded and processed successfully'}), 200
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

# --- New LLM Endpoints ---

@app.route('/api/start-llm-analysis', methods=['GET', 'POST'])
def start_llm_analysis_route():
    """
    API endpoint bắt đầu phân tích LLM
    - Đọc dữ liệu khảo sát và điểm
    - Thực hiện phân tích 3 giai đoạn
    - Stream kết quả về client
    """
    global llm_analysis_results
    global llm_conversation_history_stage3

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

    diem_data = get_diem_data_from_file(PATH_DIEM)
    if not diem_data:
        return Response(f"data: {json.dumps({'stage': 'setup', 'error': 'Không thể đọc dữ liệu điểm.'})}\n\n", mimetype='text/event-stream')

    payload1 = generate_prompt1_payload(khaosat_data, OLLAMA_MODEL)
    payload2 = generate_prompt2_payload(diem_data, khaosat_data, OLLAMA_MODEL)

    def combined_stream():
        """
        Hàm stream kết quả phân tích
        - Giai đoạn 1: Phân tích khảo sát
        - Giai đoạn 2: Phân tích điểm số
        - Giai đoạn 3: Tổng hợp và đề xuất
        """
        global llm_conversation_history_stage3
        
        # Stage 1
        yield from call_ollama_stream_logic(OLLAMA_API_URL, payload1, "stage1_khaosat", llm_analysis_results, llm_conversation_history_stage3)
        if llm_analysis_results.get("stage1_khaosat", "").startswith("<p style='color:red;'>"):
            print("Dừng ở stage 1 do lỗi.")
            yield f"data: {json.dumps({'status': 'error_stage1'})}\n\n"
            return

        # Stage 2
        yield from call_ollama_stream_logic(OLLAMA_API_URL, payload2, "stage2_diem", llm_analysis_results, llm_conversation_history_stage3)
        if llm_analysis_results.get("stage2_diem", "").startswith("<p style='color:red;'>"):
            print("Dừng ở stage 2 do lỗi.")
            yield f"data: {json.dumps({'status': 'error_stage2'})}\n\n"
            return

        # Stage 3
        phan_tich_ky_nang_text = llm_analysis_results.get("stage1_khaosat", "Không có dữ liệu phân tích kỹ năng.")
        phan_tich_diem_so_text = llm_analysis_results.get("stage2_diem", "Không có dữ liệu phân tích điểm số.")
        payload3 = generate_prompt3_payload(phan_tich_ky_nang_text, phan_tich_diem_so_text, khaosat_data, OLLAMA_MODEL)
        
        llm_conversation_history_stage3.clear() # Clear history before starting stage 3 stream
        yield from call_ollama_stream_logic(OLLAMA_API_URL, payload3, "stage3_tonghop", llm_analysis_results, llm_conversation_history_stage3)
        yield f"data: {json.dumps({'status': 'all_done'})}\n\n"

    return Response(combined_stream(), mimetype='text/event-stream')

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

if __name__ == '__main__':
    # Use port 5000 or another available port
    app.run(host='0.0.0.0', port=5000, debug=True) 