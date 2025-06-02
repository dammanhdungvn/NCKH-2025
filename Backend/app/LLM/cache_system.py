# cache_system.py - Hệ thống cache thông minh với pattern recognition
import json
import hashlib
import pickle
import os
from datetime import datetime, timedelta
from typing import Optional, Dict, List
import numpy as np

class SmartCacheSystem:
    def __init__(self, cache_dir="cache_data"):
        """
        Hệ thống cache thông minh cho educational consultation
        """
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
        
        # Load cached patterns
        self.patterns_file = os.path.join(cache_dir, "patterns.json")
        self.cached_patterns = self._load_patterns()
        
        # Cache statistics
        self.stats = {
            "cache_hits": 0,
            "cache_misses": 0,
            "patterns_matched": 0
        }
    
    def _load_patterns(self) -> Dict:
        """Tải patterns đã cache"""
        if os.path.exists(self.patterns_file):
            try:
                with open(self.patterns_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        return {}
    
    def _save_patterns(self):
        """Lưu patterns"""
        try:
            with open(self.patterns_file, 'w', encoding='utf-8') as f:
                json.dump(self.cached_patterns, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"⚠️ Lỗi lưu patterns: {e}")
    
    def generate_student_signature(self, khaosat_info: Dict, diem_info: List = None) -> str:
        """Tạo signature độc đáo cho từng student pattern"""
        # Trích xuất features quan trọng
        features = {}
        
        # Personal info
        personal = khaosat_info.get("thong_tin_ca_nhan", {})
        features["khoa"] = personal.get("khoa", "unknown")
        
        # Skills pattern - chia thành buckets để tạo pattern
        skills_fields = [
            "Thai_do_hoc_tap", "Su_dung_mang_xa_hoi", "Gia_dinh_Xa_hoi", "Ban_be",
            "Moi_truong_hoc_tap", "Quan_ly_thoi_gian", "Tu_hoc", "Hop_tac_nhom",
            "Tu_duy_phan_bien", "Tiep_thu_xu_ly_kien_thuc"
        ]
        
        skills_pattern = []
        for field in skills_fields:
            skill_data = khaosat_info.get(field, {})
            if isinstance(skill_data, dict) and "phan_tram_diem" in skill_data:
                score = skill_data["phan_tram_diem"]
                # Bucket scores: 0-40, 40-60, 60-75, 75-85, 85-100
                bucket = min(4, score // 20) if score < 85 else 4
                skills_pattern.append(bucket)
            else:
                skills_pattern.append(-1)  # Missing data
        
        features["skills_pattern"] = tuple(skills_pattern)
        
        # Grades pattern if available
        if diem_info:
            grade_buckets = self._categorize_grades(diem_info)
            features["grade_pattern"] = grade_buckets
        
        # Tạo hash từ features
        signature = hashlib.md5(
            json.dumps(features, sort_keys=True).encode()
        ).hexdigest()
        
        return signature
    
    def _categorize_grades(self, diem_info: List) -> tuple:
        """Phân loại grades thành buckets"""
        grade_map = {"A+": 5, "A": 5, "B+": 4, "B": 3, "C+": 2, "C": 2, "D+": 1, "D": 1, "F": 0}
        
        buckets = [0, 0, 0, 0, 0, 0]  # [F, D, C, B, B+, A]
        total = 0
        
        for subject in diem_info:
            if "diem_tk_chu" in subject:
                grade = subject["diem_tk_chu"]
                bucket = grade_map.get(grade, 0)
                buckets[bucket] += 1
                total += 1
        
        # Normalize to percentages and create pattern
        if total > 0:
            percentages = [round(b/total * 100) for b in buckets]
            # Create pattern based on dominant grade ranges
            pattern = []
            for i, pct in enumerate(percentages):
                if pct > 30:  # Significant presence
                    pattern.append(i)
            return tuple(pattern)
        
        return tuple()
    
    def get_cache_key(self, signature: str, stage: int) -> str:
        """Tạo cache key"""
        return f"{signature}_stage_{stage}"
    
    def get_cached_analysis(self, signature: str, stage: int) -> Optional[Dict]:
        """Lấy analysis đã cache"""
        cache_key = self.get_cache_key(signature, stage)
        cache_file = os.path.join(self.cache_dir, f"{cache_key}.pkl")
        
        if os.path.exists(cache_file):
            try:
                with open(cache_file, 'rb') as f:
                    cached_data = pickle.load(f)
                
                # Kiểm tra expiry (cache 24h)
                cache_time = datetime.fromisoformat(cached_data["timestamp"])
                if datetime.now() - cache_time < timedelta(hours=24):
                    self.stats["cache_hits"] += 1
                    return {
                        "content": cached_data["analysis"],
                        "from_cache": True,
                        "cache_time": cached_data["timestamp"],
                        "confidence": cached_data.get("confidence", 0.8)
                    }
                else:
                    # Cache expired
                    os.remove(cache_file)
            except Exception as e:
                print(f"⚠️ Lỗi đọc cache {cache_key}: {e}")
        
        self.stats["cache_misses"] += 1
        return None
    
    def cache_analysis(self, signature: str, stage: int, analysis: str, confidence: float = 0.8):
        """Cache analysis result"""
        cache_key = self.get_cache_key(signature, stage)
        cache_file = os.path.join(self.cache_dir, f"{cache_key}.pkl")
        
        cache_data = {
            "analysis": analysis,
            "timestamp": datetime.now().isoformat(),
            "confidence": confidence,
            "stage": stage,
            "signature": signature
        }
        
        try:
            with open(cache_file, 'wb') as f:
                pickle.dump(cache_data, f)
        except Exception as e:
            print(f"⚠️ Lỗi cache analysis: {e}")
    
    def find_similar_patterns(self, signature: str, threshold: float = 0.8) -> List[Dict]:
        """Tìm patterns tương tự đã cache"""
        similar_patterns = []
        
        if signature in self.cached_patterns:
            return similar_patterns
        
        # Tìm kiếm patterns tương tự (simplified implementation)
        cache_files = [f for f in os.listdir(self.cache_dir) if f.endswith('.pkl')]
        
        for cache_file in cache_files:
            try:
                with open(os.path.join(self.cache_dir, cache_file), 'rb') as f:
                    cached_data = pickle.load(f)
                    
                # Simple similarity check based on signature prefix
                cached_sig = cached_data.get("signature", "")
                if cached_sig and self._calculate_similarity(signature, cached_sig) >= threshold:
                    similar_patterns.append({
                        "signature": cached_sig,
                        "analysis": cached_data["analysis"][:200] + "...",
                        "confidence": cached_data.get("confidence", 0.5),
                        "timestamp": cached_data["timestamp"]
                    })
                    
            except Exception:
                continue
        
        return similar_patterns[:3]  # Top 3 similar patterns
    
    def _calculate_similarity(self, sig1: str, sig2: str) -> float:
        """Tính similarity giữa 2 signatures (simplified)"""
        # Jaccard similarity trên hex characters
        set1 = set(sig1)
        set2 = set(sig2)
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))
        return intersection / union if union > 0 else 0
    
    def add_successful_pattern(self, signature: str, student_data: Dict, analysis_result: str):
        """Thêm pattern thành công vào database"""
        pattern_key = signature[:8]  # Short key
        
        if pattern_key not in self.cached_patterns:
            self.cached_patterns[pattern_key] = []
        
        pattern_entry = {
            "signature": signature,
            "khoa": student_data.get("thong_tin_ca_nhan", {}).get("khoa", "unknown"),
            "success_indicators": self._extract_success_indicators(analysis_result),
            "timestamp": datetime.now().isoformat(),
            "usage_count": 1
        }
        
        self.cached_patterns[pattern_key].append(pattern_entry)
        self.stats["patterns_matched"] += 1
        self._save_patterns()
    
    def _extract_success_indicators(self, analysis: str) -> List[str]:
        """Trích xuất indicators thành công từ analysis"""
        success_keywords = [
            "xuất sắc", "thành thạo", "điểm mạnh", "tiềm năng cao", 
            "proficient", "mastery", "giỏi", "tốt"
        ]
        
        indicators = []
        analysis_lower = analysis.lower()
        
        for keyword in success_keywords:
            if keyword in analysis_lower:
                # Extract context around keyword
                start = max(0, analysis_lower.find(keyword) - 30)
                end = min(len(analysis), analysis_lower.find(keyword) + 50)
                context = analysis[start:end].strip()
                indicators.append(context)
        
        return indicators[:3]  # Top 3 indicators
    
    def get_statistics(self) -> Dict:
        """Thống kê cache system"""
        total_requests = self.stats["cache_hits"] + self.stats["cache_misses"]
        hit_rate = (self.stats["cache_hits"] / total_requests * 100) if total_requests > 0 else 0
        
        return {
            "cache_hits": self.stats["cache_hits"],
            "cache_misses": self.stats["cache_misses"],
            "hit_rate_percent": round(hit_rate, 2),
            "patterns_stored": len(self.cached_patterns),
            "total_cached_files": len([f for f in os.listdir(self.cache_dir) if f.endswith('.pkl')])
        }
    
    def cleanup_expired_cache(self, hours: int = 48):
        """Dọn dẹp cache cũ"""
        cleanup_count = 0
        cache_files = [f for f in os.listdir(self.cache_dir) if f.endswith('.pkl')]
        
        for cache_file in cache_files:
            try:
                cache_path = os.path.join(self.cache_dir, cache_file)
                with open(cache_path, 'rb') as f:
                    cached_data = pickle.load(f)
                
                cache_time = datetime.fromisoformat(cached_data["timestamp"])
                if datetime.now() - cache_time > timedelta(hours=hours):
                    os.remove(cache_path)
                    cleanup_count += 1
                    
            except Exception:
                continue
        
        return cleanup_count
    
    def get_stats(self) -> Dict:
        """Get cache statistics"""
        total_requests = self.stats["cache_hits"] + self.stats["cache_misses"]
        hit_rate = (self.stats["cache_hits"] / total_requests * 100) if total_requests > 0 else 0
        
        return {
            "cache_hits": self.stats["cache_hits"],
            "cache_misses": self.stats["cache_misses"],
            "patterns_matched": self.stats["patterns_matched"],
            "hit_rate_percentage": round(hit_rate, 2),
            "total_patterns": len(self.cached_patterns),
            "cache_directory": self.cache_dir
        }
    
    def get_cached_response(self, signature: str, stage: str) -> Optional[Dict]:
        """
        Get cached response for a given signature and stage
        Returns None if not found or expired
        """
        # Convert stage to int if it's a string
        if isinstance(stage, str):
            stage_mapping = {
                'stage1': 1,
                'stage2': 2, 
                'stage3': 3
            }
            stage_num = stage_mapping.get(stage, 1)
        else:
            stage_num = int(stage)
            
        return self.get_cached_analysis(signature, stage_num)
    
    def cache_response(self, signature: str, stage: str, response: str, confidence: float = 0.8):
        """
        Cache a response for future use
        """
        # Convert stage to int if it's a string
        if isinstance(stage, str):
            stage_mapping = {
                'stage1': 1,
                'stage2': 2,
                'stage3': 3
            }
            stage_num = stage_mapping.get(stage, 1)
        else:
            stage_num = int(stage)
            
        self.cache_analysis(signature, stage_num, response, confidence)
