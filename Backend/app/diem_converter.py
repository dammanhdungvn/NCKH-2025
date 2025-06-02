import pandas as pd
import json
import re
import os

def extract_hoc_ky_code(ten_hoc_ky_str):
    """
    Trích xuất mã học kỳ từ chuỗi tên học kỳ.
    Ví dụ: "Học kỳ 1 - Năm học 2022 - 2023" -> "20221"
    
    Args:
        ten_hoc_ky_str (str): Chuỗi chứa tên học kỳ
        
    Returns:
        str: Mã học kỳ dạng "YYYYX" (năm học + số học kỳ)
    """
    if not ten_hoc_ky_str or pd.isna(ten_hoc_ky_str):
        return ""
    
    # Tìm học kỳ và năm học bằng regex
    match_hk = re.search(r'Học kỳ\s*(\d+|I{1,3}|IV|V|Hè|Phụ)', ten_hoc_ky_str, re.IGNORECASE)
    match_year = re.search(r'Năm học\s*(\d{4})\s*-\s*(\d{4})', ten_hoc_ky_str)

    if not match_hk or not match_year:
        print(f"Cảnh báo: Không thể trích xuất mã học kỳ từ '{ten_hoc_ky_str}'")
        return "" 

    hk_part_str = match_hk.group(1).strip()
    year_part_str = match_year.group(1) 

    # Ánh xạ tên học kỳ sang mã số
    hk_code_map = {
        "1": "1", "I": "1",
        "2": "2", "II": "2",
        "3": "3", "III": "3", "Hè": "3", 
        "Phụ": "4" 
    }
    
    hk_code_val = hk_code_map.get(hk_part_str, hk_part_str if hk_part_str.isdigit() else "X")
    return year_part_str + hk_code_val

def parse_summary_stats_from_line(line_content):
    """
    Phân tích cú pháp một dòng chứa thống kê tổng hợp của học kỳ.
    
    Args:
        line_content (str): Dòng chứa thông tin thống kê
        
    Returns:
        dict: Dictionary chứa các thống kê đã được phân tích
    """
    stats = {}
    if pd.isna(line_content) or not line_content.strip():
        return stats
    
    # Xử lý chuỗi đầu vào
    cleaned_line = line_content.strip()
    if cleaned_line.startswith("- "):
        cleaned_line = cleaned_line[2:]
    
    # Tách các cặp key-value
    items = cleaned_line.split('- ')
    
    data_pairs = {}
    for item in items:
        if not item.strip():
            continue
        parts = item.split(':', 1)
        if len(parts) == 2:
            key = parts[0].strip()
            value = parts[1].strip().split(',')[0].split(' ')[0]
            data_pairs[key] = value
            
    # Ánh xạ tên trường CSV sang tên trường JSON
    mapping = {
        "Điểm trung bình học kỳ hệ 4": "dtb_hk_he4",
        "Điểm trung bình học kỳ hệ 10": "dtb_hk_he10",
        "Số tín chỉ đạt học kỳ": "so_tin_chi_dat_hk",
        "Điểm rèn luyện học kỳ": "diemrl_hk",
        "Xếp loại điểm rèn luyện": "phan_loai_rl_hk",
        "Điểm trung bình tích lũy hệ 4": "dtb_tich_luy_he_4",
        "Điểm trung bình tích lũy hệ 10": "dtb_tich_luy_he_10",
        "Số tín chỉ tích lũy": "so_tin_chi_dat_tich_luy",
        "Phân loại điểm trung bình HK": "xep_loai_tkb_hk"
    }
    
    # Chuyển đổi dữ liệu theo mapping
    for csv_key, json_key in mapping.items():
        if csv_key in data_pairs:
            stats[json_key] = data_pairs[csv_key]
    return stats

def convert_excel_to_json(excel_filepath, json_filepath):
    """
    Hàm chính để đọc tệp Excel, xử lý dữ liệu và xuất ra tệp JSON.
    
    Args:
        excel_filepath (str): Đường dẫn đến file Excel
        json_filepath (str): Đường dẫn để lưu file JSON
        
    Returns:
        tuple: (bool, str) - (Thành công hay không, Thông báo)
    """
    try:
        # Đọc file Excel
        df = pd.read_excel(excel_filepath, sheet_name=0, header=None, names=range(25), dtype=str)
    except FileNotFoundError:
        print(f"Lỗi: Không tìm thấy tệp Excel '{excel_filepath}'")
        return False, f"Không tìm thấy tệp Excel '{excel_filepath}'"
    except Exception as e:
        print(f"Lỗi khi đọc tệp Excel '{excel_filepath}': {e}")
        return False, f"Lỗi khi đọc tệp Excel: {str(e)}"

    # Khởi tạo danh sách điểm học kỳ
    ds_diem_hocky = []
    current_semester_obj = None
    course_data_header = ["Stt","Mã MH","Nhóm/tổ môn học","Tên môn học","Số tín chỉ","Điểm thi","Điểm TK (10)","Điểm TK (4)","Điểm TK (C)","Kết quả","Chi tiết"]

    # Xử lý từng dòng trong file Excel
    for idx, row_series in df.iterrows():
        row_values = [str(x).strip() if pd.notna(x) and x is not None else "" for x in row_series]
        first_cell = row_values[0]

        if not first_cell: 
            continue

        # Xử lý dòng chứa thông tin học kỳ
        if first_cell.startswith("Học kỳ"): 
            current_ten_hoc_ky = first_cell.split(',')[0] 
            current_hoc_ky_code = extract_hoc_ky_code(current_ten_hoc_ky)
            
            # Tạo đối tượng học kỳ mới
            current_semester_obj = {
                "loai_nganh": 1, "hoc_ky": current_hoc_ky_code, "ten_hoc_ky": current_ten_hoc_ky,
                "dtb_hk_he10": None, "dtb_hk_he4": None, 
                "dtb_tich_luy_he_10": None, "dtb_tich_luy_he_4": None, 
                "so_tin_chi_dat_hk": None, "so_tin_chi_dat_tich_luy": None,
                "diemrl_hk": None, "phan_loai_rl_hk": None,
                "hien_thi_tk_he_10": True, "hien_thi_tk_he_4": True, 
                "xep_loai_tkb_hk": None, "ds_diem_mon_hoc": [] 
            }
            ds_diem_hocky.append(current_semester_obj) 
            continue 

        # Bỏ qua dòng header
        if row_values[:len(course_data_header)] == course_data_header:
            continue
            
        # Xử lý dòng chứa điểm môn học
        if current_semester_obj and first_cell and first_cell.isdigit() and len(row_values) >= 9:
            diem_tk_10 = row_values[6]
            diem_tk_4 = row_values[7]

            if diem_tk_10 and diem_tk_4: 
                # Tạo đối tượng môn học
                mon_hoc = {
                    "chuyen_diem_ve_hoc_ky": "", "ma_mon": row_values[1], "ma_mon_tt": "",
                    "nhom_to": row_values[2], "ten_mon": row_values[3], "ten_mon_eg": "",
                    "mon_hoc_nganh": True, "so_tin_chi": row_values[4], "diem_thi": row_values[5],
                    "diem_giua_ky": "", "diem_tk": diem_tk_10, "diem_tk_so": diem_tk_4,
                    "diem_tk_chu": row_values[8],
                    "ket_qua": 1 if not row_values[9] else (0 if row_values[9].lower() in ["rớt", "fail", "trượt", "f"] else 1),
                    "hien_thi_ket_qua": True, "loai_nganh": 1, "KhoaThi": 0,
                    "khong_tinh_diem_tbtl": 0, 
                    "ly_do_khong_tinh_diem_tbtl": "", 
                    "ds_diem_thanh_phan": []
                }
                current_semester_obj["ds_diem_mon_hoc"].append(mon_hoc)
            continue 

        # Xử lý dòng chứa thống kê tổng hợp
        if current_semester_obj and first_cell.startswith("- Điểm trung bình học kỳ hệ 4"):
            parsed_stats = parse_summary_stats_from_line(first_cell)
            current_semester_obj.update(parsed_stats) 
            continue
            
    # Sắp xếp danh sách học kỳ theo năm và học kỳ
    ds_diem_hocky.sort(key=lambda s: (
        s.get("hoc_ky", "00000")[:4],  # Năm học
        s.get("hoc_ky", "00000")[4:]   # Học kỳ
    ), reverse=True) 
    
    # Tạo cấu trúc JSON đầu ra
    final_output_data = {
        "data": {
            "total_items": len(ds_diem_hocky),
            "total_pages": 1,
            "is_kkbd": False,
            "ds_diem_hocky": ds_diem_hocky
        }
    }

    try:
        # Đảm bảo thư mục đầu ra tồn tại
        output_dir = os.path.dirname(json_filepath)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)

        # Lưu file JSON
        with open(json_filepath, 'w', encoding='utf-8') as f:
            json.dump(final_output_data, f, ensure_ascii=False, indent=4)
        return True, "File processed successfully"
    except Exception as e:
        return False, f"Error saving JSON file: {str(e)}" 