# utils.py
import json

def get_khaosat_data_from_file(path_khaosat):
    """
    Đọc dữ liệu khảo sát từ file JSON.
    
    Args:
        path_khaosat (str): Đường dẫn đến file JSON chứa dữ liệu khảo sát
        
    Returns:
        dict: Dữ liệu khảo sát của sinh viên đầu tiên hoặc dict rỗng nếu có lỗi
    """
    try:
        with open(path_khaosat, 'r', encoding='utf-8') as f:
            khaosat_data_list = json.load(f)
            
        # Trả về dữ liệu sinh viên đầu tiên nếu có
        if isinstance(khaosat_data_list, list) and khaosat_data_list:
            return khaosat_data_list[0]
        elif isinstance(khaosat_data_list, dict):
            return khaosat_data_list
        else:
            print(f"Cảnh báo: File {path_khaosat} không chứa dữ liệu hợp lệ.")
            return {}
            
    except FileNotFoundError:
        print(f"Lỗi: File {path_khaosat} không tìm thấy. Hãy đảm bảo file tồn tại và đường dẫn đúng.")
        return {}
    except json.JSONDecodeError:
        print(f"Lỗi: File {path_khaosat} không đúng định dạng JSON.")
        return {}
    except Exception as e:
        print(f"Lỗi không xác định khi đọc {path_khaosat}: {e}")
        return {}

def get_diem_data_from_file(path_diem):
    """
    Đọc dữ liệu điểm từ file JSON simplified và trả về danh sách tất cả môn học.
    
    Args:
        path_diem (str): Đường dẫn đến file JSON
        
    Returns:
        list: Danh sách các môn học với ten_mon và diem_tk_chu
    """
    try:
        with open(path_diem, 'r', encoding='utf-8') as f:
            diem_data_full = json.load(f)
            
        all_subjects = []
        if diem_data_full and "data" in diem_data_full and "ds_diem_hocky" in diem_data_full["data"]:
            for hocky in diem_data_full["data"]["ds_diem_hocky"]:
                if "ds_diem_mon_hoc" in hocky:
                    for mon_hoc in hocky["ds_diem_mon_hoc"]:
                        # File simplified chỉ có ten_mon và diem_tk_chu
                        if mon_hoc.get("ten_mon") and mon_hoc.get("diem_tk_chu"):
                            all_subjects.append({
                                "ten_mon": mon_hoc.get("ten_mon"),
                                "diem_tk_chu": mon_hoc.get("diem_tk_chu")
                            })
        return all_subjects
        
    except FileNotFoundError:
        print(f"Lỗi: File {path_diem} không tìm thấy. Hãy đảm bảo file tồn tại và đường dẫn đúng.")
        return []
    except json.JSONDecodeError:
        print(f"Lỗi: File {path_diem} không đúng định dạng JSON.")
        return []
    except Exception as e:
        print(f"Lỗi không xác định khi đọc {path_diem}: {e}")
        return []

