"""
Excel to JSON converter for student grade data.
This module converts Excel grade files to structured JSON format for analysis.
"""

import pandas as pd
import json
import re
import os
from typing import Tuple, Dict, Any, Optional, List


# Constants
SEMESTER_PATTERN = r'Học kỳ\s*(\d+|I{1,3}|IV|V|Hè|Phụ)'
YEAR_PATTERN = r'Năm học\s*(\d{4})\s*-\s*(\d{4})'
COURSE_HEADER = ["Stt", "Mã MH", "Nhóm/tổ môn học", "Tên môn học", "Số tín chỉ",
                 "Điểm thi", "Điểm TK (10)", "Điểm TK (4)", "Điểm TK (C)", "Kết quả", "Chi tiết"]

# Semester code mapping
SEMESTER_CODE_MAP = {
    "1": "1", "I": "1",
    "2": "2", "II": "2", 
    "3": "3", "III": "3", "Hè": "3",
    "Phụ": "4"
}

# Field mapping for semester statistics
STATS_FIELD_MAPPING = {
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


def extract_hoc_ky_code(ten_hoc_ky_str: str) -> str:
    """
    Extract semester code from semester name string.
    
    Args:
        ten_hoc_ky_str (str): Semester name string
        
    Returns:
        str: Semester code in format "YYYYX" (year + semester number)
        
    Example:
        "Học kỳ 1 - Năm học 2022 - 2023" -> "20221"
    """
    if not ten_hoc_ky_str or pd.isna(ten_hoc_ky_str):
        return ""
    
    # Find semester and year using regex
    match_hk = re.search(SEMESTER_PATTERN, ten_hoc_ky_str, re.IGNORECASE)
    match_year = re.search(YEAR_PATTERN, ten_hoc_ky_str)

    if not match_hk or not match_year:
        print(f"Warning: Cannot extract semester code from '{ten_hoc_ky_str}'")
        return ""

    hk_part_str = match_hk.group(1).strip()
    year_part_str = match_year.group(1)

    # Map semester name to code
    hk_code_val = SEMESTER_CODE_MAP.get(
        hk_part_str, 
        hk_part_str if hk_part_str.isdigit() else "X"
    )
    
    return year_part_str + hk_code_val


def parse_summary_stats_from_line(line_content: str) -> Dict[str, str]:
    """
    Parse semester summary statistics from a line.
    
    Args:
        line_content (str): Line containing statistical information
        
    Returns:
        Dict[str, str]: Dictionary of parsed statistics
    """
    stats = {}
    
    if pd.isna(line_content) or not line_content.strip():
        return stats
    
    # Clean input string
    cleaned_line = line_content.strip()
    if cleaned_line.startswith("- "):
        cleaned_line = cleaned_line[2:]
    
    # Split key-value pairs
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
            
    # Convert field names using mapping
    for csv_key, json_key in STATS_FIELD_MAPPING.items():
        if csv_key in data_pairs:
            stats[json_key] = data_pairs[csv_key]
            
    return stats


def _create_semester_object(ten_hoc_ky: str, hoc_ky_code: str) -> Dict[str, Any]:
    """
    Create a new semester data object.
    
    Args:
        ten_hoc_ky (str): Semester name
        hoc_ky_code (str): Semester code
        
    Returns:
        Dict[str, Any]: Semester data structure
    """
    return {
        "loai_nganh": 1,
        "hoc_ky": hoc_ky_code,
        "ten_hoc_ky": ten_hoc_ky,
        "dtb_hk_he10": None,
        "dtb_hk_he4": None,
        "dtb_tich_luy_he_10": None,
        "dtb_tich_luy_he_4": None,
        "so_tin_chi_dat_hk": None,
        "so_tin_chi_dat_tich_luy": None,
        "diemrl_hk": None,
        "phan_loai_rl_hk": None,
        "hien_thi_tk_he_10": True,
        "hien_thi_tk_he_4": True,
        "xep_loai_tkb_hk": None,
        "ds_diem_mon_hoc": []
    }


def _create_course_object(row_values: List[str]) -> Optional[Dict[str, Any]]:
    """
    Create a course data object from row values.
    
    Args:
        row_values (List[str]): Row values from Excel
        
    Returns:
        Optional[Dict[str, Any]]: Course data object or None if invalid
    """
    if len(row_values) < 9:
        return None
        
    diem_tk_10 = row_values[6]
    diem_tk_4 = row_values[7]

    if not diem_tk_10 or not diem_tk_4:
        return None

    # Determine pass/fail status
    ket_qua_str = row_values[9] if len(row_values) > 9 else ""
    ket_qua = 0 if ket_qua_str.lower() in ["rớt", "fail", "trượt", "f"] else 1

    return {
        "chuyen_diem_ve_hoc_ky": "",
        "ma_mon": row_values[1],
        "ma_mon_tt": "",
        "nhom_to": row_values[2],
        "ten_mon": row_values[3],
        "ten_mon_eg": "",
        "mon_hoc_nganh": True,
        "so_tin_chi": row_values[4],
        "diem_thi": row_values[5],
        "diem_giua_ky": "",
        "diem_tk": diem_tk_10,
        "diem_tk_so": diem_tk_4,
        "diem_tk_chu": row_values[8],
        "ket_qua": ket_qua,
        "hien_thi_ket_qua": True,
        "loai_nganh": 1,
        "KhoaThi": 0,
        "khong_tinh_diem_tbtl": 0,
        "ly_do_khong_tinh_diem_tbtl": "",
        "ds_diem_thanh_phan": []
    }


def _process_excel_rows(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """
    Process Excel rows to extract semester and course data.
    
    Args:
        df (pd.DataFrame): Excel data as DataFrame
        
    Returns:
        List[Dict[str, Any]]: List of semester data
    """
    ds_diem_hocky = []
    current_semester_obj = None

    for idx, row_series in df.iterrows():
        row_values = [
            str(x).strip() if pd.notna(x) and x is not None else "" 
            for x in row_series
        ]
        first_cell = row_values[0]

        if not first_cell:
            continue

        # Process semester header
        if first_cell.startswith("Học kỳ"):
            current_ten_hoc_ky = first_cell.split(',')[0]
            current_hoc_ky_code = extract_hoc_ky_code(current_ten_hoc_ky)
            
            current_semester_obj = _create_semester_object(
                current_ten_hoc_ky, 
                current_hoc_ky_code
            )
            ds_diem_hocky.append(current_semester_obj)
            continue

        # Skip header row
        if row_values[:len(COURSE_HEADER)] == COURSE_HEADER:
            continue
            
        # Process course data
        if (current_semester_obj and 
            first_cell and 
            first_cell.isdigit() and 
            len(row_values) >= 9):
            
            course_obj = _create_course_object(row_values)
            if course_obj:
                current_semester_obj["ds_diem_mon_hoc"].append(course_obj)
            continue

        # Process summary statistics
        if (current_semester_obj and 
            first_cell.startswith("- Điểm trung bình học kỳ hệ 4")):
            
            parsed_stats = parse_summary_stats_from_line(first_cell)
            current_semester_obj.update(parsed_stats)
            continue
            
    return ds_diem_hocky


def convert_excel_to_json(excel_filepath: str, json_filepath: str) -> Tuple[bool, str]:
    """
    Main function to read Excel file, process data and export to JSON.
    
    Args:
        excel_filepath (str): Path to Excel file
        json_filepath (str): Path to save JSON file
        
    Returns:
        Tuple[bool, str]: (Success status, Message)
    """
    try:
        # Read Excel file
        df = pd.read_excel(
            excel_filepath, 
            sheet_name=0, 
            header=None, 
            names=range(25), 
            dtype=str
        )
    except FileNotFoundError:
        error_msg = f"Excel file not found: '{excel_filepath}'"
        print(f"Error: {error_msg}")
        return False, error_msg
    except Exception as e:
        error_msg = f"Error reading Excel file: {str(e)}"
        print(f"Error: {error_msg}")
        return False, error_msg

    try:
        # Process Excel data
        ds_diem_hocky = _process_excel_rows(df)
        
        # Sort semesters by year and semester (newest first)
        ds_diem_hocky.sort(key=lambda s: (
            s.get("hoc_ky", "00000")[:4],  # Year
            s.get("hoc_ky", "00000")[4:]   # Semester
        ), reverse=True)
        
        # Create final output structure
        final_output_data = {
            "data": {
                "total_items": len(ds_diem_hocky),
                "total_pages": 1,
                "is_kkbd": False,
                "ds_diem_hocky": ds_diem_hocky
            }
        }

        # Ensure output directory exists
        output_dir = os.path.dirname(json_filepath)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)

        # Save JSON file
        with open(json_filepath, 'w', encoding='utf-8') as f:
            json.dump(final_output_data, f, ensure_ascii=False, indent=4)
            
        return True, "File processed successfully"
        
    except Exception as e:
        error_msg = f"Error saving JSON file: {str(e)}"
        print(f"Error: {error_msg}")
        return False, error_msg 