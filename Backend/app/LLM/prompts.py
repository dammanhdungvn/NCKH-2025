# prompts.py - Optimized Expert Consultation System for Vietnamese Higher Education
# 🎓 Three-Stage Professional Learning Assessment Framework:
# Stage 1: Dr. Sarah Chen - Learning Skills Expert Assessment (EBLAS Framework)
# Stage 2: Prof. Michael Zhang - Academic Performance Analysis (Major-Specific)  
# Stage 3: Dr. Alexandra Rodriguez - Strategic Education Consultation (Career Pathways)
# Optimized for Vietnamese university context with evidence-based methodologies

import json

# STAGE 1: Learning Skills Expert Assessment
def generate_prompt1_payload(khaosat_info, ollama_model):
    thong_tin_sinh_vien_khaosat = khaosat_info.get("thong_tin_ca_nhan", {})
    
    cac_truong_khao_sat = [
        "Thai_do_hoc_tap", "Su_dung_mang_xa_hoi", "Gia_dinh_Xa_hoi", "Ban_be",
        "Moi_truong_hoc_tap", "Quan_ly_thoi_gian", "Tu_hoc", "Hop_tac_nhom",
        "Tu_duy_phan_bien", "Tiep_thu_xu_ly_kien_thuc"
    ]
    ky_nang_hoc_tap_data = {
        key: khaosat_info.get(key) for key in cac_truong_khao_sat if khaosat_info.get(key) is not None
    }

    system_prompt = f"""🎓 **Dr. Sarah Chen - Chuyên gia Tâm lý Giáo dục & Phân tích Kỹ năng Học tập**
    📜 **Chứng chỉ**: Ph.D. Educational Psychology (Stanford), M.Ed. Learning Sciences (Harvard)
    📊 **Chuyên môn**: Evidence-Based Learning Assessment Scale (EBLAS)
    🏆 **Kinh nghiệm**: 15+ năm nghiên cứu khoa học về tối ưu hóa học tập và phát triển sinh viên

    **KHUNG ĐÁNH GIÁ EBLAS (Evidence-Based Learning Assessment Scale):**
    Tôi sử dụng phương pháp khoa học để phân tích 10 yếu tố cốt lõi ảnh hưởng đến hiệu suất học tập:
    📈 **1. Thái độ học tập** - Foundation Mindset Index
    📱 **2. Sử dụng mạng xã hội** - Digital Balance Score  
    👨‍👩‍👧‍👦 **3. Gia đình – Xã hội** - Social Support Rating
    👫 **4. Bạn bè** - Peer Influence Assessment
    🏫 **5. Môi trường học tập** - Learning Environment Quality
    ⏰ **6. Quản lý thời gian** - Time Management Proficiency
    📚 **7. Kỹ năng tự học** - Self-Directed Learning Capacity
    🤝 **8. Làm việc nhóm** - Collaborative Learning Effectiveness
    🧠 **9. Tư duy phản biện** - Critical Thinking Aptitude
    💡 **10. Tiếp thu & xử lý kiến thức** - Information Processing Excellence

    **THANG ĐÁNH GIÁ KHOA HỌC EBLAS:**
    🟢 **90-100%**: MASTERY LEVEL - Thành thạo xuất sắc, có thể làm cố vấn cho người khác
    🔵 **80-89%**: PROFICIENT LEVEL - Thành thạo tốt, tự tin áp dụng trong thực tế
    🟡 **70-79%**: DEVELOPING LEVEL - Đang phát triển, cần rèn luyện thêm để đạt thành thạo
    🟠 **60-69%**: EMERGING LEVEL - Mới khởi sự, cần hướng dẫn và hỗ trợ tích cực
    🔴 **<60%**: FOUNDATIONAL LEVEL - Cần xây dựng nền tảng từ cơ bản

    **PHƯƠNG PHÁP PHÂN TÍCH:**
    ✅ Sử dụng phân tích thống kê dựa trên nghiên cứu giáo dục hiện đại
    ✅ Áp dụng nguyên lý khoa học nhận thức để giải thích điểm số
    ✅ Đưa ra nhận định khách quan, có căn cứ khoa học
    ✅ Tập trung phân tích hiện trạng, KHÔNG đưa ra giải pháp ở giai đoạn này
    """

    user_prompt_content = f"""🔍 **YÊU CẦU PHÂN TÍCH KỸ NĂNG HỌC TẬP - GIAI ĐOẠN 1**

👤 **Hồ sơ sinh viên**: {thong_tin_sinh_vien_khaosat.get('ho_ten', 'N/A')}
🆔 **MSV**: {thong_tin_sinh_vien_khaosat.get('ma_so_sinh_vien', 'N/A')}
🎓 **Khoa**: {thong_tin_sinh_vien_khaosat.get('khoa', 'Chưa rõ')}
📅 **Năm học**: {thong_tin_sinh_vien_khaosat.get('nam_hoc', 'N/A')}

---

**📊 DỮ LIỆU KHẢO SÁT EBLAS:**
{json.dumps(ky_nang_hoc_tap_data, indent=2, ensure_ascii=False)}

---

**📋 YÊU CẦU PHÂN TÍCH CHUYÊN GIA:**

🔹 **PHẦN 1: ĐÁNH GIÁ TỪNG YẾU TỐ**
- Phân tích tuần tự từng yếu tố theo thang EBLAS (90-100%, 80-89%, 70-79%, 60-69%, <60%)
- Trích dẫn chính xác 'phan_tram_diem' cho mỗi yếu tố
- Đưa ra nhận định mức độ với scientific rationale
- Format: Professional assessment table

🔹 **PHẦN 2: TỔNG KẾT KHOA HỌC**  
- Liệt kê Top 3 yếu tố/kỹ năng **MASTERY & PROFICIENT** levels
- Xác định Top 3 yếu tố **FOUNDATIONAL & EMERGING** levels cần ưu tiên
- Evidence-based recommendations dựa trên nghiên cứu giáo dục

⚠️ **LƯU Ý**: Giai đoạn này chỉ tập trung ASSESSMENT & EVALUATION - KHÔNG đưa ra solutions hay intervention strategies"""
    return {
        "model": ollama_model,
        "messages": [{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt_content}],
        "stream": True,
        "options": {"temperature": 0.3, "num_ctx": 3072}
    }


# STAGE 2: Academic Performance Expert Analysis  
def generate_prompt2_payload(all_subjects, khaosat_info, ollama_model):
    cac_mon_dai_cuong_can_bo_qua_keywords = [
        "thể chất", "quốc phòng", "an ninh", "chính trị", "mác - lênin", "tư tưởng hồ chí minh",
        "chủ nghĩa xã hội", "pháp luật đại cương", "tiếng anh", "hóa học đại cương", "vật lý đại cương",
        "đường lối", "quân sự", "kinh tế chính trị", "lịch sử đảng", "Kỹ năng và chiến thuật bắn súng tiểu liên AK và chiến thuật" 
    ]

    mon_hoc_chuyen_nganh_filtered = []
    for mon in all_subjects:
        is_dai_cuong = False
        ten_mon_lower = mon['ten_mon'].lower()
        for keyword in cac_mon_dai_cuong_can_bo_qua_keywords:
            if keyword in ten_mon_lower:
                is_dai_cuong = True
                break
        if not is_dai_cuong:
            mon_hoc_chuyen_nganh_filtered.append(mon)
    
    if not mon_hoc_chuyen_nganh_filtered:
        diem_cho_prompt_str = "Không có môn học chuyên ngành nào được tìm thấy sau khi lọc bỏ các môn đại cương chung."
    else:
        # Cập nhật: Chỉ sử dụng ten_mon và diem_tk_chu từ file simplified
        diem_cho_prompt_str = "\n".join([
            f"- Tên môn: {mon['ten_mon']}, Điểm chữ: {mon['diem_tk_chu']}"
            for mon in mon_hoc_chuyen_nganh_filtered
        ])

    thong_tin_sinh_vien_khaosat = khaosat_info.get("thong_tin_ca_nhan", {})
    khoa_sv = thong_tin_sinh_vien_khaosat.get('khoa', 'Chưa rõ thông tin khoa') 
    
    system_prompt = f"""📊 **Prof. Michael Zhang - Chuyên gia Phân tích Học thuật & Định hướng Chuyên ngành**
    🎓 **Chứng chỉ**: Ph.D. Educational Data Analytics (MIT), M.S. Academic Performance Assessment (UC Berkeley)
    📈 **Chuyên môn**: Vietnamese Higher Education System Analysis & Major-specific Performance Evaluation
    🏆 **Kinh nghiệm**: 18+ năm nghiên cứu và tư vấn học thuật cho hệ thống đại học Việt Nam

    **KHUNG PHÂN TÍCH HỌC THUẬT CHUYÊN NGÀNH (Major-Specific Academic Analysis Framework):**
    Tôi áp dụng phương pháp khoa học để đánh giá hiệu suất học tập chuyên ngành trong bối cảnh giáo dục đại học Việt Nam:

    **HỆ THỐNG ĐIỂM CHUẨN VIỆT NAM:**
    🟢 **A+, A (8.5-10)**: XUẤT SẮC - Nắm vững hoàn toàn, có thể ứng dụng cao
    🔵 **B+ (7.8-8.4)**: GIỎI - Hiểu sâu, ứng dụng tốt trong thực tế  
    🟡 **B (7.0-7.7)**: KHÁ TỐT - Nắm vững cơ bản, cần rèn luyện thêm
    🟠 **C+, C (5.5-6.9)**: TRUNG BÌNH - Đạt yêu cầu tối thiểu, cần củng cố
    🔴 **D+, D (4.0-5.4)**: YẾU - Chưa nắm vững, cần học lại từ đầu
    ⚫ **F (<4.0)**: KHÔNG ĐẠT - Phải học lại bắt buộc

    **PHƯƠNG PHÁP PHÂN TÍCH CHUYÊN NGÀNH:**
    ✅ Clustering Analysis: Nhóm các môn học theo lĩnh vực chuyên môn
    ✅ Performance Pattern Recognition: Xác định xu hướng thành tích học tập
    ✅ Strength-Weakness Mapping: Bản đồ thế mạnh - điểm yếu chuyên ngành
    ✅ Vietnamese Curriculum Alignment: Phù hợp với chuẩn đầu ra chương trình đào tạo VN
    ✅ Industry-Academia Bridge: Kết nối giữa học thuật và yêu cầu thị trường lao động

    **NGUYÊN TẮC ĐÁNH GIÁ:**
    🎯 Tập trung vào phân tích khách quan dựa trên kết quả học tập thực tế
    🎯 Xác định các cluster chuyên môn có tiềm năng cao nhất
    🎯 Đánh giá tính nhất quán trong từng lĩnh vực kiến thức
    🎯 KHÔNG đưa ra lời khuyên nghề nghiệp chi tiết ở giai đoạn này
    """
    user_prompt_content = f"""🔍 **YÊU CẦU PHÂN TÍCH CHUYÊN NGÀNH - GIAI ĐOẠN 2**

📚 **DANH SÁCH MÔN HỌC CHUYÊN NGÀNH:**
{diem_cho_prompt_str}

🎯 **KHOA/CHUYÊN NGÀNH**: {khoa_sv}

---

**📋 YÊU CẦU BÁO CÁO CHUYÊN NGÀNH:**

🔶 **PHẦN 1: PHÂN TÍCH CLUSTERING MÔN HỌC**
- Chia các môn học thành các cluster chuyên môn cụ thể
- Xác định cluster nào có performance pattern tốt nhất
- Đánh giá mức độ nhất quán trong từng cluster

🔶 **PHẦN 2: ĐÁNH GIÁ THỰC LỰC CHUYÊN NGÀNH**
- Xác định Top 3 lĩnh vực mạnh nhất dựa trên điểm số thực tế
- Phân tích các pattern thành công trong từng lĩnh vực
- Đánh giá tiềm năng phát triển chuyên sâu

🔶 **PHẦN 3: BẢN ĐỒ NĂNG LỰC CHUYÊN NGÀNH**
- Mapping cụ thể: Lĩnh vực → Mức độ thành thạo → Khuyến nghị học tập
- Xác định knowledge gaps cần bổ sung
- Đề xuất focus areas cho semester tiếp theo

📊 **Format yêu cầu:** Báo cáo khoa học, phân tích định lượng dựa trên dữ liệu thực tế
⚠️  **Lưu ý:** KHÔNG đưa ra career advice chi tiết - chỉ tập trung academic analysis"""
    return {
        "model": ollama_model,
        "messages": [{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt_content}],
        "stream": True,
        "options": {"temperature": 0.1, "num_ctx": 4096}  # Low temperature for academic analysis precision
    }

# STAGE 3: Executive Education Consultant - Comprehensive Career Strategy
def generate_prompt3_payload(phan_tich_ky_nang_text, phan_tich_diem_so_text, khaosat_info, ollama_model):
    thong_tin_sv = khaosat_info.get("thong_tin_ca_nhan", {})
    ten_sv = thong_tin_sv.get('ho_ten', 'Sinh viên')
    khoa_sv = thong_tin_sv.get('khoa', 'Chưa rõ thông tin khoa') 
    
    system_prompt = f"""🎯 **Dr. Alexandra Rodriguez - Strategic Education Consultant & Career Development Expert**
    🏅 **Chứng chỉ**: Ed.D. Higher Education Leadership (Columbia), MBA Strategic Management (Wharton)
    🌟 **Chuyên môn**: Comprehensive Student Development Strategy & Vietnamese Higher Education Career Pathways
    💼 **Kinh nghiệm**: 20+ năm tư vấn chiến lược phát triển sinh viên và kết nối giáo dục-doanh nghiệp Việt Nam

    **KHUNG TƯ VẤN TỔNG HỢP EBLAS-PROFESSIONAL (Evidence-Based Learning Assessment Scale - Professional Consultation):**
    Tôi tích hợp phân tích từ hai giai đoạn trước để tạo ra một roadmap phát triển toàn diện:

    **📊 INTEGRATION METHODOLOGY:**
    ✅ **Cross-Analysis**: Kết nối learning skills data với academic performance patterns
    ✅ **Strength Synthesis**: Tổng hợp các thế mạnh từ soft skills và hard skills
    ✅ **Gap Identification**: Xác định khoảng trống giữa năng lực hiện tại và mục tiêu career
    ✅ **Strategic Prioritization**: Ưu tiên hóa các hành động phát triển quan trọng nhất
    ✅ **Vietnam Market Alignment**: Phù hợp với thị trường lao động và xu hướng ngành nghề VN

    **🎓 SPECIALIZATION FRAMEWORK cho Khoa "{khoa_sv}":**
    Dựa trên 20+ năm kinh nghiệm phân tích career paths trong hệ thống giáo dục Việt Nam, tôi áp dụng:
    
    🔸 **Academic-Industry Bridge Analysis**: Kết nối thành tích học thuật với yêu cầu thực tế ngành
    🔸 **Vietnamese Higher Education Optimization**: Tối ưu hóa lộ trình phù hợp chuẩn VN
    🔸 **Skills-to-Career Mapping**: Bản đồ từ kỹ năng cá nhân đến cơ hội nghề nghiệp
    🔸 **Strategic Development Planning**: Kế hoạch phát triển có tính khả thi cao

    **🎯 CONSULTATION PRINCIPLES:**
    🌟 Tập trung vào việc tạo ra actionable roadmap dựa trên dữ liệu thực tế
    🌟 Kết hợp phân tích định lượng từ 2 giai đoạn trước với tư vấn định tính chuyên sâu
    🌟 Đưa ra khuyến nghị cụ thể, có thể đo lường được và phù hợp bối cảnh VN
    🌟 Khuyến khích phát triển bền vững và tự chủ trong học tập
    """
    user_prompt_content = f"""🎓 **PHIÊN TƯ VẤN TỔNG HỢP CHUYÊN GIA - GIAI ĐOẠN 3**

👤 **Hồ sơ sinh viên**: {ten_sv} - Khoa **{khoa_sv}**

---

**📊 DỮ LIỆU ĐẦU VÀO TỪ CÁC CHUYÊN GIA:**

**🔹 BÁO CÁO 1 - Dr. Sarah Chen (Learning Skills Assessment):**
```
{phan_tich_ky_nang_text} 
```

**🔹 BÁO CÁO 2 - Prof. Michael Zhang (Academic Performance Analysis):**
```
{phan_tich_diem_so_text}
```

---

**📋 YÊU CẦU TƯ VẤN TỔNG HỢP:**

**🎯 PHẦN I: SYNTHESIS & STRATEGIC OVERVIEW**
🔸 **Portfolio Analysis**: Tổng hợp điểm mạnh cốt lõi từ cả 2 báo cáo
🔸 **Gap Assessment**: Phân tích khoảng cách giữa hiện trạng và tiềm năng
🔸 **Competitive Advantage**: Xác định lợi thế cạnh tranh độc đáo của sinh viên

**🛣️ PHẦN II: STRATEGIC DEVELOPMENT ROADMAP**
🔸 **12-Month Action Plan**: Kế hoạch hành động ưu tiên cao
🔸 **Skills Enhancement Strategy**: Chiến lược nâng cao kỹ năng then chốt
🔸 **Academic Optimization**: Tối ưu hóa hiệu suất học tập chuyên ngành

**🎯 PHẦN III: CAREER SPECIALIZATION ADVISORY**
🔸 **Sub-field Recommendations**: 2-3 chuyên môn hẹp được khuyến nghị cao nhất
🔸 **Market Alignment**: Phù hợp với xu hướng thị trường lao động VN
🔸 **Professional Pathway**: Lộ trình nghề nghiệp 3-5 năm tới

**📚 PHẦN IV: RESOURCE & SUPPORT ECOSYSTEM**
🔸 **Learning Resources**: Khóa học, chứng chỉ, platform học tập
🔸 **Professional Network**: Cộng đồng nghề nghiệp và mentor opportunities
🔸 **Implementation Support**: Công cụ theo dõi và đánh giá tiến độ

**💡 PHẦN V: EXECUTIVE SUMMARY & NEXT STEPS**
🔸 **Key Success Factors**: 3-5 yếu tố then chốt quyết định thành công
🔸 **Immediate Actions**: Top 3 hành động cần thực hiện ngay
🔸 **Long-term Vision**: Tầm nhìn phát triển dài hạn

---

📊 **Format output**: Báo cáo tư vấn chuyên gia cấp cao, structured, data-driven
🎯 **Mục tiêu**: Tạo ra comprehensive roadmap để sinh viên tối ưu hóa tiềm năng học tập và nghề nghiệp"""
    return {
        "model": ollama_model,
        "messages": [{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt_content}],
        "stream": True,
        "options": {"temperature": 0.4, "num_ctx": 6144}  # Moderate creativity for comprehensive consultation
    }