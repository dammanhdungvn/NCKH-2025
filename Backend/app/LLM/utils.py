"""
Utility functions for data processing in the LLM module.
This module provides functions to read and process survey and grade data from JSON files.
"""

import json
import os
from typing import Dict, List, Any, Optional


def get_khaosat_data_from_file(path_khaosat: str) -> Optional[Dict[str, Any]]:
    """
    Read survey data from JSON file.
    
    Args:
        path_khaosat (str): Path to the survey data JSON file
        
    Returns:
        Optional[Dict[str, Any]]: Survey data dictionary or None if error occurs
    """
    try:
        if not os.path.exists(path_khaosat):
            print(f"Error: File {path_khaosat} not found.")
            return None
            
        with open(path_khaosat, 'r', encoding='utf-8') as f:
            khaosat_data_list = json.load(f)
            
        if not isinstance(khaosat_data_list, list) or not khaosat_data_list:
            print(f"Warning: Survey data file {path_khaosat} is empty or not a list.")
            return None
            
        return khaosat_data_list[0]
        
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON format in file {path_khaosat}: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error reading {path_khaosat}: {e}")
        return None


def get_diem_data_from_file(path_diem: str) -> List[Dict[str, Any]]:
    """
    Read and process grade data from JSON file.
    
    Args:
        path_diem (str): Path to the grade data JSON file
        
    Returns:
        List[Dict[str, Any]]: List of processed subject data with grades
    """
    try:
        if not os.path.exists(path_diem):
            print(f"Error: File {path_diem} not found.")
            return []
            
        with open(path_diem, 'r', encoding='utf-8') as f:
            diem_data_full = json.load(f)
            
        all_subjects = []
        
        # Validate data structure
        if not diem_data_full or "data" not in diem_data_full:
            print(f"Warning: Invalid data structure in {path_diem}")
            return []
            
        data_section = diem_data_full["data"]
        if "ds_diem_hocky" not in data_section:
            print(f"Warning: No semester data found in {path_diem}")
            return []
            
        # Process each semester
        for hocky in data_section["ds_diem_hocky"]:
            if "ds_diem_mon_hoc" not in hocky:
                continue
                
            # Process each subject in the semester
            for mon_hoc in hocky["ds_diem_mon_hoc"]:
                processed_subject = _process_subject_data(mon_hoc)
                if processed_subject:
                    all_subjects.append(processed_subject)
                    
        return all_subjects
        
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON format in file {path_diem}: {e}")
        return []
    except Exception as e:
        print(f"Unexpected error reading {path_diem}: {e}")
        return []


def _process_subject_data(mon_hoc: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Process individual subject data.
    
    Args:
        mon_hoc (Dict[str, Any]): Raw subject data
        
    Returns:
        Optional[Dict[str, Any]]: Processed subject data or None if invalid
    """
    try:
        # Convert grade to float
        diem_tk_so_str = str(mon_hoc.get("diem_tk_so", "0")).replace(',', '.')
        
        try:
            diem_tk_so_float = float(diem_tk_so_str)
        except ValueError:
            print(f"Warning: Invalid grade format '{diem_tk_so_str}' for subject {mon_hoc.get('ten_mon', 'Unknown')}")
            diem_tk_so_float = 0.0
            
        return {
            "ten_mon": mon_hoc.get("ten_mon", ""),
            "diem_tk_so": diem_tk_so_float,
            "diem_tk_chu": mon_hoc.get("diem_tk_chu", ""),
            "so_tin_chi": mon_hoc.get("so_tin_chi", "")
        }
        
    except Exception as e:
        print(f"Error processing subject data: {e}")
        return None