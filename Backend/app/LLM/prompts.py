"""
Prompt generation module for LLM analysis.
This module contains functions to generate structured prompts for different analysis stages.
"""

import json
from typing import Dict, Any, List


# Analysis sections configuration
ANALYSIS_SECTIONS = [
    "Thai_do_hoc_tap", "Su_dung_mang_xa_hoi", "Gia_dinh_Xa_hoi", "Ban_be",
    "Moi_truong_hoc_tap", "Quan_ly_thoi_gian", "Tu_hoc", "Hop_tac_nhom",
    "Tu_duy_phan_bien", "Tiep_thu_xu_ly_kien_thuc"
]

# Keywords for general education courses to exclude
GENERAL_EDUCATION_KEYWORDS = [
    "thể chất", "quốc phòng", "an ninh", "chính trị", "mác - lênin", 
    "tư tưởng hồ chí minh", "chủ nghĩa xã hội", "pháp luật đại cương", 
    "tiếng anh", "hóa học đại cương", "vật lý đại cương", "đường lối", 
    "quân sự", "kinh tế chính trị", "lịch sử đảng", "nhập môn ngành", 
    "Kỹ thuật bắn súng"
]

# Grade letter to GPA conversion
GRADE_TO_GPA = {
    "A+": 4.0, "A": 3.7, "B+": 3.5, "B": 3.0, "C+": 2.5, 
    "C": 2.0, "D+": 1.5, "D": 1.0, "F": 0.0
}


def convert_grade_letter_to_gpa(grade_letter: str) -> float:
    """
    Convert grade letter to GPA score.
    
    Args:
        grade_letter (str): Grade letter (A+, A, B+, B, C+, C, D+, D, F)
        
    Returns:
        float: GPA score
    """
    return GRADE_TO_GPA.get(grade_letter.upper(), 0.0)


def generate_prompt1_payload(khaosat_info: Dict[str, Any], ollama_model: str) -> Dict[str, Any]:
    """
    Generate prompt payload for stage 1: Survey skill analysis.
    
    Args:
        khaosat_info (Dict[str, Any]): Survey information data
        ollama_model (str): Name of the Ollama model to use
        
    Returns:
        Dict[str, Any]: Prompt payload for Ollama API
    """
    personal_info = khaosat_info.get("thong_tin_ca_nhan", {})
    
    # Extract learning skill data
    skill_data = {
        key: khaosat_info.get(key) 
        for key in ANALYSIS_SECTIONS 
        if khaosat_info.get(key) is not None
    }

    system_prompt = _build_stage1_system_prompt()
    user_prompt = _build_stage1_user_prompt(personal_info, skill_data)

    return {
        "model": ollama_model,
        "messages": [
            {"role": "system", "content": system_prompt}, 
            {"role": "user", "content": user_prompt}
        ],
        "stream": True,
        "options": {"temperature": 0.3, "num_ctx": 3072}
    }


def generate_prompt2_payload(
    all_subjects: List[Dict[str, Any]], 
    khaosat_info: Dict[str, Any], 
    ollama_model: str
) -> Dict[str, Any]:
    """
    Generate prompt payload for stage 2: Academic performance analysis.
    
    Args:
        all_subjects (List[Dict[str, Any]]): List of all subject data from diemllm.json
        khaosat_info (Dict[str, Any]): Survey information data
        ollama_model (str): Name of the Ollama model to use
        
    Returns:
        Dict[str, Any]: Prompt payload for Ollama API
    """
    # Filter out general education courses
    specialized_subjects = _filter_specialized_subjects(all_subjects)
    print(f"📊 Filtered subjects: {len(all_subjects)} → {len(specialized_subjects)} specialized subjects")
    
    # Format subjects for prompt
    subjects_text = _format_subjects_for_prompt(specialized_subjects)
    print(f"📝 Formatted {len(specialized_subjects)} subjects for LLM prompt")
    
    personal_info = khaosat_info.get("thong_tin_ca_nhan", {})
    department = personal_info.get('khoa', 'Chưa rõ thông tin khoa')
    
    system_prompt = _build_stage2_system_prompt(department)
    user_prompt = _build_stage2_user_prompt(department, subjects_text)

    return {
        "model": ollama_model,
        "messages": [
            {"role": "system", "content": system_prompt}, 
            {"role": "user", "content": user_prompt}
        ],
        "stream": True,
        "options": {"temperature": 0.1, "num_ctx": 3072}
    }


def generate_prompt3_payload(
    stage1_analysis: str, 
    stage2_analysis: str, 
    khaosat_info: Dict[str, Any], 
    ollama_model: str
) -> Dict[str, Any]:
    """
    Generate prompt payload for stage 3: Comprehensive analysis and recommendations.
    
    Args:
        stage1_analysis (str): Results from stage 1 analysis
        stage2_analysis (str): Results from stage 2 analysis
        khaosat_info (Dict[str, Any]): Survey information data
        ollama_model (str): Name of the Ollama model to use
        
    Returns:
        Dict[str, Any]: Prompt payload for Ollama API
    """
    personal_info = khaosat_info.get("thong_tin_ca_nhan", {})
    student_name = personal_info.get('ho_ten', 'Sinh viên')
    department = personal_info.get('khoa', 'Chưa rõ thông tin khoa')
    
    system_prompt = _build_stage3_system_prompt(department)
    user_prompt = _build_stage3_user_prompt(
        student_name, department, stage1_analysis, stage2_analysis
    )

    return {
        "model": ollama_model,
        "messages": [
            {"role": "system", "content": system_prompt}, 
            {"role": "user", "content": user_prompt}
        ],
        "stream": True,
        "options": {"temperature": 0.5, "num_ctx": 4096}
    }


def _filter_specialized_subjects(all_subjects: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Filter out general education courses from subject list.
    
    Args:
        all_subjects (List[Dict[str, Any]]): List of all subjects from diemllm.json
        
    Returns:
        List[Dict[str, Any]]: Filtered list of specialized subjects
    """
    specialized_subjects = []
    
    for subject in all_subjects:
        subject_name_lower = subject['ten_mon'].lower()
        is_general_education = any(
            keyword in subject_name_lower 
            for keyword in GENERAL_EDUCATION_KEYWORDS
        )
        
        if not is_general_education:
            specialized_subjects.append(subject)
            print(f"✅ Specialized: {subject['ten_mon']} - {subject['diem_tk_chu']}")
        else:
            print(f"🚫 General education (filtered): {subject['ten_mon']}")
    
    return specialized_subjects


def _format_subjects_for_prompt(subjects: List[Dict[str, Any]]) -> str:
    """
    Format subject data for inclusion in prompts.
    
    Args:
        subjects (List[Dict[str, Any]]): List of subjects from diemllm.json
        
    Returns:
        str: Formatted subject text
    """
    if not subjects:
        return "Không có môn học chuyên ngành nào được tìm thấy sau khi lọc bỏ các môn đại cương chung."
    
    formatted_lines = []
    for subject in subjects:
        # Convert grade letter to GPA
        grade_letter = subject.get('diem_tk_chu', 'F')
        gpa_score = convert_grade_letter_to_gpa(grade_letter)
        
        line = (f"- Tên môn: {subject['ten_mon']}, Điểm hệ 4: {gpa_score:.1f} "
                f"(Điểm chữ: {grade_letter}), Số tín chỉ: {subject['so_tin_chi']}")
        formatted_lines.append(line)
        print(f"📋 Formatted: {subject['ten_mon']} - {grade_letter} → {gpa_score:.1f}")
    
    return "\n".join(formatted_lines)


def _build_stage1_system_prompt() -> str:
    """Build system prompt for stage 1 analysis."""
    return f"""Bạn là một chuyên gia phân tích giáo dục và tâm lý học tập, nhiệm vụ của bạn là đánh giá chi tiết và khách quan các yếu tố và kỹ năng học tập của sinh viên dựa trên dữ liệu khảo sát được cung cấp.

**Các kỹ năng cần được đánh giá:**
1. Thái độ học tập
2. Sử dụng mạng xã hội
3. Gia đình – Xã hội
4. Bạn bè
5. Môi trường học tập
6. Kỹ năng Quản lý thời gian
7. Kỹ năng tự học
8. Kỹ năng làm việc nhóm
9. Tư duy phản biện
10. Tiếp thu & xử lý kiến thức

**QUY TẮC PHÂN TÍCH VÀ ĐÁNH GIÁ (TUÂN THỦ NGHIÊM NGẶT):**
1. **Thang đánh giá mức độ (dựa trên phần trăm điểm ('phan_tram_diem') của mỗi mục):**
   * 80% - 100%: **Tốt/Thành thạo**. Cho thấy sinh viên làm chủ hoặc có điều kiện rất thuận lợi ở khía cạnh này.
   * 60% - 79%: **Khá**. Sinh viên thể hiện ở mức độ ổn, có nền tảng nhưng có thể cải thiện thêm.
   * 40% - 60%: **Trung bình/Cần lưu ý**. Sinh viên đạt mức cơ bản, nhưng đây là yếu tố cần được chú ý để cải thiện.
   * Dưới 40%: **Yếu/Cần cải thiện đáng kể**. Đây là yếu tố sinh viên gặp khó khăn hoặc chưa đầu tư đúng mức, cần có sự thay đổi lớn.

2. **Nội dung phân tích cho từng yếu tố:**
   * Nêu rõ tên yếu tố.
   * Trích dẫn % điểm.
   * Đưa ra nhận định MỨC ĐỘ dựa trên thang đánh giá ở trên (ví dụ: "Rất Tốt", "Cần cải thiện đáng kể").
   * Giải thích ngắn gọn ý nghĩa của mức điểm đó đối với việc học tập của sinh viên trong thực tế liên quan đến yếu tố đó. KHÔNG đưa ra giải pháp hay đề xuất cải thiện chi tiết ở giai đoạn này.

3. **Yêu cầu chung:**
   * Sử dụng ngôn ngữ chuyên nghiệp, chính xác, khách quan.
   * Tập trung vào việc **đánh giá hiện trạng** dựa trên dữ liệu.
   * Trình bày kết quả theo từng mục đã được liệt kê trong dữ liệu khảo sát."""


def _build_stage1_user_prompt(personal_info: Dict[str, Any], skill_data: Dict[str, Any]) -> str:
    """Build user prompt for stage 1 analysis."""
    return f"""Dưới đây là dữ liệu khảo sát về các yếu tố và kỹ năng học tập của sinh viên {personal_info.get('ho_ten', 'N/A')}, mã sinh viên (MSV: {personal_info.get('ma_so_sinh_vien', 'N/A')}), khoa {personal_info.get('khoa', 'Chưa rõ')}, năm học {personal_info.get('nam_hoc', 'N/A')}. 
Dữ liệu bao gồm tên yếu tố/kỹ năng và 'phan_tram_diem' tương ứng:

{json.dumps(skill_data, indent=2, ensure_ascii=False)}

**YÊU CẦU PHÂN TÍCH:**
Hãy phân tích và đánh giá **TUẦN TỰ TỪNG YẾU TỐ/KỸ NĂNG** có trong dữ liệu trên theo đúng QUY TẮC PHÂN TÍCH VÀ ĐÁNH GIÁ đã được nêu trong vai trò hệ thống của bạn. 
Với mỗi yếu tố, hãy:
a. Nêu tên yếu tố.
b. Trích dẫn 'phan_tram_diem'.
c. Đưa ra nhận định về mức độ (ví dụ: "Rất Tốt", "Tốt/Khá", "Trung bình/Cần lưu ý", "Yếu/Cần cải thiện đáng kể").
d. Giải thích ngắn gọn ý nghĩa của mức điểm đó đối với sinh viên liên quan đến yếu tố đó.
e. Format câu trả lời là dùng Table

Sau khi phân tích tất cả các yếu tố, hãy đưa ra một **TỔNG KẾT NGẮN GỌN** về:
1. Liệt kê yếu tố/kỹ năng mà sinh viên được đánh giá là **Tốt/Thành thạo**.
2. Liệt kê yếu tố/kỹ năng mà sinh viên **cần chú trọng cải thiện nhất** (dựa trên % điểm thấp nhất và nhận định mức độ).

LƯU Ý QUAN TRỌNG: Ở giai đoạn này, chỉ tập trung PHÂN TÍCH VÀ ĐÁNH GIÁ. KHÔNG đưa ra bất kỳ đề xuất, giải pháp, hay kế hoạch cải thiện chi tiết nào."""


def _build_stage2_system_prompt(department: str) -> str:
    """Build system prompt for stage 2 analysis."""
    return f"""Bạn là một chuyên gia phân tích học thuật có kinh nghiệm với nhiều ngành học khác nhau ở bậc đại học. 
Nhiệm vụ của bạn là phân tích bảng điểm các môn học **CHUYÊN NGÀNH (đã được lọc sơ bộ)** của một sinh viên thuộc khoa "{department}" để xác định các môn học/nhóm môn học thể hiện năng lực nổi bật và các lĩnh vực kiến thức tiềm năng của sinh viên đó trong chuyên ngành của họ.

Đây là CẤU TRÚC DỮ LIỆU ĐẦU VÀO (JSON) để giúp bạn hiểu được và dễ dàng phân tích hiệu quả: Dữ liệu bảng điểm là một danh sách các đối tượng, mỗi đối tượng biểu diễn thông tin của một học kỳ.
- Mỗi đối tượng học kỳ có các trường quan trọng sau:
* `"ten_hoc_ky"`: Tên đầy đủ của học kỳ (Ví dụ: "Học kỳ 2 - Năm học 2024 - 2025").
* `"dtb_tich_luy_he_4"`: Điểm Trung bình Tích lũy (GPA) của sinh viên tính đến hết học kỳ này, theo hệ 4 (Ví dụ: "3.20-Điểm"). Điểm GPA hiện tại mới nhất là giá trị `"dtb_tich_luy_he_4"` trong đối tượng học kỳ **đầu tiên** trong danh sách JSON (do dữ liệu được sắp xếp từ học kỳ gần nhất đến cũ nhất).
* `"ds_diem_mon_hoc"`: Một danh sách chứa các đối tượng biểu diễn điểm của từng môn học trong học kỳ này.
* ten_hoc_ky": Học kỳ (ví dụ: "Học kỳ 2 - Năm học 2024 - 2025")
* "ten_mon": Tên môn học (ví dụ: "Phát triển ứng dụng IoT")
* "diem_tk": Điểm tổng kết môn hệ số (ví dụ: "7.6")
* "diem_tk_chu": Điểm tổng kết môn hệ chữ cái (ví dụ: "B")

**QUY TẮC PHÂN TÍCH VÀ ĐÁNH GIÁ (TUÂN THỦ NGHIÊM NGẶT):**
1. **Đối tượng phân tích:** Tập trung vào danh sách các môn học được cung cấp.
2. **Đánh giá kết quả môn học (dựa trên Điểm hệ 4 và Điểm chữ):**
   * A - A+ (Thường từ 3.7 - 4.0): Xuất sắc.
   * B+ (Thường từ 3.0 - 3.6): Giỏi.
   * C+ - B (Thường từ 2.5 - 2.9): Khá.
   * C (Thường từ 2.0 - 2.5): Trung bình.
   * D - D+ (Thường từ 1.0 - 1.5): Yếu.
   * F (Dưới 1.0): Không đạt phải học lại môn.
3. **Xác định các lĩnh vực/nhóm môn học chuyên ngành nổi bật:** Dựa vào các môn học có kết quả tốt (ví dụ: từ B+ trở lên), hãy xác định và nhóm các môn có liên quan đến nhau để làm nổi bật các lĩnh vực kiến thức hoặc cụm chuyên môn mà sinh viên thể hiện tốt trong ngành học của mình (khoa "{department}").
4. **Yêu cầu chung:** Tập trung vào việc **xác định các lĩnh vực học thuật mạnh**. KHÔNG đưa ra kế hoạch phát triển hay dự đoán nghề nghiệp chi tiết ở bước này."""


def _build_stage2_user_prompt(department: str, subjects_text: str) -> str:
    """Build user prompt for stage 2 analysis."""
    return f"""Sinh viên này thuộc khoa: **{department}**.
Dưới đây là bảng điểm các môn học được cho là thuộc chuyên ngành của sinh viên này:

{subjects_text}

**YÊU CẦU PHÂN TÍCH:**
1. **Liệt kê các môn học chuyên ngành có kết quả đánh giá môn học đạt từ Giỏi (điểm chữ B+) đến Xuất sắc (điểm chữ A - A+):** Format trả lời là Table.
2. **Xác định và nhóm các mảng trong ngành {department}:** Dựa trên các môn học có kết quả tốt, nhóm các môn có kiến thức liên quan.
3. **Xác định các lĩnh vực chuyên ngành tiềm năng nhất:** Dựa trên sự phân nhóm, chỉ ra 1-3 lĩnh vực/cụm chuyên môn mà sinh viên này có kết quả các môn học và năng lực học tập tốt nhất trong khoa "{department}". Nêu rõ lý do.
4. **Nhận xét về những môn học chuyên ngành, nhưng môn nền tảng cần thiết nắm vững trong ngành {department} cần cải thiện nếu kết quả đánh giá "Điểm chữ" nằm trong các điểm sau [F, D, D+, C, C+, B]**.

LƯU Ý QUAN TRỌNG: Chỉ tập trung PHÂN TÍCH ĐIỂM SỐ CÁC MÔN CHUYÊN NGÀNH và XÁC ĐỊNH LĨNH VỰC HỌC THUẬT THẾ MẠNH."""


def _build_stage3_system_prompt(department: str) -> str:
    """Build system prompt for stage 3 analysis."""
    return f"""Bạn là một chuyên gia tư vấn giáo dục và hướng nghiệp dày dặn kinh nghiệm, với vai trò xây dựng một "Hệ thống phân tích và đánh giá kỹ năng học tập của sinh viên". 
Sinh viên này thuộc khoa "{department}".
Nhiệm vụ của bạn là tổng hợp thông tin từ hai báo cáo phân tích trước đó (Báo cáo 1: Kỹ năng học tập từ khảo sát; Báo cáo 2: Thế mạnh học thuật từ bảng điểm chuyên ngành của khoa "{department}") để đưa ra một bản đánh giá tổng hợp, toàn diện và những đề xuất phát triển cụ thể, bao gồm cả việc định hướng các mảng chuyên môn hẹp mà sinh viên nên theo đuổi trong ngành học của mình.

**QUY TẮC TƯ VẤN (TUÂN THỦ NGHIÊM NGẶT):**
1. **Tính tổng hợp và kết nối:** Phải liên kết chặt chẽ thông tin từ Báo cáo 1 và Báo cáo 2.
2. **Bằng chứng cụ thể:** Mọi nhận định và đề xuất phải dựa trên dữ liệu đã được phân tích từ hai báo cáo trước.
3. **Phù hợp với chuyên ngành:** Các đề xuất về học thuật, nghề nghiệp, khóa học, chứng chỉ và **đặc biệt là các mảng chuyên môn hẹp** phải phù hợp với chuyên ngành của sinh viên là khoa "{department}" và các lĩnh vực thế mạnh đã được xác định từ Báo cáo 2, kết hợp với kỹ năng từ Báo cáo 1.
4. **Tính thực tế và khả thi:** Các đề xuất phải phù hợp với năng lực và điều kiện của sinh viên.
5. **Tính hệ thống:** Câu trả lời phải thể hiện một cái nhìn tổng thể về năng lực học tập của sinh viên.
6. **Không trùng lặp:** Không nhắc lại chi tiết phân tích đã có ở Báo cáo 1 và 2. Sử dụng kết luận từ các báo cáo đó.
7. **Ngôn ngữ:** Chuyên nghiệp, tích cực, khích lệ, và mang tính định hướng rõ ràng."""


def _build_stage3_user_prompt(
    student_name: str, 
    department: str, 
    stage1_analysis: str, 
    stage2_analysis: str
) -> str:
    """Build user prompt for stage 3 analysis."""
    return f"""Thông tin đầu vào cho việc xây dựng "Hệ thống phân tích và đánh giá kỹ năng học tập" cho sinh viên {student_name}, khoa **{department}**:

**Báo cáo 1: Tóm tắt Phân tích Kỹ năng Học tập từ Khảo sát**
(Bao gồm nhận định mức độ và ý nghĩa của từng yếu tố: Thái độ học tập, Sử dụng mạng xã hội, Gia đình – Xã hội, Bạn bè, Môi trường học tập, Kỹ năng Quản lý thời gian, Kỹ năng tự học, Kỹ năng làm việc nhóm, Tư duy phản biện, Tiếp thu & xử lý kiến thức; cùng với 3 yếu tố tốt nhất và 3 yếu tố cần cải thiện nhất từ khảo sát).
```
{stage1_analysis}
```

**Báo cáo 2: Tóm tắt Phân tích Thế mạnh Học thuật từ Bảng điểm Chuyên ngành (Khoa: {department})**
(Bao gồm các môn chuyên ngành nổi bật, các lĩnh vực/cụm chuyên môn tiềm năng dựa trên điểm số trong khoa "{department}", và những môn chuyên ngành (nếu có) cần cải thiện).
```
{stage2_analysis}
```

**YÊU CẦU XÂY DỰNG HỆ THỐNG ĐÁNH GIÁ VÀ ĐỀ XUẤT CHO SINH VIÊN (Khoa: {department}):**
Dựa trên việc **tổng hợp và kết nối thông tin** từ hai báo cáo trên, hãy cung cấp một bản đánh giá và đề xuất chi tiết, có cấu trúc như sau:

**I. ĐÁNH GIÁ TỔNG QUAN VỀ NĂNG LỰC HỌC TẬP CỦA SINH VIÊN (Khoa: {department}):**
    1. **Điểm mạnh nổi bật tổng hợp:** Kết hợp kỹ năng vượt trội (Báo cáo 1) với lĩnh vực học thuật xuất sắc (Báo cáo 2) để chỉ ra thế mạnh toàn diện nhất của sinh viên.
    2. **Những khía cạnh cần ưu tiên phát triển:** Kết hợp kỹ năng cần cải thiện (Báo cáo 1) với môn chuyên ngành cần cố gắng hơn (Báo cáo 2) để xác định lĩnh vực cần tập trung nỗ lực.
    3. **Sự tương thích giữa Kỹ năng và Học thuật chuyên ngành ("{department}"):** Phân tích xem các kỹ năng học tập hiện tại (Báo cáo 1) đang hỗ trợ hay cản trở việc học các lĩnh vực chuyên ngành (Báo cáo 2) như thế nào? Nêu ví dụ cụ thể.

**II. ĐỀ XUẤT LỘ TRÌNH PHÁT TRIỂN KỸ NĂNG VÀ HỌC THUẬT (Phù hợp với Khoa "{department}"):**
    1. **Mục tiêu phát triển tổng thể (6-12 tháng):** Đề xuất 1-2 mục tiêu tổng thể.
    2. **Kế hoạch hành động chi tiết cho các khía cạnh cần cải thiện:**
        * Với **MỖI kỹ năng cần cải thiện nhất** (từ Báo cáo 1 và I.2), đề xuất 2-3 hành động/phương pháp cụ thể.
        * Với **MỖI môn học chuyên ngành cần cải thiện** (từ Báo cáo 2 và I.2), gợi ý cách tiếp cận học tập hiệu quả.
    3. **ĐỊNH HƯỚNG CHUYÊN MÔN SÂU (MẢNG NÊN THEO ĐUỔI TRONG NGÀNH):**
        * Dựa trên **sự kết hợp** giữa các lĩnh vực học thuật tiềm năng nhất (từ Báo cáo 2) và các kỹ năng mềm/tư duy nổi bật (từ Báo cáo 1), hãy **đề xuất 1-2 mảng chuyên môn hẹp (sub-fields/specializations) cụ thể** trong ngành học ("{department}") mà sinh viên này có tiềm năng lớn nhất và nên tập trung theo đuổi.
        * **Giải thích rõ ràng lý do** cho mỗi đề xuất mảng chuyên môn, chỉ ra sự phù hợp giữa điểm mạnh học thuật và các kỹ năng liên quan. (Ví dụ: "Với thế mạnh ở các môn Mạng máy tính, An ninh mạng cùng với kỹ năng Tư duy phản biện tốt, sinh viên nên cân nhắc theo đuổi chuyên sâu mảng An toàn thông tin (Security). Kỹ năng logic sẽ hỗ trợ tốt cho việc phân tích và giải quyết các vấn đề bảo mật phức tạp.")
        * Gợi ý các môn học chuyên sâu tự chọn (nếu có), chủ đề nghiên cứu/dự án cá nhân liên quan đến các mảng đề xuất này.

**III. GỢI Ý TÀI NGUYÊN VÀ HỖ TRỢ PHÁT TRIỂN (Phù hợp với Khoa "{department}" và định hướng đã đề xuất):**
    1. **Khóa học/Chứng chỉ:** Đề xuất 2-3 khóa học online hoặc chứng chỉ nghề nghiệp PHÙ HỢP với các mảng chuyên môn hẹp đã đề xuất ở mục II.3.
    2. **Nguồn tài liệu/ Cộng đồng:** Gợi ý 2-3 nguồn tài liệu hoặc cộng đồng liên quan.
    3. **Hoạt động ngoại khóa/Thực tiễn:** Gợi ý các hoạt động phù hợp.

**IV. KẾT LUẬN VÀ LỜI KHUYÊN ĐỘNG VIÊN:**
    * Tóm tắt những nhận định quan trọng nhất về tiềm năng của sinh viên.
    * Đưa ra lời khuyên cuối cùng để sinh viên tự tin, chủ động.

Hãy đảm bảo câu trả lời khoa học, logic, dễ hiểu và hữu ích, và đi sâu vào từng khía cạnh để phân tích, dùng các icon phù hợp và chuyên nghiệp trong câu trả lời."""


# if __name__ == "__main__":
#     # Test code để in ra dữ liệu THỰC TẾ mà app.py gửi tới prompts.py
#     import sys
#     import os
    
#     # Add path để import được các module khác
#     sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    
#     from utils import get_diem_data_from_file
    
#     # Sử dụng ĐÚNG đường dẫn như trong app.py
#     DATABASE_DIR = os.path.join('..', '..', '..', 'Database')
#     PATH_DIEM_LLM = os.path.join(DATABASE_DIR, 'diemllm.json')
    
#     print("🔍 TEST: Dữ liệu THỰC TẾ mà app.py gửi tới prompts.py")
#     print("=" * 60)
#     print(f"📁 Đường dẫn: {os.path.abspath(PATH_DIEM_LLM)}")
#     print(f"📁 File exists: {os.path.exists(PATH_DIEM_LLM)}")
#     print()
    
#     # Đọc dữ liệu GIỐNG HỆT trong app.py dòng 301
#     print("📖 Gọi: get_diem_data_from_file(PATH_DIEM_LLM)")
#     diem_data = get_diem_data_from_file(PATH_DIEM_LLM)
    
#     if diem_data:
#         print(f"✅ Thành công! get_diem_data_from_file() trả về: {type(diem_data)}")
#         print(f"📊 Số lượng môn học: {len(diem_data)}")
#         print()
        
#         # In ra cấu trúc dữ liệu thực tế
#         print("🔍 CẤU TRÚC DỮ LIỆU THỰC TẾ:")
#         print("-" * 40)
#         if len(diem_data) > 0:
#             print("Ví dụ 1 môn học đầu tiên:")
#             first_subject = diem_data[0]
#             print(f"Type: {type(first_subject)}")
#             print(f"Keys: {list(first_subject.keys())}")
#             print(f"Content: {first_subject}")
#             print()
            
#         # In ra 5 môn đầu tiên
#         print("📝 DANH SÁCH 5 MÔN HỌC ĐẦU TIÊN:")
#         print("-" * 40)
#         for i, subject in enumerate(diem_data[:5]):
#             print(f"{i+1}. {subject}")
#             print()
        
#         # Test thực tế generate_prompt2_payload như trong app.py
#         print("🤖 TEST THỰC TẾ GENERATE_PROMPT2_PAYLOAD:")
#         print("-" * 40)
        
#         # Mock khaosat_info như trong app.py
#         mock_khaosat_info = {
#             "thong_tin_ca_nhan": {
#                 "ho_ten": "Test Student", 
#                 "khoa": "Công nghệ thông tin"
#             }
#         }
        
#         try:
#             # Gọi ĐÚNG hàm như trong app.py dòng 308
#             payload2 = generate_prompt2_payload(diem_data, mock_khaosat_info, "test-model")
#             print("✅ generate_prompt2_payload() thành công!")
#             print(f"📊 Payload type: {type(payload2)}")
#             print(f"🔑 Payload keys: {list(payload2.keys())}")
            
#             # Extract user prompt để thấy dữ liệu cuối cùng gửi cho LLM
#             if 'messages' in payload2 and len(payload2['messages']) > 1:
#                 user_message = payload2['messages'][1]['content']
#                 print("\n📝 NỘI DUNG CUỐI CÙNG GỬI CHO LLM:")
#                 print("-" * 40)
#                 # In ra 1000 ký tự đầu của prompt
#                 print(user_message[:1000] + "..." if len(user_message) > 1000 else user_message)
                
#         except Exception as e:
#             print(f"❌ Lỗi khi gọi generate_prompt2_payload(): {e}")
#             print(f"📋 Chi tiết lỗi: {type(e).__name__}")
#             import traceback
#             traceback.print_exc()
            
#     else:
#         print("❌ get_diem_data_from_file() trả về None hoặc empty")
#         print("🔍 Kiểm tra file diemllm.json:")
        
#         if os.path.exists(PATH_DIEM_LLM):
#             try:
#                 with open(PATH_DIEM_LLM, 'r', encoding='utf-8') as f:
#                     raw_content = f.read()
#                 print(f"📄 File size: {len(raw_content)} ký tự")
#                 print(f"📄 500 ký tự đầu:")
#                 print(raw_content[:500])
#             except Exception as e:
#                 print(f"❌ Không thể đọc file: {e}")
#         else:
#             print("❌ File không tồn tại!")