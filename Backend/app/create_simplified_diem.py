import json
import os
import re

def extract_year_semester_for_sorting(ten_hoc_ky):
    """
    Trích xuất năm và học kỳ để sắp xếp từ cũ đến mới.
    
    Args:
        ten_hoc_ky (str): Tên học kỳ như "Học kỳ 1 - Năm học 2022 - 2023"
        
    Returns:
        tuple: (năm, học kỳ) để sắp xếp
    """
    if not ten_hoc_ky:
        return (0, 0)
    
    match_hk = re.search(r'Học kỳ\s*(\d+)', ten_hoc_ky)
    match_year = re.search(r'Năm học\s*(\d{4})', ten_hoc_ky)
    
    if match_hk and match_year:
        return (int(match_year.group(1)), int(match_hk.group(1)))
    return (0, 0)

def clean_dtb_tich_luy_he_4(value):
    """
    Làm sạch giá trị điểm tích lũy hệ 4.
    
    Args:
        value (str): Giá trị như "3.20-Điểm"
        
    Returns:
        str: Giá trị đã làm sạch như "3.20"
    """
    if not value:
        return ""
    
    # Loại bỏ "-Điểm" nếu có
    cleaned = str(value).replace("-Điểm", "").strip()
    return cleaned

def create_simplified_diem_json(input_path, output_path):
    """
    Đọc file diem.json gốc và tạo file JSON đơn giản hóa.
    
    Args:
        input_path (str): Đường dẫn đến file diem.json gốc
        output_path (str): Đường dẫn để lưu file JSON đơn giản hóa
        
    Returns:
        tuple: (bool, str) - (Thành công hay không, Thông báo)
    """
    try:
        # Kiểm tra file đầu vào có tồn tại không
        if not os.path.exists(input_path):
            return False, f"File không tồn tại: {input_path}"
        
        # Đọc file JSON gốc
        with open(input_path, 'r', encoding='utf-8') as f:
            original_data = json.load(f)
        
        # Kiểm tra cấu trúc dữ liệu
        if 'data' not in original_data or 'ds_diem_hocky' not in original_data['data']:
            return False, "Cấu trúc dữ liệu không hợp lệ"
        
        # Trích xuất và đơn giản hóa dữ liệu
        simplified_semesters = []
        
        for semester in original_data['data']['ds_diem_hocky']:
            # Tạo đối tượng học kỳ đơn giản - chỉ giữ các trường cần thiết
            simplified_semester = {
                "ten_hoc_ky": semester.get("ten_hoc_ky", ""),
                "dtb_tich_luy_he_4": clean_dtb_tich_luy_he_4(semester.get("dtb_tich_luy_he_4", "")),
                "ds_diem_mon_hoc": []
            }
            
            # Trích xuất thông tin môn học - chỉ giữ các trường cần thiết
            for mon_hoc in semester.get("ds_diem_mon_hoc", []):
                # Kiểm tra môn học có đủ thông tin không (chỉ cần tên môn và điểm chữ)
                if (mon_hoc.get("ten_mon") and 
                    mon_hoc.get("diem_tk_chu")):
                    
                    simplified_mon_hoc = {
                        "ten_mon": str(mon_hoc.get("ten_mon", "")),
                        "diem_tk_chu": str(mon_hoc.get("diem_tk_chu", ""))
                    }
                    simplified_semester["ds_diem_mon_hoc"].append(simplified_mon_hoc)
            
            simplified_semesters.append(simplified_semester)
        
        # Sắp xếp từ cũ đến mới (học kỳ đầu tiên đến hiện tại)
        simplified_semesters.sort(key=lambda s: extract_year_semester_for_sorting(s["ten_hoc_ky"]))
        
        # Tạo cấu trúc JSON đơn giản hóa (chỉ chứa data, không có metadata)
        simplified_data = {
            "data": {
                "ds_diem_hocky": simplified_semesters
            }
        }
        
        # Đảm bảo thư mục đầu ra tồn tại
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
        
        # Lưu file JSON đơn giản hóa
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(simplified_data, f, ensure_ascii=False, indent=4)
        
        print(f"✅ Đã tạo file điểm đơn giản hóa thành công!")
        print(f"📁 File gốc: {input_path}")
        print(f"📁 File đơn giản: {output_path}")
        print(f"📊 Số học kỳ: {len(simplified_semesters)}")
        
        # In thống kê môn học
        total_subjects = sum(len(s["ds_diem_mon_hoc"]) for s in simplified_semesters)
        print(f"📚 Tổng số môn học: {total_subjects}")
        
        return True, "File đã được tạo thành công"
        
    except json.JSONDecodeError as e:
        return False, f"Lỗi định dạng JSON: {str(e)}"
    except Exception as e:
        return False, f"Lỗi khi xử lý file: {str(e)}"

def main():
    """
    Hàm chính để test chức năng tạo file đơn giản hóa.
    """
    # Đường dẫn file - sửa để trỏ đúng thư mục Database ngang hàng với Backend
    input_file = os.path.join('..', '..', 'Database', 'diem.json')
    output_file = os.path.join('..', '..', 'Database', 'diem_simplified.json')
    
    # Tạo file đơn giản hóa
    success, message = create_simplified_diem_json(input_file, output_file)
    
    if success:
        print(f"✅ {message}")
    else:
        print(f"❌ Lỗi: {message}")

if __name__ == "__main__":
    main()