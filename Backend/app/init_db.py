#!/usr/bin/env python3
"""
Database Initialization Script for Enhanced Education Consultant System
This script initializes the database with sample data and sets up the AI components.
"""

import json
import os
import sys
from datetime import datetime

# Add the app directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def init_database():
    """Initialize the database with sample data"""
    
    # Base directory paths
    base_dir = os.path.dirname(os.path.abspath(__file__))
    database_dir = os.path.join(base_dir, '..', '..', 'Database')
    
    # Ensure database directory exists
    os.makedirs(database_dir, exist_ok=True)
    
    # Sample survey data (khaosat.json)
    sample_surveys = [
        {
            "id": 1,
            "user_id": "user_001",
            "survey_type": "academic_preference",
            "questions_answers": {
                "favorite_subjects": ["Toán", "Vật lý", "Hóa học"],
                "learning_style": "visual",
                "career_interests": ["Công nghệ thông tin", "Kỹ thuật"],
                "strengths": ["Tư duy logic", "Giải quyết vấn đề"],
                "weaknesses": ["Giao tiếp", "Thuyết trình"]
            },
            "timestamp": datetime.now().isoformat()
        },
        {
            "id": 2,
            "user_id": "user_002",
            "survey_type": "career_exploration",
            "questions_answers": {
                "favorite_subjects": ["Văn học", "Lịch sử", "Địa lý"],
                "learning_style": "auditory",
                "career_interests": ["Giáo dục", "Báo chí"],
                "strengths": ["Viết lách", "Phân tích"],
                "weaknesses": ["Toán học", "Khoa học"]
            },
            "timestamp": datetime.now().isoformat()
        }
    ]
    
    # Sample grade data (diem_simplified.json)
    sample_grades = [
        {
            "id": 1,
            "user_id": "user_001",
            "semester": "2023-2024-1",
            "subjects": {
                "Toán": 8.5,
                "Vật lý": 8.0,
                "Hóa học": 7.5,
                "Sinh học": 7.0,
                "Văn": 6.5,
                "Anh": 7.5,
                "Lịch sử": 6.0,
                "Địa lý": 6.5
            },
            "gpa": 7.31,
            "ranking": 15,
            "total_students": 150
        },
        {
            "id": 2,
            "user_id": "user_002",
            "semester": "2023-2024-1",
            "subjects": {
                "Toán": 6.0,
                "Vật lý": 5.5,
                "Hóa học": 6.0,
                "Sinh học": 6.5,
                "Văn": 9.0,
                "Anh": 8.0,
                "Lịch sử": 8.5,
                "Địa lý": 8.0
            },
            "gpa": 7.19,
            "ranking": 18,
            "total_students": 150
        }
    ]
    
    # Save survey data
    khaosat_path = os.path.join(database_dir, 'khaosat.json')
    with open(khaosat_path, 'w', encoding='utf-8') as f:
        json.dump(sample_surveys, f, ensure_ascii=False, indent=2)
    
    # Save grade data
    diem_path = os.path.join(database_dir, 'diem_simplified.json')
    with open(diem_path, 'w', encoding='utf-8') as f:
        json.dump(sample_grades, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Database initialized successfully!")
    print(f"📁 Survey data saved to: {khaosat_path}")
    print(f"📁 Grade data saved to: {diem_path}")

def init_sample_courses():
    """Initialize sample course data for the recommendation system"""
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    database_dir = os.path.join(base_dir, '..', '..', 'Database')
    
    sample_courses = [
        {
            "id": 1,
            "title": "Khoa học Máy tính",
            "category": "STEM",
            "description": "Ngành học về thuật toán, lập trình và công nghệ thông tin",
            "prerequisites": ["Toán học mạnh", "Tư duy logic"],
            "career_prospects": ["Lập trình viên", "Kỹ sư phần mềm", "Data Scientist"],
            "difficulty_level": 8,
            "duration_years": 4,
            "skills_required": ["Tư duy logic", "Giải quyết vấn đề", "Toán học"],
            "universities": ["Đại học Bách Khoa", "Đại học Công nghệ", "Đại học Quốc gia"]
        },
        {
            "id": 2,
            "title": "Ngôn ngữ Anh",
            "category": "Humanities",
            "description": "Ngành học về ngôn ngữ, văn học và văn hóa Anh-Mỹ",
            "prerequisites": ["Khả năng ngoại ngữ", "Kỹ năng giao tiếp"],
            "career_prospects": ["Giáo viên", "Phiên dịch", "Nhà báo"],
            "difficulty_level": 6,
            "duration_years": 4,
            "skills_required": ["Giao tiếp", "Viết lách", "Phân tích văn bản"],
            "universities": ["Đại học Ngoại ngữ", "Đại học Sư phạm", "Đại học Khoa học Xã hội"]
        },
        {
            "id": 3,
            "title": "Kỹ thuật Cơ khí",
            "category": "Engineering",
            "description": "Ngành học về thiết kế, chế tạo và vận hành máy móc",
            "prerequisites": ["Vật lý", "Toán học", "Tư duy không gian"],
            "career_prospects": ["Kỹ sư cơ khí", "Thiết kế sản phẩm", "Quản lý sản xuất"],
            "difficulty_level": 9,
            "duration_years": 4,
            "skills_required": ["Toán học", "Vật lý", "Thiết kế", "Tư duy không gian"],
            "universities": ["Đại học Bách Khoa", "Đại học Công nghiệp", "Đại học Kỹ thuật"]
        }
    ]
    
    courses_path = os.path.join(database_dir, 'courses.json')
    with open(courses_path, 'w', encoding='utf-8') as f:
        json.dump(sample_courses, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Sample courses initialized!")
    print(f"📁 Courses data saved to: {courses_path}")

def init_ai_components():
    """Initialize AI components and create necessary directories"""
    
    app_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Create directories for AI components
    ai_dirs = [
        os.path.join(app_dir, 'data', 'vectors'),
        os.path.join(app_dir, 'data', 'cache'),
        os.path.join(app_dir, 'data', 'models')
    ]
    
    for dir_path in ai_dirs:
        os.makedirs(dir_path, exist_ok=True)
        print(f"📁 Created directory: {dir_path}")
    
    # Create initial vector database metadata
    vector_metadata = {
        "last_updated": datetime.now().isoformat(),
        "document_count": 0,
        "vector_dimension": 384,  # Default for sentence-transformers
        "model_name": "paraphrase-multilingual-MiniLM-L12-v2"
    }
    
    metadata_path = os.path.join(app_dir, 'data', 'vectors', 'metadata.json')
    with open(metadata_path, 'w', encoding='utf-8') as f:
        json.dump(vector_metadata, f, ensure_ascii=False, indent=2)
    
    print(f"✅ AI components initialized!")

def main():
    """Main initialization function"""
    print("🚀 Initializing Enhanced Education Consultant System...")
    print("=" * 60)
    
    try:
        # Initialize database
        init_database()
        print()
        
        # Initialize sample courses
        init_sample_courses()
        print()
        
        # Initialize AI components
        init_ai_components()
        print()
        
        print("=" * 60)
        print("🎉 System initialization completed successfully!")
        print("📝 You can now start the application with: python app.py")
        
    except Exception as e:
        print(f"❌ Error during initialization: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
