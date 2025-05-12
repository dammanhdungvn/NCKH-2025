# prompts.py
import json

# generate_prompt1_payload (giữ nguyên như phiên bản trước)
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

    system_prompt = f"""Bạn là một chuyên gia phân tích giáo dục và tâm lý học tập, nhiệm vụ của bạn là đánh giá chi tiết và khách quan các yếu tố và kỹ năng học tập của sinh viên dựa trên dữ liệu khảo sát được cung cấp.

    **QUY TẮC PHÂN TÍCH VÀ ĐÁNH GIÁ (TUÂN THỦ NGHIÊM NGẶT):**
    1.  **Thang đánh giá mức độ (dựa trên 'phan_tram_diem' của mỗi mục):**
        * 80% - 100%: **Rất Tốt/Thành thạo**. Cho thấy sinh viên làm chủ hoặc có điều kiện rất thuận lợi ở khía cạnh này.
        * 60% - 79%: **Tốt/Khá**. Sinh viên thể hiện ở mức độ ổn, có nền tảng nhưng có thể cải thiện thêm.
        * 40% - 59%: **Trung bình/Cần lưu ý**. Sinh viên đạt mức cơ bản, nhưng đây là yếu tố cần được chú ý để cải thiện.
        * Dưới 40%: **Yếu/Cần cải thiện đáng kể**. Đây là yếu tố sinh viên gặp khó khăn hoặc chưa đầu tư đúng mức, cần có sự thay đổi lớn.
    
    2.  **Nội dung phân tích cho từng yếu tố:**
        * Nêu rõ tên yếu tố.
        * Trích dẫn % điểm.
        * Đưa ra nhận định MỨC ĐỘ dựa trên thang đánh giá ở trên (ví dụ: "Rất Tốt", "Cần cải thiện đáng kể").
        * Giải thích ngắn gọn ý nghĩa của mức điểm đó đối với việc học tập của sinh viên trong thực tế liên quan đến yếu tố đó. KHÔNG đưa ra giải pháp hay đề xuất cải thiện chi tiết ở giai đoạn này.

    3.  **Yêu cầu chung:**
        * Sử dụng ngôn ngữ chuyên nghiệp, chính xác, khách quan.
        * Tập trung vào việc **đánh giá hiện trạng** dựa trên dữ liệu.
        * Trình bày kết quả theo từng mục đã được liệt kê trong dữ liệu khảo sát.
    """

    user_prompt_content = f"""
    Dưới đây là dữ liệu khảo sát về các yếu tố và kỹ năng học tập của sinh viên {thong_tin_sinh_vien_khaosat.get('ho_ten', 'N/A')}, mã sinh viên (MSV: {thong_tin_sinh_vien_khaosat.get('ma_so_sinh_vien', 'N/A')}), khoa {thong_tin_sinh_vien_khaosat.get('khoa', 'Chưa rõ')}, năm học {thong_tin_sinh_vien_khaosat.get('nam_hoc', 'N/A')}. 
    Dữ liệu bao gồm tên yếu tố/kỹ năng và 'phan_tram_diem' tương ứng:

    {json.dumps(ky_nang_hoc_tap_data, indent=2, ensure_ascii=False)}

    **YÊU CẦU PHÂN TÍCH:**
    Hãy phân tích và đánh giá **TUẦN TỰ TỪNG YẾU TỐ/KỸ NĂNG** có trong dữ liệu trên theo đúng QUY TẮC PHÂN TÍCH VÀ ĐÁNH GIÁ đã được nêu trong vai trò hệ thống của bạn. 
    Với mỗi yếu tố, hãy:
    a.  Nêu tên yếu tố.
    b.  Trích dẫn 'phan_tram_diem'.
    c.  Đưa ra nhận định về mức độ (ví dụ: "Rất Tốt", "Tốt/Khá", "Trung bình/Cần lưu ý", "Yếu/Cần cải thiện đáng kể").
    d.  Giải thích ngắn gọn ý nghĩa của mức điểm đó đối với sinh viên liên quan đến yếu tố đó.

    Sau khi phân tích tất cả các yếu tố, hãy đưa ra một **TỔNG KẾT NGẮN GỌN** về:
    1.  Ba (03) yếu tố/kỹ năng mà sinh viên thể hiện **tốt nhất** (dựa trên % điểm cao nhất và nhận định mức độ).
    2.  Ba (03) yếu tố/kỹ năng mà sinh viên **cần chú trọng cải thiện nhất** (dựa trên % điểm thấp nhất và nhận định mức độ).

    LƯU Ý QUAN TRỌNG: Ở giai đoạn này, chỉ tập trung PHÂN TÍCH VÀ ĐÁNH GIÁ. KHÔNG đưa ra bất kỳ đề xuất, giải pháp, hay kế hoạch cải thiện chi tiết nào.
    """
    return {
        "model": ollama_model,
        "messages": [{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt_content}],
        "stream": True,
        "options": {"temperature": 0.3, "num_ctx": 3072}
    }


# generate_prompt2_payload (giữ nguyên như phiên bản trước)
def generate_prompt2_payload(all_subjects, khaosat_info, ollama_model):
    cac_mon_dai_cuong_can_bo_qua_keywords = [
        "thể chất", "quốc phòng", "an ninh", "chính trị", "mác - lênin", "tư tưởng hồ chí minh",
        "chủ nghĩa xã hội", "pháp luật đại cương", "tiếng anh", "hóa học đại cương", "vật lý đại cương",
        "đường lối", "quân sự", "kinh tế chính trị", "lịch sử đảng", "nhập môn ngành" 
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
        diem_cho_prompt_str = "\n".join([
            f"- Tên môn: {mon['ten_mon']}, Điểm hệ 4: {mon['diem_tk_so']:.1f} (Điểm chữ: {mon['diem_tk_chu']}), Số tín chỉ: {mon['so_tin_chi']}"
            for mon in mon_hoc_chuyen_nganh_filtered
        ])

    thong_tin_sinh_vien_khaosat = khaosat_info.get("thong_tin_ca_nhan", {})
    khoa_sv = thong_tin_sinh_vien_khaosat.get('khoa', 'Chưa rõ thông tin khoa') 
    
    system_prompt = f"""Bạn là một chuyên gia phân tích học thuật có kinh nghiệm với nhiều ngành học khác nhau ở bậc đại học. 
    Nhiệm vụ của bạn là phân tích bảng điểm các môn học **CHUYÊN NGÀNH (đã được lọc sơ bộ)** của một sinh viên thuộc khoa "{khoa_sv}" để xác định các môn học/nhóm môn học thể hiện năng lực nổi bật và các lĩnh vực kiến thức tiềm năng của sinh viên đó trong chuyên ngành của họ.

    **QUY TẮC PHÂN TÍCH VÀ ĐÁNH GIÁ (TUÂN THỦ NGHIÊM NGẶT):**
    1.  **Đối tượng phân tích:** Tập trung vào danh sách các môn học được cung cấp.
    2.  **Đánh giá kết quả môn học (dựa trên Điểm hệ 4 và Điểm chữ):**
         * A - A+ (Thường từ 3.7 - 4.0): Xuất sắc.
        * B+ (Thường từ 3.0 - 3.6): Giỏi.
        * C+ - B (Thường từ 2.5 - 2.9): Khá.
        * C (Thường từ 2.0 - 2.5): Trung bình.
        * D - D+ (Thường từ 1.0 - 1.5): Yếu.
        * F (Dưới 1.0): Không đạt phải học lại môn.
    3.  **Xác định các lĩnh vực/nhóm môn học chuyên ngành nổi bật:** Dựa vào các môn học có kết quả tốt (ví dụ: từ B+ trở lên), hãy xác định và nhóm các môn có liên quan đến nhau để làm nổi bật các lĩnh vực kiến thức hoặc cụm chuyên môn mà sinh viên thể hiện tốt trong ngành học của mình (khoa "{khoa_sv}"). 
    4.  **Yêu cầu chung:** Tập trung vào việc **xác định các lĩnh vực học thuật mạnh**. KHÔNG đưa ra kế hoạch phát triển hay dự đoán nghề nghiệp chi tiết ở bước này.
    """
    user_prompt_content = f"""
    Sinh viên này thuộc khoa: **{khoa_sv}**.
    Dưới đây là bảng điểm các môn học được cho là thuộc chuyên ngành của sinh viên này:

    {diem_cho_prompt_str}

    **YÊU CẦU PHÂN TÍCH:**
    1.  **Liệt kê các môn học chuyên ngành có kết quả nổi bật:** (ví dụ: từ B+ trở lên hoặc điểm hệ 4 từ 3.2 trở lên).
    2.  **Xác định và nhóm các lĩnh vực kiến thức/cụm chuyên môn nổi bật:** Dựa trên các môn học có kết quả tốt, nhóm các môn có nội dung liên quan. Gọi tên các nhóm này theo hướng chuyên môn (ví dụ: "Lập trình và Phát triển ứng dụng", "Phân tích dữ liệu", "Mạng và Bảo mật", "Kinh tế lượng", "Quản trị Tài chính" tùy theo khoa "{khoa_sv}").
    3.  **Xác định các lĩnh vực chuyên ngành tiềm năng nhất:** Dựa trên sự phân nhóm, chỉ ra 1-3 lĩnh vực/cụm chuyên môn mà sinh viên này có năng lực học tập tốt nhất trong khoa "{khoa_sv}". Nêu rõ lý do.
    4.  **Nhận xét về những môn học chuyên ngành (nếu có) cần cải thiện:** (ví dụ: dưới C+ hoặc điểm hệ 4 dưới 2.5).

    LƯU Ý QUAN TRỌNG: Chỉ tập trung PHÂN TÍCH ĐIỂM SỐ CÁC MÔN CHUYÊN NGÀNH và XÁC ĐỊNH LĨNH VỰC HỌC THUẬT THẾ MẠNH.
    """
    return {
        "model": ollama_model,
        "messages": [{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt_content}],
        "stream": True,
        "options": {"temperature": 0.1, "num_ctx": 3072} 
    }

# generate_prompt3_payload (ĐÃ CẬP NHẬT ĐỂ NHẤN MẠNH ĐỀ XUẤT MẢNG NGÀNH)
def generate_prompt3_payload(phan_tich_ky_nang_text, phan_tich_diem_so_text, khaosat_info, ollama_model):
    thong_tin_sv = khaosat_info.get("thong_tin_ca_nhan", {})
    ten_sv = thong_tin_sv.get('ho_ten', 'Sinh viên')
    khoa_sv = thong_tin_sv.get('khoa', 'Chưa rõ thông tin khoa') 
    
    system_prompt = f"""Bạn là một chuyên gia tư vấn giáo dục và hướng nghiệp dày dặn kinh nghiệm, với vai trò xây dựng một "Hệ thống phân tích và đánh giá kỹ năng học tập của sinh viên". 
    Sinh viên này thuộc khoa "{khoa_sv}".
    Nhiệm vụ của bạn là tổng hợp thông tin từ hai báo cáo phân tích trước đó (Báo cáo 1: Kỹ năng học tập từ khảo sát; Báo cáo 2: Thế mạnh học thuật từ bảng điểm chuyên ngành của khoa "{khoa_sv}") để đưa ra một bản đánh giá tổng hợp, toàn diện và những đề xuất phát triển cụ thể, bao gồm cả việc định hướng các mảng chuyên môn hẹp mà sinh viên nên theo đuổi trong ngành học của mình.

    **QUY TẮC TƯ VẤN (TUÂN THỦ NGHIÊM NGẶT):**
    1.  **Tính tổng hợp và kết nối:** Phải liên kết chặt chẽ thông tin từ Báo cáo 1 và Báo cáo 2.
    2.  **Bằng chứng cụ thể:** Mọi nhận định và đề xuất phải dựa trên dữ liệu đã được phân tích từ hai báo cáo trước.
    3.  **Phù hợp với chuyên ngành:** Các đề xuất về học thuật, nghề nghiệp, khóa học, chứng chỉ và **đặc biệt là các mảng chuyên môn hẹp** phải phù hợp với chuyên ngành của sinh viên là khoa "{khoa_sv}" và các lĩnh vực thế mạnh đã được xác định từ Báo cáo 2, kết hợp với kỹ năng từ Báo cáo 1.
    4.  **Tính thực tế và khả thi:** Các đề xuất phải phù hợp với năng lực và điều kiện của sinh viên.
    5.  **Tính hệ thống:** Câu trả lời phải thể hiện một cái nhìn tổng thể về năng lực học tập của sinh viên.
    6.  **Không trùng lặp:** Không nhắc lại chi tiết phân tích đã có ở Báo cáo 1 và 2. Sử dụng kết luận từ các báo cáo đó.
    7.  **Ngôn ngữ:** Chuyên nghiệp, tích cực, khích lệ, và mang tính định hướng rõ ràng.
    """
    user_prompt_content = f"""
    Thông tin đầu vào cho việc xây dựng "Hệ thống phân tích và đánh giá kỹ năng học tập" cho sinh viên {ten_sv}, khoa **{khoa_sv}**:

    **Báo cáo 1: Tóm tắt Phân tích Kỹ năng Học tập từ Khảo sát**
    (Bao gồm nhận định mức độ và ý nghĩa của từng yếu tố: Thái độ học tập, Sử dụng mạng xã hội, Gia đình – Xã hội, Bạn bè, Môi trường học tập, Kỹ năng Quản lý thời gian, Kỹ năng tự học, Kỹ năng làm việc nhóm, Tư duy phản biện, Tiếp thu & xử lý kiến thức; cùng với 3 yếu tố tốt nhất và 3 yếu tố cần cải thiện nhất từ khảo sát).
    ```
    {phan_tich_ky_nang_text} 
    ```

    **Báo cáo 2: Tóm tắt Phân tích Thế mạnh Học thuật từ Bảng điểm Chuyên ngành (Khoa: {khoa_sv})**
    (Bao gồm các môn chuyên ngành nổi bật, các lĩnh vực/cụm chuyên môn tiềm năng dựa trên điểm số trong khoa "{khoa_sv}", và những môn chuyên ngành (nếu có) cần cải thiện).
    ```
    {phan_tich_diem_so_text}
    ```

    **YÊU CẦU XÂY DỰNG HỆ THỐNG ĐÁNH GIÁ VÀ ĐỀ XUẤT CHO SINH VIÊN (Khoa: {khoa_sv}):**
    Dựa trên việc **tổng hợp và kết nối thông tin** từ hai báo cáo trên, hãy cung cấp một bản đánh giá và đề xuất chi tiết, có cấu trúc như sau:

    **I. ĐÁNH GIÁ TỔNG QUAN VỀ NĂNG LỰC HỌC TẬP CỦA SINH VIÊN (Khoa: {khoa_sv}):**
        1.  **Điểm mạnh nổi bật tổng hợp:** Kết hợp kỹ năng vượt trội (Báo cáo 1) với lĩnh vực học thuật xuất sắc (Báo cáo 2) để chỉ ra thế mạnh toàn diện nhất của sinh viên.
        2.  **Những khía cạnh cần ưu tiên phát triển:** Kết hợp kỹ năng cần cải thiện (Báo cáo 1) với môn chuyên ngành cần cố gắng hơn (Báo cáo 2) để xác định lĩnh vực cần tập trung nỗ lực.
        3.  **Sự tương thích giữa Kỹ năng và Học thuật chuyên ngành ("{khoa_sv}"):** Phân tích xem các kỹ năng học tập hiện tại (Báo cáo 1) đang hỗ trợ hay cản trở việc học các lĩnh vực chuyên ngành (Báo cáo 2) như thế nào? Nêu ví dụ cụ thể.

    **II. ĐỀ XUẤT LỘ TRÌNH PHÁT TRIỂN KỸ NĂNG VÀ HỌC THUẬT (Phù hợp với Khoa "{khoa_sv}"):**
        1.  **Mục tiêu phát triển tổng thể (6-12 tháng):** Đề xuất 1-2 mục tiêu tổng thể.
        2.  **Kế hoạch hành động chi tiết cho các khía cạnh cần cải thiện:**
            * Với **MỖI kỹ năng cần cải thiện nhất** (từ Báo cáo 1 và I.2), đề xuất 2-3 hành động/phương pháp cụ thể.
            * Với **MỖI môn học chuyên ngành cần cải thiện** (từ Báo cáo 2 và I.2), gợi ý cách tiếp cận học tập hiệu quả.
        3.  **ĐỊNH HƯỚNG CHUYÊN MÔN SÂU (MẢNG NÊN THEO ĐUỔI TRONG NGÀNH):**
            * Dựa trên **sự kết hợp** giữa các lĩnh vực học thuật tiềm năng nhất (từ Báo cáo 2) và các kỹ năng mềm/tư duy nổi bật (từ Báo cáo 1), hãy **đề xuất 1-2 mảng chuyên môn hẹp (sub-fields/specializations) cụ thể** trong ngành học ("{khoa_sv}") mà sinh viên này có tiềm năng lớn nhất và nên tập trung theo đuổi. 
            * **Giải thích rõ ràng lý do** cho mỗi đề xuất mảng chuyên môn, chỉ ra sự phù hợp giữa điểm mạnh học thuật và các kỹ năng liên quan. (Ví dụ: "Với thế mạnh ở các môn Mạng máy tính, An ninh mạng cùng với kỹ năng Tư duy phản biện tốt, sinh viên nên cân nhắc theo đuổi chuyên sâu mảng An toàn thông tin (Security). Kỹ năng logic sẽ hỗ trợ tốt cho việc phân tích và giải quyết các vấn đề bảo mật phức tạp.")
            * Gợi ý các môn học chuyên sâu tự chọn (nếu có), chủ đề nghiên cứu/dự án cá nhân liên quan đến các mảng đề xuất này.

    **III. GỢI Ý TÀI NGUYÊN VÀ HỖ TRỢ PHÁT TRIỂN (Phù hợp với Khoa "{khoa_sv}" và định hướng đã đề xuất):**
        1.  **Khóa học/Chứng chỉ:** Đề xuất 2-3 khóa học online hoặc chứng chỉ nghề nghiệp PHÙ HỢP với các mảng chuyên môn hẹp đã đề xuất ở mục II.3.
        2.  **Nguồn tài liệu/ Cộng đồng:** Gợi ý 2-3 nguồn tài liệu hoặc cộng đồng liên quan.
        3.  **Hoạt động ngoại khóa/Thực tiễn:** Gợi ý các hoạt động phù hợp.

    **IV. KẾT LUẬN VÀ LỜI KHUYÊN ĐỘNG VIÊN:**
        * Tóm tắt những nhận định quan trọng nhất về tiềm năng của sinh viên.
        * Đưa ra lời khuyên cuối cùng để sinh viên tự tin, chủ động.

    Hãy đảm bảo câu trả lời khoa học, logic, dễ hiểu và hữu ích, và đi sâu vào từng khía cạnh để phân tích.
    """
    return {
        "model": ollama_model,
        "messages": [{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt_content}],
        "stream": True,
        "options": {"temperature": 0.5, "num_ctx": 4096} 
    }