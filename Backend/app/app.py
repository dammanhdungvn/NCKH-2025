"""
Flask application for student learning analytics system.
This application handles survey submissions, grade file uploads, and LLM-based analysis.
"""

from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import json
import os
from datetime import datetime
from werkzeug.utils import secure_filename

from diem_converter import convert_excel_to_json
from LLM.utils import get_khaosat_data_from_file, get_diem_data_from_file
from LLM.prompts import generate_prompt1_payload, generate_prompt2_payload, generate_prompt3_payload
from LLM.ollama_interactions import call_ollama_stream_logic, ollama_chat_streaming

# --- Application Configuration ---
app = Flask(__name__)
CORS(app)

# --- Constants ---
OLLAMA_API_URL = "http://192.168.2.114:11434/api/chat"
OLLAMA_MODEL = "gemma3:12b"
DATABASE_DIR = '../Database'
PATH_KHAOSAT = os.path.join(DATABASE_DIR, 'khaosat.json')
PATH_DIEM = os.path.join(DATABASE_DIR, 'diem.json')

# Survey configuration
SURVEY_SECTIONS = {
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

# Global variables for LLM analysis
llm_analysis_results = {
    "stage1_khaosat": "",
    "stage2_diem": "",
    "stage3_tonghop": ""
}
llm_conversation_history_stage3 = []

# Ensure the Database directory exists
os.makedirs(DATABASE_DIR, exist_ok=True)

# --- Utility Functions ---
def calculate_percentage(scores, total_questions):
    """
    Calculate percentage score for a survey section.
    
    Args:
        scores (list): List of scores
        total_questions (int): Total number of questions
        
    Returns:
        float: Percentage score rounded to 2 decimal places
    """
    if not scores or total_questions <= 0:
        return 0.0
    
    total_score = sum(scores)
    max_possible_score = total_questions * 5
    percentage = (total_score / max_possible_score) * 100
    return round(percentage, 2)

def validate_file_upload(file):
    """
    Validate uploaded file.
    
    Args:
        file: Flask file object
        
    Returns:
        tuple: (is_valid, error_message)
    """
    if not file:
        return False, 'No file part'
    
    if file.filename == '':
        return False, 'No selected file'
    
    if not file.filename.endswith('.xlsx'):
        return False, 'Invalid file format. Only .xlsx files are allowed'
    
    return True, None

def extract_personal_info(data):
    """
    Extract personal information from survey data.
    
    Args:
        data (dict): Survey data
        
    Returns:
        dict: Personal information
    """
    return {
        "ma_so_sinh_vien": data.get("ma_so_sinh_vien"),
        "gioi_tinh": data.get("gioi_tinh"),
        "khoa": data.get("khoa"),
        "nam_hoc": data.get("nam_hoc"),
        "ho_ten": data.get("ho_va_ten")
    }

def process_survey_sections(data):
    """
    Process survey section scores.
    
    Args:
        data (dict): Survey data
        
    Returns:
        dict: Processed section results
    """
    results = {}
    
    for section_key, section_info in SURVEY_SECTIONS.items():
        section_scores = []
        
        for i in range(1, section_info["count"] + 1):
            score = data.get(f"{section_key}_{i}")
            if score is not None:
                try:
                    section_scores.append(int(score))
                except ValueError:
                    print(f"Warning: Could not convert score '{score}' to int for {section_key}_{i}")
                    continue

        if section_scores:
            percentage = calculate_percentage(section_scores, section_info["count"])
            results[section_info["name"]] = {
                "tong_so_cau_hoi": section_info["count"],
                "phan_tram_diem": percentage
            }
    
    return results

# --- API Routes ---
@app.route('/api/submit-survey', methods=['POST'])
def submit_survey():
    """
    Handle survey submission.
    
    Process personal information and survey scores,
    calculate percentages, and save to JSON file.
    
    Returns:
        JSON response with success/error message
    """
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        # Extract personal information
        personal_info = extract_personal_info(data)
        
        # Process survey sections
        section_results = process_survey_sections(data)
        
        # Combine results
        results = {
            "thong_tin_ca_nhan": personal_info,
            "thoi_gian_nop": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            **section_results
        }
        
        # Save to JSON file
        with open(PATH_KHAOSAT, 'w', encoding='utf-8') as f:
            json.dump([results], f, ensure_ascii=False, indent=4)
        
        return jsonify({"message": "Survey submitted successfully", "data": results}), 200
        
    except Exception as e:
        print(f"Error in submit_survey: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/upload-file', methods=['POST'])
def upload_file():
    """
    Handle file upload for grade sheets.
    
    Validate, save Excel file and convert to JSON format.
    
    Returns:
        JSON response with success/error message
    """
    try:
        file = request.files.get('file')
        is_valid, error_message = validate_file_upload(file)
        
        if not is_valid:
            return jsonify({'error': error_message}), 400
        
        # Save the file
        filename = secure_filename('diem.xlsx')
        file_path = os.path.join(DATABASE_DIR, filename)
        file.save(file_path)
        
        # Convert Excel to JSON
        success, message = convert_excel_to_json(file_path, PATH_DIEM)
        
        if success:
            return jsonify({'message': 'File uploaded and processed successfully'}), 200
        else:
            return jsonify({'error': message}), 500
            
    except Exception as e:
        print(f"Error in upload_file: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/get-data', methods=['GET'])
def get_data():
    """
    Get grade data.
    
    Returns:
        JSON response with grade data or error message
    """
    try:
        if not os.path.exists(PATH_DIEM):
            return jsonify({'error': 'No data file found'}), 404
            
        with open(PATH_DIEM, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return jsonify(data)
        
    except Exception as e:
        print(f"Error in get_data: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/get-khaosat-summary', methods=['GET'])
def get_khaosat_summary():
    """
    Get survey summary data.
    
    Returns:
        JSON response with survey data or error message
    """
    try:
        if not os.path.exists(PATH_KHAOSAT):
            return jsonify({'error': 'Không tìm thấy file dữ liệu khảo sát.'}), 404
            
        with open(PATH_KHAOSAT, 'r', encoding='utf-8') as f:
            khaosat_data_list = json.load(f)
        
        if not khaosat_data_list:
            return jsonify({'error': 'File khảo sát rỗng.'}), 404
            
        return jsonify(khaosat_data_list[0])
        
    except Exception as e:
        print(f"Error in get_khaosat_summary: {e}")
        return jsonify({'error': str(e)}), 500

# --- LLM Analysis Routes ---
@app.route('/api/start-llm-analysis', methods=['GET', 'POST'])
def start_llm_analysis_route():
    """
    Start LLM analysis process.
    
    Performs 3-stage analysis:
    1. Survey skill analysis
    2. Academic performance analysis
    3. Comprehensive analysis and recommendations
    
    Returns:
        Server-sent events stream with analysis results
    """
    global llm_analysis_results, llm_conversation_history_stage3

    # Reset results for new analysis
    llm_analysis_results = {
        "stage1_khaosat": "",
        "stage2_diem": "",
        "stage3_tonghop": ""
    }
    llm_conversation_history_stage3 = []

    # Load data
    khaosat_data = get_khaosat_data_from_file(PATH_KHAOSAT)
    if not khaosat_data:
        error_response = json.dumps({'stage': 'setup', 'error': 'Không thể đọc dữ liệu khảo sát.'})
        return Response(f"data: {error_response}\n\n", mimetype='text/event-stream')

    diem_data = get_diem_data_from_file(PATH_DIEM)
    if not diem_data:
        error_response = json.dumps({'stage': 'setup', 'error': 'Không thể đọc dữ liệu điểm.'})
        return Response(f"data: {error_response}\n\n", mimetype='text/event-stream')

    # Generate prompts
    payload1 = generate_prompt1_payload(khaosat_data, OLLAMA_MODEL)
    payload2 = generate_prompt2_payload(diem_data, khaosat_data, OLLAMA_MODEL)

    def combined_stream():
        """
        Stream combined analysis results.
        
        Yields:
            Server-sent events with analysis progress and results
        """
        global llm_conversation_history_stage3
        
        # Stage 1: Survey analysis
        yield from call_ollama_stream_logic(
            OLLAMA_API_URL, payload1, "stage1_khaosat", 
            llm_analysis_results, llm_conversation_history_stage3
        )
        
        if llm_analysis_results.get("stage1_khaosat", "").startswith("<p style='color:red;'>"):
            print("Stopped at stage 1 due to error.")
            yield f"data: {json.dumps({'status': 'error_stage1'})}\n\n"
            return

        # Stage 2: Grade analysis
        yield from call_ollama_stream_logic(
            OLLAMA_API_URL, payload2, "stage2_diem", 
            llm_analysis_results, llm_conversation_history_stage3
        )
        
        if llm_analysis_results.get("stage2_diem", "").startswith("<p style='color:red;'>"):
            print("Stopped at stage 2 due to error.")
            yield f"data: {json.dumps({'status': 'error_stage2'})}\n\n"
            return

        # Stage 3: Comprehensive analysis
        stage1_text = llm_analysis_results.get("stage1_khaosat", "Không có dữ liệu phân tích kỹ năng.")
        stage2_text = llm_analysis_results.get("stage2_diem", "Không có dữ liệu phân tích điểm số.")
        payload3 = generate_prompt3_payload(stage1_text, stage2_text, khaosat_data, OLLAMA_MODEL)
        
        llm_conversation_history_stage3.clear()
        yield from call_ollama_stream_logic(
            OLLAMA_API_URL, payload3, "stage3_tonghop", 
            llm_analysis_results, llm_conversation_history_stage3
        )
        
        yield f"data: {json.dumps({'status': 'all_done'})}\n\n"

    return Response(combined_stream(), mimetype='text/event-stream')

@app.route('/api/llm-chat', methods=['POST'])
def llm_chat_route():
    """
    Handle chat with LLM.
    
    Process user messages and stream LLM responses.
    
    Returns:
        Server-sent events stream with chat responses
    """
    global llm_conversation_history_stage3
    
    try:
        user_message = request.json.get('message')
        
        if not user_message:
            return jsonify({"error": "No message provided"}), 400
        
        if not llm_conversation_history_stage3:
            return jsonify({
                "error": "Phân tích ban đầu chưa được thực hiện hoặc đã xảy ra lỗi. Vui lòng chạy lại phân tích."
            }), 400

        return Response(
            ollama_chat_streaming(OLLAMA_API_URL, OLLAMA_MODEL, llm_conversation_history_stage3, user_message),
            mimetype='text/event-stream'
        )
        
    except Exception as e:
        print(f"Error in llm_chat_route: {e}")
        return jsonify({"error": str(e)}), 500

# --- Application Entry Point ---
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 