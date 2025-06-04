"""
Configuration module for the student learning analytics system.
This module contains all configuration constants and settings.
"""

import os
from pathlib import Path

# --- Base Paths ---
BASE_DIR = Path(__file__).parent
DATABASE_DIR = BASE_DIR.parent / 'Database'
UPLOADS_DIR = DATABASE_DIR / 'uploads'

# --- File Paths ---
PATH_KHAOSAT = DATABASE_DIR / 'khaosat.json'
PATH_DIEM = DATABASE_DIR / 'diem.json'

# --- Ollama Configuration ---
OLLAMA_API_URL = os.getenv('OLLAMA_API_URL', 'http://192.168.2.114:11434/api/chat')
OLLAMA_MODEL = os.getenv('OLLAMA_MODEL', 'gemma2:2b')

# --- Flask Configuration ---
FLASK_HOST = os.getenv('FLASK_HOST', '0.0.0.0')
FLASK_PORT = int(os.getenv('FLASK_PORT', 5000))
FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'

# --- Survey Configuration ---
SURVEY_SECTIONS = {
    "I": {"name": "Thai_do_hoc_tap", "count": 5},
    "II": {"name": "Su_dung_mang_xa_hoi", "count": 5},
    "III": {"name": "Gia_dinh_Xa_hoi", "count": 5},
    "IV": {"name": "Ban_be", "count": 5},
    "V": {"name": "Moi_truong_hoc_tap", "count": 5},
    "VI": {"name": "Quan_ly_thoi_gian", "count": 4},
    "VII": {"name": "Tu_hoc", "count": 4},
    "VIII": {"name": "Hop_tac_nhom", "count": 4},
    "IX": {"name": "Tu_duy_phan_bien", "count": 4},
    "X": {"name": "Tiep_thu_xu_ly_kien_thuc", "count": 4}
}

# --- File Upload Configuration ---
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB
ALLOWED_EXTENSIONS = {'.xlsx'}
UPLOAD_FOLDER = UPLOADS_DIR

# --- Logging Configuration ---
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# --- LLM Configuration ---
LLM_TIMEOUT = int(os.getenv('LLM_TIMEOUT', 400))
CHAT_TIMEOUT = int(os.getenv('CHAT_TIMEOUT', 180))
MAX_CHAT_HISTORY = int(os.getenv('MAX_CHAT_HISTORY', 10))

# Ensure directories exist
DATABASE_DIR.mkdir(exist_ok=True)
UPLOADS_DIR.mkdir(exist_ok=True) 