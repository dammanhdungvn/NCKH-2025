# enhanced_prompts.py - Enhanced Expert Consultation System với RAG, Cache, và Ollama Features
# 🚀 Nâng cấp từ prompts.py với tích hợp:
# - RAG System cho context enhancement
# - Smart Cache cho fast responses
# - Ollama session management
# - Template system cho quick responses
# - Fine-tuning capabilities

import json
import time
from typing import Dict, List, Optional, Tuple
from datetime import datetime

from .rag_system import VietnameseEducationRAG
from .cache_system import SmartCacheSystem
from .prompts import generate_prompt1_payload, generate_prompt2_payload, generate_prompt3_payload

class EnhancedEducationConsultant:
    """
    Enhanced Education Consultant với tích hợp RAG, Cache và Ollama features
    """
    
    def __init__(self, knowledge_base_path="knowledge_base", cache_dir="cache_data"):
        # Initialize systems
        self.rag_system = VietnameseEducationRAG(knowledge_base_path)
        self.cache_system = SmartCacheSystem(cache_dir)
        
        # Session management
        self.current_session = None
        self.session_history = []
        
        # Template responses for common patterns
        self.templates = self._initialize_templates()
        
        # Performance tracking
        self.performance_stats = {
            "total_consultations": 0,
            "cache_hits": 0,
            "rag_enhanced": 0,
            "template_responses": 0,
            "avg_response_time": 0
        }
        
        print("✅ Enhanced Education Consultant initialized!")
    
    def _initialize_templates(self) -> Dict:
        """Initialize quick response templates for common patterns"""
        return {
            "high_performer": {
                "pattern": "skills_avg >= 80 and grades_avg >= 85",
                "template": """🌟 **PHÂN TÍCH NHANH - HỌC SINH XUẤT SẮC**
                
Dựa trên pattern phân tích, bạn thuộc nhóm học sinh có hiệu suất cao:
- Kỹ năng học tập: Xuất sắc (>80%)
- Thành tích học tập: Ưu tú (>85%)

🎯 **KHUYẾN NGHỊ NHANH:**
1. **Phát triển Leadership**: Tham gia các dự án nhóm, mentor junior
2. **Chuyên sâu**: Tập trung vào 1-2 lĩnh vực để trở thành expert
3. **Networking**: Kết nối với industry professionals
4. **Research**: Tham gia nghiên cứu khoa học, publications

⏱️ *Phản hồi nhanh từ template - Để có phân tích chi tiết hơn, vui lòng yêu cầu full consultation*"""
            },
            
            "struggling_student": {
                "pattern": "skills_avg < 50 or grades_avg < 60",
                "template": """💪 **PHÂN TÍCH NHANH - HỖ TRỢ NÂNG CAO**
                
Dựa trên pattern phân tích, bạn cần hỗ trợ để cải thiện:
- Kỹ năng cần phát triển: {weak_skills}
- Môn học cần cải thiện: {weak_subjects}

🎯 **KHUYẾN NGHỊ NGAY:**
1. **Study Skills**: Áp dụng kỹ thuật Pomodoro, active recall
2. **Time Management**: Lập lịch học tập cụ thể hàng tuần
3. **Support System**: Tìm study buddy, tham gia study groups
4. **Academic Help**: Gặp advisor, sử dụng tutoring services

⏱️ *Phản hồi nhanh từ template - Để có phân tích chi tiết hơn, vui lòng yêu cầu full consultation*"""
            },
            
            "balanced_student": {
                "pattern": "50 <= skills_avg < 80 and 60 <= grades_avg < 85",
                "template": """⚖️ **PHÂN TÍCH NHANH - SINH VIÊN CÂN BẰNG**
                
Bạn có profile cân bằng với tiềm năng phát triển:
- Kỹ năng tổng thể: Khá (60-80%)
- Thành tích học tập: Tốt (60-85%)

🎯 **KHUYẾN NGHỊ TỐI ưU:**
1. **Identify Strengths**: Tập trung phát triển điểm mạnh nhất
2. **Address Gaps**: Cải thiện 1-2 kỹ năng yếu nhất
3. **Goal Setting**: Đặt mục tiêu SMART cho từng semester
4. **Exploration**: Thử internship, extracurricular activities

⏱️ *Phản hồi nhanh từ template - Để có phân tích chi tiết hơn, vui lòng yêu cầu full consultation*"""
            }
        }
    
    def analyze_student_pattern(self, khaosat_info: Dict, diem_info: List = None) -> Dict:
        """Phân tích pattern của sinh viên để quyết định response strategy"""
        pattern_info = {}
        
        # Calculate skills average
        skills_fields = [
            "Thai_do_hoc_tap", "Su_dung_mang_xa_hoi", "Gia_dinh_Xa_hoi", "Ban_be",
            "Moi_truong_hoc_tap", "Quan_ly_thoi_gian", "Tu_hoc", "Hop_tac_nhom",
            "Tu_duy_phan_bien", "Tiep_thu_xu_ly_kien_thuc"
        ]
        
        valid_skills = []
        weak_skills = []
        for field in skills_fields:
            skill_data = khaosat_info.get(field, {})
            if isinstance(skill_data, dict) and "phan_tram_diem" in skill_data:
                score = skill_data["phan_tram_diem"]
                valid_skills.append(score)
                if score < 60:
                    weak_skills.append(field.replace("_", " "))
        
        pattern_info["skills_avg"] = sum(valid_skills) / len(valid_skills) if valid_skills else 0
        pattern_info["weak_skills"] = weak_skills
        
        # Calculate grades average if available
        if diem_info:
            grade_values = {"A+": 95, "A": 90, "B+": 85, "B": 80, "C+": 75, "C": 70, "D+": 65, "D": 60, "F": 0}
            valid_grades = []
            weak_subjects = []
            
            for subject in diem_info:
                if "diem_tk_chu" in subject:
                    grade = subject["diem_tk_chu"]
                    if grade in grade_values:
                        score = grade_values[grade]
                        valid_grades.append(score)
                        if score < 70:
                            weak_subjects.append(subject.get("ten_mon_hoc", "Unknown"))
            
            pattern_info["grades_avg"] = sum(valid_grades) / len(valid_grades) if valid_grades else 0
            pattern_info["weak_subjects"] = weak_subjects
        else:
            pattern_info["grades_avg"] = 0
            pattern_info["weak_subjects"] = []
        
        return pattern_info
    
    def get_template_response(self, pattern_info: Dict) -> Optional[str]:
        """Kiểm tra và trả về template response nếu match pattern"""
        skills_avg = pattern_info["skills_avg"]
        grades_avg = pattern_info["grades_avg"]
        
        # High performer
        if skills_avg >= 80 and grades_avg >= 85:
            return self.templates["high_performer"]["template"]
        
        # Struggling student
        elif skills_avg < 50 or grades_avg < 60:
            template = self.templates["struggling_student"]["template"]
            return template.format(
                weak_skills=", ".join(pattern_info["weak_skills"][:3]),
                weak_subjects=", ".join(pattern_info["weak_subjects"][:3])
            )
        
        # Balanced student
        elif 50 <= skills_avg < 80 and 60 <= grades_avg < 85:
            return self.templates["balanced_student"]["template"]
        
        return None
    
    def enhanced_stage1_consultation(self, khaosat_info: Dict, ollama_model: str, 
                                   use_cache: bool = True, use_rag: bool = True, 
                                   force_template: bool = False) -> Dict:
        """
        Enhanced Stage 1 với RAG, Cache và Template support
        """
        start_time = time.time()
        response_metadata = {
            "source": "unknown",
            "cache_hit": False,
            "rag_enhanced": False,
            "template_used": False,
            "response_time": 0,
            "confidence": 0
        }
        
        # Generate student signature
        signature = self.cache_system.generate_student_signature(khaosat_info)
        
        # Analyze student pattern
        pattern_info = self.analyze_student_pattern(khaosat_info)
        
        # 1. Check for template response first (if enabled)
        if force_template:
            template_response = self.get_template_response(pattern_info)
            if template_response:
                response_metadata.update({
                    "source": "template",
                    "template_used": True,
                    "response_time": time.time() - start_time,
                    "confidence": 85
                })
                self.performance_stats["template_responses"] += 1
                return {
                    "response": template_response,
                    "metadata": response_metadata
                }
        
        # 2. Check cache
        cached_response = None
        if use_cache:
            cached_response = self.cache_system.get_cached_response(signature, stage="stage1")
            if cached_response:
                response_metadata.update({
                    "source": "cache",
                    "cache_hit": True,
                    "response_time": time.time() - start_time,
                    "confidence": cached_response.get("confidence", 90)
                })
                self.performance_stats["cache_hits"] += 1
                return {
                    "response": cached_response.get("content", ""),
                    "metadata": response_metadata
                }
        
        # 3. Generate enhanced prompt with RAG
        base_payload = generate_prompt1_payload(khaosat_info, ollama_model)
        
        enhanced_context = ""
        if use_rag:
            # Create search query from student info
            personal = khaosat_info.get("thong_tin_ca_nhan", {})
            search_queries = [
                f"sinh viên {personal.get('khoa', '')}",
                f"kỹ năng học tập yếu"
            ]
            
            # Add weak skills to search
            for field in ["Thai_do_hoc_tap", "Quan_ly_thoi_gian", "Tu_duy_phan_bien"]:
                skill_data = khaosat_info.get(field, {})
                if isinstance(skill_data, dict) and skill_data.get("phan_tram_diem", 0) < 60:
                    search_queries.append(field.replace("_", " "))
            
            # Get relevant context from RAG
            for query in search_queries[:3]:  # Limit queries
                relevant_docs = self.rag_system.search_relevant_knowledge(query, top_k=2)
                for doc in relevant_docs:
                    enhanced_context += f"\n📚 **Kiến thức chuyên môn**: {doc['content']}\n"
            
            if enhanced_context:
                response_metadata["rag_enhanced"] = True
                self.performance_stats["rag_enhanced"] += 1
        
        # Add enhanced context to prompt
        if enhanced_context:
            base_payload["messages"][0]["content"] += f"\n\n**KNOWLEDGE BASE CONTEXT:**{enhanced_context}\n**Hãy tích hợp kiến thức này vào phân tích của bạn.**"
        
        response_metadata.update({
            "source": "llm_enhanced" if enhanced_context else "llm_basic",
            "response_time": time.time() - start_time
        })
        
        self.performance_stats["total_consultations"] += 1
        
        return {
            "payload": base_payload,
            "metadata": response_metadata,
            "signature": signature,
            "cache_enabled": use_cache
        }
    
    def enhanced_stage2_consultation(self, khaosat_info: Dict, diem_info: List, 
                                   ollama_model: str, use_cache: bool = True, 
                                   use_rag: bool = True) -> Dict:
        """Enhanced Stage 2 với RAG và Cache"""
        start_time = time.time()
        response_metadata = {
            "source": "unknown",
            "cache_hit": False,
            "rag_enhanced": False,
            "response_time": 0
        }
        
        # Generate signature including grades
        signature = self.cache_system.generate_student_signature(khaosat_info, diem_info)
        
        # Check cache
        if use_cache:
            cached_response = self.cache_system.get_cached_response(signature, stage="stage2")
            if cached_response:
                response_metadata.update({
                    "source": "cache",
                    "cache_hit": True,
                    "response_time": time.time() - start_time
                })
                return {
                    "response": cached_response.get("content", ""),
                    "metadata": response_metadata
                }
        
        # Generate enhanced prompt
        base_payload = generate_prompt2_payload(khaosat_info, diem_info, ollama_model)
        
        enhanced_context = ""
        if use_rag:
            # Search for major-specific and grade-related knowledge
            personal = khaosat_info.get("thong_tin_ca_nhan", {})
            khoa = personal.get("khoa", "")
            
            search_queries = [
                f"sinh viên {khoa} thành tích học tập",
                "phân tích điểm số và cải thiện"
            ]
            
            # Add low-grade subjects to search
            for subject in diem_info:
                grade = subject.get("diem_tk_chu", "")
                if grade in ["C", "D+", "D", "F"]:
                    search_queries.append(f"cải thiện điểm {subject.get('ten_mon_hoc', '')}")
            
            for query in search_queries[:3]:
                relevant_docs = self.rag_system.search_relevant_knowledge(query, top_k=2)
                for doc in relevant_docs:
                    enhanced_context += f"\n📚 **Kiến thức chuyên môn**: {doc['content']}\n"
            
            if enhanced_context:
                response_metadata["rag_enhanced"] = True
        
        if enhanced_context:
            base_payload["messages"][0]["content"] += f"\n\n**KNOWLEDGE BASE CONTEXT:**{enhanced_context}\n**Hãy tích hợp kiến thức này vào phân tích điểm số.**"
        
        response_metadata.update({
            "source": "llm_enhanced" if enhanced_context else "llm_basic",
            "response_time": time.time() - start_time
        })
        
        return {
            "payload": base_payload,
            "metadata": response_metadata,
            "signature": signature,
            "cache_enabled": use_cache
        }
    
    def enhanced_stage3_consultation(self, khaosat_info: Dict, diem_info: List,
                                   stage1_result: str, stage2_result: str,
                                   ollama_model: str, use_cache: bool = True,
                                   use_rag: bool = True) -> Dict:
        """Enhanced Stage 3 với comprehensive analysis"""
        start_time = time.time()
        response_metadata = {
            "source": "unknown",
            "cache_hit": False,
            "rag_enhanced": False,
            "response_time": 0
        }
        
        # Generate comprehensive signature
        signature = self.cache_system.generate_student_signature(khaosat_info, diem_info)
        signature += f"_stage3_{hash(stage1_result + stage2_result) % 10000}"
        
        # Check cache
        if use_cache:
            cached_response = self.cache_system.get_cached_response(signature, stage="stage3")
            if cached_response:
                response_metadata.update({
                    "source": "cache",
                    "cache_hit": True,
                    "response_time": time.time() - start_time
                })
                return {
                    "response": cached_response.get("content", ""),
                    "metadata": response_metadata
                }
        
        # Generate enhanced prompt
        base_payload = generate_prompt3_payload(stage1_result, stage2_result, khaosat_info, ollama_model)
        
        enhanced_context = ""
        if use_rag:
            # Search for career guidance and strategic planning
            personal = khaosat_info.get("thong_tin_ca_nhan", {})
            
            search_queries = [
                f"định hướng nghề nghiệp {personal.get('khoa', '')}",
                "chiến lược phát triển sinh viên",
                "kỹ năng mềm và hard skills"
            ]
            
            for query in search_queries:
                relevant_docs = self.rag_system.search_relevant_knowledge(query, top_k=3)
                for doc in relevant_docs:
                    enhanced_context += f"\n📚 **Kiến thức chuyên môn**: {doc['content']}\n"
            
            if enhanced_context:
                response_metadata["rag_enhanced"] = True
        
        if enhanced_context:
            base_payload["messages"][0]["content"] += f"\n\n**STRATEGIC KNOWLEDGE BASE:**{enhanced_context}\n**Hãy tích hợp kiến thức này vào tư vấn chiến lược.**"
        
        response_metadata.update({
            "source": "llm_enhanced" if enhanced_context else "llm_basic",
            "response_time": time.time() - start_time
        })
        
        return {
            "payload": base_payload,
            "metadata": response_metadata,
            "signature": signature,
            "cache_enabled": use_cache
        }
    
    def save_successful_consultation(self, signature: str, stage: str, 
                                   response: str, feedback_score: int = None):
        """Lưu consultation thành công vào cache và update RAG"""
        if feedback_score and feedback_score >= 4:  # Only cache good responses
            confidence = min(95, 70 + feedback_score * 5)
            self.cache_system.cache_response(signature, stage, response, confidence)
            
            # Add to RAG knowledge base if very positive feedback
            if feedback_score >= 5:
                self.rag_system.add_successful_consultation(response, {
                    "stage": stage,
                    "feedback_score": feedback_score,
                    "timestamp": datetime.now().isoformat()
                })
    
    # Ollama Session Management
    def save_session(self, session_name: str, context: Dict):
        """Save current consultation session"""
        self.current_session = {
            "name": session_name,
            "context": context,
            "timestamp": datetime.now().isoformat(),
            "history": self.session_history.copy()
        }
        print(f"💾 Session '{session_name}' saved successfully")
    
    def load_session(self, session_name: str) -> bool:
        """Load a saved session"""
        # In a real implementation, this would load from persistent storage
        if self.current_session and self.current_session["name"] == session_name:
            self.session_history = self.current_session["history"]
            print(f"📂 Session '{session_name}' loaded successfully")
            return True
        return False
    
    def clear_session(self):
        """Clear current session"""
        self.current_session = None
        self.session_history = []
        print("🗑️ Session cleared")
    
    def get_performance_stats(self) -> Dict:
        """Get performance statistics"""
        cache_hit_rate = (self.performance_stats["cache_hits"] / 
                         max(1, self.performance_stats["total_consultations"])) * 100
        
        return {
            **self.performance_stats,
            "cache_hit_rate": f"{cache_hit_rate:.1f}%",
            "cache_system_stats": self.cache_system.get_stats(),
            "rag_knowledge_count": len(self.rag_system.documents)
        }

# Utility functions for backward compatibility
def generate_enhanced_prompt1_payload(khaosat_info, ollama_model, consultant=None, **kwargs):
    """Wrapper function for backward compatibility"""
    if consultant is None:
        consultant = EnhancedEducationConsultant()
    return consultant.enhanced_stage1_consultation(khaosat_info, ollama_model, **kwargs)

def generate_enhanced_prompt2_payload(khaosat_info, diem_info, ollama_model, consultant=None, **kwargs):
    """Wrapper function for backward compatibility"""
    if consultant is None:
        consultant = EnhancedEducationConsultant()
    return consultant.enhanced_stage2_consultation(khaosat_info, diem_info, ollama_model, **kwargs)

def generate_enhanced_prompt3_payload(khaosat_info, diem_info, stage1_result, stage2_result, 
                                    ollama_model, consultant=None, **kwargs):
    """Wrapper function for backward compatibility"""
    if consultant is None:
        consultant = EnhancedEducationConsultant()
    return consultant.enhanced_stage3_consultation(khaosat_info, diem_info, stage1_result, 
                                                 stage2_result, ollama_model, **kwargs)
