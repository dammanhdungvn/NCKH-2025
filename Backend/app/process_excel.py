import pandas as pd
import json
import os
from datetime import datetime

def process_excel_to_json():
    try:
        # Read the Excel file
        excel_path = os.path.join('..', 'Database', 'diem.xlsx')
        df = pd.read_excel(excel_path)

        # Initialize the result structure
        result = {
            "data": {
                "total_items": 0,
                "total_pages": 1,
                "is_kkbd": False,
                "ds_diem_hocky": []
            }
        }

        # Process each semester
        current_semester = None
        semester_data = None

        for _, row in df.iterrows():
            # Extract semester information
            semester = str(row.get('hoc_ky', ''))
            if semester != current_semester:
                if semester_data:
                    result["data"]["ds_diem_hocky"].append(semester_data)
                
                current_semester = semester
                semester_data = {
                    "hoc_ky": semester,
                    "ten_hoc_ky": f"Học kỳ {semester[-1]} - Năm học {semester[:4]} - {int(semester[:4])+1}",
                    "so_tin_chi_dat_hk": str(row.get('so_tin_chi_dat_hk', '')),
                    "so_tin_chi_dat_tich_luy": str(row.get('so_tin_chi_dat_tich_luy', '')),
                    "diemrl_hk": str(row.get('diemrl_hk', '')),
                    "phan_loai_rl_hk": str(row.get('phan_loai_rl_hk', '')),
                    "hien_thi_tk_he_10": True,
                    "hien_thi_tk_he_4": True,
                    "ds_diem_mon_hoc": []
                }

                # Add semester-specific fields if they exist
                if 'dtb_hk_he10' in row:
                    semester_data.update({
                        "dtb_hk_he10": str(row.get('dtb_hk_he10', '')),
                        "dtb_hk_he4": str(row.get('dtb_hk_he4', '')),
                        "dtb_tich_luy_he_10": str(row.get('dtb_tich_luy_he_10', '')),
                        "dtb_tich_luy_he_4": str(row.get('dtb_tich_luy_he_4', '')),
                        "xep_loai_tkb_hk": str(row.get('xep_loai_tkb_hk', '')),
                        "loai_nganh": 1
                    })

            # Create course data
            course_data = {
                "chuyen_diem_ve_hoc_ky": "",
                "ma_mon": str(row.get('ma_mon', '')),
                "ma_mon_tt": "",
                "nhom_to": str(row.get('nhom_to', '')),
                "ten_mon": str(row.get('ten_mon', '')),
                "ten_mon_eg": str(row.get('ten_mon_eg', '')),
                "mon_hoc_nganh": True,
                "so_tin_chi": str(row.get('so_tin_chi', '')),
                "diem_thi": str(row.get('diem_thi', '')),
                "diem_giua_ky": str(row.get('diem_giua_ky', '')),
                "diem_tk": str(row.get('diem_tk', '')),
                "diem_tk_so": str(row.get('diem_tk_so', '')),
                "diem_tk_chu": str(row.get('diem_tk_chu', '')),
                "ket_qua": 1 if row.get('ket_qua', 0) == 1 else 0,
                "hien_thi_ket_qua": True,
                "loai_nganh": 1,
                "KhoaThi": 0,
                "khong_tinh_diem_tbtl": 1 if pd.isna(row.get('diem_tk', None)) else 0,
                "ly_do_khong_tinh_diem_tbtl": "Môn chưa nhập điểm" if pd.isna(row.get('diem_tk', None)) else "Môn cải thiện điểm" if row.get('ket_qua', 0) == 0 else "",
                "ds_diem_thanh_phan": []
            }

            # Process component scores if they exist
            component_scores = []
            for i in range(1, 14):  # Assuming max 13 components
                ky_hieu = row.get(f'ky_hieu_{i}')
                if pd.notna(ky_hieu):
                    component = {
                        "ky_hieu": str(ky_hieu),
                        "ten_thanh_phan": str(row.get(f'ten_thanh_phan_{i}', '')),
                        "trong_so": str(row.get(f'trong_so_{i}', '')),
                        "diem_thanh_phan": str(row.get(f'diem_thanh_phan_{i}', ''))
                    }
                    component_scores.append(component)
            
            if component_scores:
                course_data["ds_diem_thanh_phan"] = component_scores

            # Add course to semester
            semester_data["ds_diem_mon_hoc"].append(course_data)

        # Add the last semester
        if semester_data:
            result["data"]["ds_diem_hocky"].append(semester_data)

        # Update total items
        result["data"]["total_items"] = len(result["data"]["ds_diem_hocky"])

        # Save to JSON file
        json_path = os.path.join('..', 'Database', 'diem.json')
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=4)

        return True, "File processed successfully"

    except Exception as e:
        return False, f"Error processing file: {str(e)}"

if __name__ == "__main__":
    success, message = process_excel_to_json()
    print(message) 