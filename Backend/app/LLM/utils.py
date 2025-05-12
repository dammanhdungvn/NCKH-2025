# utils.py
import json

def get_khaosat_data_from_file(path_khaosat):
    try:
        with open(path_khaosat, 'r', encoding='utf-8') as f:
            khaosat_data_list = json.load(f)
        return khaosat_data_list[0] if isinstance(khaosat_data_list, list) and khaosat_data_list else {}
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
    try:
        with open(path_diem, 'r', encoding='utf-8') as f:
            diem_data_full = json.load(f)
        all_subjects = []
        if diem_data_full and "data" in diem_data_full and "ds_diem_hocky" in diem_data_full["data"]:
            for hocky in diem_data_full["data"]["ds_diem_hocky"]:
                if "ds_diem_mon_hoc" in hocky:
                    for mon_hoc in hocky["ds_diem_mon_hoc"]:
                        diem_tk_so_str = str(mon_hoc.get("diem_tk_so", "0")).replace(',', '.')
                        try:
                            diem_tk_so_float = float(diem_tk_so_str)
                        except ValueError:
                            diem_tk_so_float = 0.0
                        all_subjects.append({
                            "ten_mon": mon_hoc.get("ten_mon"),
                            "diem_tk_so": diem_tk_so_float,
                            "diem_tk_chu": mon_hoc.get("diem_tk_chu"),
                            "so_tin_chi": mon_hoc.get("so_tin_chi")
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