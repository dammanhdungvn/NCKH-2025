# rag_system.py - Hệ thống RAG cho tư vấn giáo dục Việt Nam
import json
import numpy as np
import hashlib
import os
from datetime import datetime
from typing import List, Dict, Optional
from sentence_transformers import SentenceTransformer
import faiss
import pickle

class VietnameseEducationRAG:
    def __init__(self, knowledge_base_path="knowledge_base", embedding_model="keepitreal/vietnamese-sbert"):
        """
        Hệ thống RAG chuyên dụng cho tư vấn giáo dục Việt Nam
        """
        self.knowledge_base_path = knowledge_base_path
        self.embedding_model = embedding_model
        self.encoder = None
        self.index = None
        self.documents = []
        self.metadata = []
        
        # Tạo thư mục knowledge base nếu chưa có
        os.makedirs(knowledge_base_path, exist_ok=True)
        
        self._initialize_encoder()
        self._load_or_create_knowledge_base()
    
    def _initialize_encoder(self):
        """Khởi tạo model embedding"""
        try:
            self.encoder = SentenceTransformer(self.embedding_model)
            print(f"✅ Đã tải model embedding: {self.embedding_model}")
        except Exception as e:
            print(f"⚠️ Không thể tải model {self.embedding_model}, sử dụng model backup")
            self.encoder = SentenceTransformer('all-MiniLM-L6-v2')
    
    def _load_or_create_knowledge_base(self):
        """Tải hoặc tạo knowledge base"""
        index_path = os.path.join(self.knowledge_base_path, "faiss_index.pkl")
        docs_path = os.path.join(self.knowledge_base_path, "documents.json")
        
        if os.path.exists(index_path) and os.path.exists(docs_path):
            self._load_existing_knowledge_base(index_path, docs_path)
        else:
            self._create_initial_knowledge_base()
    
    def _load_existing_knowledge_base(self, index_path, docs_path):
        """Tải knowledge base đã có"""
        try:
            with open(index_path, 'rb') as f:
                self.index = pickle.load(f)
            
            with open(docs_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.documents = data['documents']
                self.metadata = data['metadata']
            
            print(f"✅ Đã tải knowledge base với {len(self.documents)} documents")
        except Exception as e:
            print(f"⚠️ Lỗi tải knowledge base: {e}")
            self._create_initial_knowledge_base()
    
    def _create_initial_knowledge_base(self):
        """Tạo knowledge base ban đầu với dữ liệu mẫu"""
        initial_knowledge = self._get_initial_education_knowledge()
        
        # Tạo embeddings
        texts = [doc['content'] for doc in initial_knowledge]
        embeddings = self.encoder.encode(texts)
        
        # Tạo FAISS index
        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatIP(dimension)
        
        # Normalize embeddings cho cosine similarity
        faiss.normalize_L2(embeddings)
        self.index.add(embeddings.astype('float32'))
        
        # Lưu documents và metadata
        self.documents = [doc['content'] for doc in initial_knowledge]
        self.metadata = [doc['metadata'] for doc in initial_knowledge]
        
        self._save_knowledge_base()
        print(f"✅ Đã tạo knowledge base mới với {len(self.documents)} documents")
    
    def _get_initial_education_knowledge(self) -> List[Dict]:
        """Dữ liệu kiến thức giáo dục Việt Nam ban đầu"""
        return [
            {
                "content": "Sinh viên Công nghệ thông tin thường có điểm mạnh trong tư duy logic, giải quyết vấn đề và làm việc với công nghệ. Các lĩnh vực phát triển bao gồm: Phát triển phần mềm, An ninh mạng, Khoa học dữ liệu, AI/ML, DevOps.",
                "metadata": {"khoa": "Công nghệ thông tin", "type": "strength_analysis", "keywords": ["CNTT", "programming", "logic"]}
            },
            {
                "content": "Sinh viên Kinh tế thường có điểm mạnh trong phân tích, giao tiếp và hiểu biết thị trường. Định hướng nghề nghiệp: Phân tích tài chính, Marketing, Tư vấn kinh doanh, Quản lý dự án, Ngân hàng.",
                "metadata": {"khoa": "Kinh tế", "type": "career_guidance", "keywords": ["economics", "business", "finance"]}
            },
            {
                "content": "Kỹ năng quản lý thời gian kém (dưới 60%) thường dẫn đến stress học tập và hiệu suất thấp. Giải pháp: Sử dụng Pomodoro Technique, lập kế hoạch hàng tuần, ưu tiên việc quan trọng.",
                "metadata": {"skill": "Quan_ly_thoi_gian", "type": "improvement_strategy", "level": "foundational"}
            },
            {
                "content": "Sinh viên có điểm tư duy phản biện cao (trên 80%) thường thành công trong các ngành yêu cầu phân tích sâu: Nghiên cứu, Tư vấn, Luật, Y khoa, Báo chí điều tra.",
                "metadata": {"skill": "Tu_duy_phan_bien", "type": "career_mapping", "level": "proficient"}
            },
            {
                "content": "Hệ thống điểm Việt Nam: A+ (9.5-10), A (8.5-9.4), B+ (7.8-8.4), B (7.0-7.7), C+ (6.5-6.9), C (5.5-6.4), D+ (4.5-5.4), D (4.0-4.4), F (<4.0). Điểm B+ trở lên được coi là thành tích tốt.",
                "metadata": {"type": "grading_system", "context": "vietnamese_education", "keywords": ["grading", "assessment"]}
            },
            {
                "content": "Sinh viên có kỹ năng làm việc nhóm tốt (trên 75%) thường phù hợp với vai trò: Team Lead, Project Manager, Scrum Master, Sales, HR, Giảng dạy.",
                "metadata": {"skill": "Hop_tac_nhom", "type": "career_mapping", "level": "developing"}
            },
            {
                "content": "Môi trường học tập kém ảnh hưởng trực tiếp đến kết quả học tập. Giải pháp: Tìm không gian yên tĩnh, loại bỏ yếu tố phân tâm, tham gia study group, sử dụng thư viện.",
                "metadata": {"skill": "Moi_truong_hoc_tap", "type": "improvement_strategy", "keywords": ["environment", "study_space"]}
            },
            {
                "content": "Việc sử dụng mạng xã hội quá mức (trên 4 giờ/ngày) có thể ảnh hưởng tiêu cực đến học tập. Cần cân bằng và sử dụng có mục đích cho việc học.",
                "metadata": {"skill": "Su_dung_mang_xa_hoi", "type": "balance_strategy", "keywords": ["social_media", "digital_balance"]}
            }
        ]
    
    def add_knowledge(self, content: str, metadata: Dict):
        """Thêm kiến thức mới vào knowledge base"""
        # Tạo embedding cho content mới
        embedding = self.encoder.encode([content])
        faiss.normalize_L2(embedding)
        
        # Thêm vào index
        self.index.add(embedding.astype('float32'))
        
        # Thêm vào documents và metadata
        self.documents.append(content)
        self.metadata.append(metadata)
        
        # Lưu lại
        self._save_knowledge_base()
    
    def retrieve_relevant_context(self, query: str, top_k: int = 3, min_score: float = 0.5) -> List[Dict]:
        """Lấy context liên quan từ knowledge base"""
        if not self.index or len(self.documents) == 0:
            return []
        
        # Tạo embedding cho query
        query_embedding = self.encoder.encode([query])
        faiss.normalize_L2(query_embedding)
        
        # Search trong FAISS index
        scores, indices = self.index.search(query_embedding.astype('float32'), min(top_k, len(self.documents)))
        
        results = []
        for i, (score, idx) in enumerate(zip(scores[0], indices[0])):
            if score >= min_score:  # Chỉ lấy kết quả có score đủ cao
                results.append({
                    "content": self.documents[idx],
                    "metadata": self.metadata[idx],
                    "score": float(score),
                    "rank": i + 1
                })
        
        return results
    
    def learn_from_consultation(self, student_data: Dict, analysis_result: str, feedback_score: float):
        """Học từ kết quả tư vấn để cải thiện knowledge base"""
        if feedback_score >= 4.0:  # Chỉ học từ feedback tích cực
            # Trích xuất pattern từ student data
            khoa = student_data.get("thong_tin_ca_nhan", {}).get("khoa", "Unknown")
            
            # Tạo knowledge entry mới
            knowledge_content = f"Case study thành công: {analysis_result[:200]}..."
            metadata = {
                "khoa": khoa,
                "type": "successful_case",
                "feedback_score": feedback_score,
                "timestamp": datetime.now().isoformat(),
                "student_pattern": self._extract_student_pattern(student_data)
            }
            
            self.add_knowledge(knowledge_content, metadata)
    
    def _extract_student_pattern(self, student_data: Dict) -> Dict:
        """Trích xuất pattern từ dữ liệu sinh viên"""
        pattern = {}
        
        # Trích xuất skills pattern
        skills_data = student_data.get("skills", {})
        if skills_data:
            pattern["skills_avg"] = np.mean(list(skills_data.values()))
            pattern["top_skills"] = sorted(skills_data.items(), key=lambda x: x[1], reverse=True)[:3]
        
        # Trích xuất grades pattern
        grades_data = student_data.get("grades", [])
        if grades_data:
            grade_values = [self._convert_grade_to_number(g.get("diem_tk_chu", "F")) for g in grades_data]
            pattern["grade_avg"] = np.mean([g for g in grade_values if g > 0])
        
        return pattern
    
    def _convert_grade_to_number(self, grade: str) -> float:
        """Chuyển đổi điểm chữ sang số"""
        grade_map = {"A+": 9.5, "A": 9.0, "B+": 8.0, "B": 7.5, "C+": 6.5, "C": 6.0, "D+": 5.0, "D": 4.5, "F": 0}
        return grade_map.get(grade, 0)
    
    def _save_knowledge_base(self):
        """Lưu knowledge base"""
        try:
            # Lưu FAISS index
            index_path = os.path.join(self.knowledge_base_path, "faiss_index.pkl")
            with open(index_path, 'wb') as f:
                pickle.dump(self.index, f)
            
            # Lưu documents và metadata
            docs_path = os.path.join(self.knowledge_base_path, "documents.json")
            with open(docs_path, 'w', encoding='utf-8') as f:
                json.dump({
                    "documents": self.documents,
                    "metadata": self.metadata,
                    "last_updated": datetime.now().isoformat()
                }, f, ensure_ascii=False, indent=2)
            
        except Exception as e:
            print(f"⚠️ Lỗi lưu knowledge base: {e}")
    
    def get_statistics(self) -> Dict:
        """Thống kê knowledge base"""
        return {
            "total_documents": len(self.documents),
            "knowledge_types": list(set([m.get("type", "unknown") for m in self.metadata])),
            "faculties_covered": list(set([m.get("khoa", "unknown") for m in self.metadata if m.get("khoa")])),
            "skills_covered": list(set([m.get("skill", "unknown") for m in self.metadata if m.get("skill")]))
        }
