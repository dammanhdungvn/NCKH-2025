# fine_tuning_manager.py - Fine-tuning Support cho Vietnamese Education Models
# 🎯 Quản lý fine-tuning models với educational data và feedback

import json
import os
import requests
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from pathlib import Path

class FineTuningManager:
    """
    Quản lý fine-tuning process cho educational consultation models
    """
    
    def __init__(self, ollama_url="http://192.168.2.114:11434", 
                 training_data_dir="training_data", models_dir="custom_models"):
        self.ollama_url = ollama_url
        self.training_data_dir = Path(training_data_dir)
        self.models_dir = Path(models_dir)
        
        # Create directories
        self.training_data_dir.mkdir(exist_ok=True)
        self.models_dir.mkdir(exist_ok=True)
        
        # Training configurations
        self.model_configs = self._initialize_model_configs()
        
        # Performance tracking
        self.training_history = self._load_training_history()
        
        print(f"🎯 Fine-tuning Manager initialized - Training dir: {training_data_dir}")
    
    def _initialize_model_configs(self) -> Dict:
        """Initialize model configurations for different educational domains"""
        return {
            "education_consultant_v1": {
                "base_model": "gemma3:latest",
                "description": "Specialized Vietnamese education consultant",
                "system_prompt": """Bạn là chuyên gia tư vấn giáo dục với 15+ năm kinh nghiệm tại Việt Nam. 
                Hãy cung cấp lời khuyên chuyên nghiệp, thực tế và phù hợp với bối cảnh giáo dục Việt Nam.
                Luôn sử dụng tiếng Việt và tham khảo các chuẩn giáo dục trong nước.""",
                "parameters": {
                    "temperature": 0.3,
                    "top_p": 0.9,
                    "top_k": 40,
                    "repeat_penalty": 1.1,
                    "num_ctx": 4096
                },
                "training_focus": ["skills_analysis", "grade_improvement", "career_guidance"]
            },
            
            "skills_analyzer_v1": {
                "base_model": "gemma3:latest", 
                "description": "Specialized in learning skills analysis and improvement",
                "system_prompt": """Bạn là chuyên gia phân tích kỹ năng học tập với PhD in Educational Psychology.
                Chuyên môn: EBLAS (Evidence-Based Learning Assessment Scale) và các phương pháp khoa học.
                Hãy đưa ra phân tích chính xác và kế hoạch cải thiện cụ thể.""",
                "parameters": {
                    "temperature": 0.1,
                    "top_p": 0.8,
                    "top_k": 30,
                    "repeat_penalty": 1.15,
                    "num_ctx": 3072
                },
                "training_focus": ["skills_assessment", "improvement_strategies", "study_methods"]
            },
            
            "career_advisor_v1": {
                "base_model": "gemma3:latest",
                "description": "Specialized in career guidance for Vietnamese students", 
                "system_prompt": """Bạn là cố vấn nghề nghiệp chuyên về thị trường lao động Việt Nam.
                Hiểu biết sâu về các ngành nghề, xu hướng tuyển dụng và yêu cầu skills.
                Hãy đưa ra lời khuyên nghề nghiệp thực tế và roadmap phát triển cụ thể.""",
                "parameters": {
                    "temperature": 0.4,
                    "top_p": 0.9,
                    "top_k": 50,
                    "repeat_penalty": 1.1,
                    "num_ctx": 6144
                },
                "training_focus": ["career_planning", "industry_insights", "skill_requirements"]
            }
        }
    
    def _load_training_history(self) -> Dict:
        """Load training history from file"""
        history_file = self.training_data_dir / "training_history.json"
        if history_file.exists():
            try:
                with open(history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        return {"models": {}, "training_sessions": []}
    
    def _save_training_history(self):
        """Save training history to file"""
        history_file = self.training_data_dir / "training_history.json"
        try:
            with open(history_file, 'w', encoding='utf-8') as f:
                json.dump(self.training_history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"⚠️ Error saving training history: {e}")
    
    def collect_training_data(self, consultation_data: List[Dict], 
                            feedback_threshold: int = 4) -> Dict:
        """
        Collect and prepare training data from successful consultations
        """
        training_samples = {
            "skills_analysis": [],
            "grade_improvement": [], 
            "career_guidance": [],
            "general_consultation": []
        }
        
        for consultation in consultation_data:
            feedback_score = consultation.get("feedback_score", 0)
            if feedback_score < feedback_threshold:
                continue
                
            # Categorize consultation type
            stage = consultation.get("stage", "general")
            consultation_type = self._categorize_consultation(consultation)
            
            # Create training sample
            sample = {
                "input": consultation.get("user_input", ""),
                "output": consultation.get("assistant_response", ""),
                "context": consultation.get("context", {}),
                "feedback_score": feedback_score,
                "timestamp": consultation.get("timestamp", ""),
                "metadata": {
                    "stage": stage,
                    "student_profile": consultation.get("student_profile", {}),
                    "confidence": consultation.get("confidence", 0)
                }
            }
            
            training_samples[consultation_type].append(sample)
        
        # Save training data
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        training_file = self.training_data_dir / f"training_data_{timestamp}.json"
        
        with open(training_file, 'w', encoding='utf-8') as f:
            json.dump(training_samples, f, ensure_ascii=False, indent=2)
        
        stats = {category: len(samples) for category, samples in training_samples.items()}
        print(f"✅ Training data collected: {stats}")
        print(f"📁 Saved to: {training_file}")
        
        return {
            "file_path": str(training_file),
            "stats": stats,
            "total_samples": sum(stats.values())
        }
    
    def _categorize_consultation(self, consultation: Dict) -> str:
        """Categorize consultation for targeted training"""
        stage = consultation.get("stage", "")
        content = consultation.get("assistant_response", "").lower()
        
        if stage == "stage1" or "kỹ năng" in content or "skills" in content:
            return "skills_analysis"
        elif stage == "stage2" or "điểm" in content or "grade" in content:
            return "grade_improvement"
        elif stage == "stage3" or "nghề nghiệp" in content or "career" in content:
            return "career_guidance"
        else:
            return "general_consultation"
    
    def create_fine_tuned_model(self, model_name: str, base_model: str = None,
                               training_data_file: str = None, 
                               model_type: str = "education_consultant_v1") -> Dict:
        """
        Create fine-tuned model with educational training data
        """
        try:
            # Get model configuration
            if model_type not in self.model_configs:
                return {"success": False, "error": f"Unknown model type: {model_type}"}
            
            config = self.model_configs[model_type]
            base_model = base_model or config["base_model"]
            
            # Create enhanced Modelfile
            modelfile_content = self._create_modelfile(config, training_data_file)
            
            # Save Modelfile
            modelfile_path = self.models_dir / f"{model_name}.Modelfile"
            with open(modelfile_path, 'w', encoding='utf-8') as f:
                f.write(modelfile_content)
            
            # Create model via Ollama API
            create_url = f"{self.ollama_url}/api/create"
            payload = {
                "name": model_name,
                "modelfile": modelfile_content
            }
            
            print(f"🔨 Creating fine-tuned model: {model_name}")
            response = requests.post(create_url, json=payload, stream=True)
            
            if response.status_code == 200:
                # Track training session
                training_session = {
                    "model_name": model_name,
                    "base_model": base_model,
                    "model_type": model_type,
                    "training_data_file": training_data_file,
                    "timestamp": datetime.now().isoformat(),
                    "status": "completed",
                    "modelfile_path": str(modelfile_path)
                }
                
                self.training_history["training_sessions"].append(training_session)
                self.training_history["models"][model_name] = training_session
                self._save_training_history()
                
                print(f"✅ Fine-tuned model '{model_name}' created successfully")
                print(f"📁 Modelfile: {modelfile_path}")
                
                return {
                    "success": True,
                    "model_name": model_name,
                    "modelfile_path": str(modelfile_path),
                    "training_session": training_session
                }
            else:
                error_msg = f"HTTP {response.status_code}: {response.text}"
                print(f"❌ Failed to create model: {error_msg}")
                return {"success": False, "error": error_msg}
                
        except Exception as e:
            print(f"❌ Error creating fine-tuned model: {e}")
            return {"success": False, "error": str(e)}
    
    def _create_modelfile(self, config: Dict, training_data_file: str = None) -> str:
        """Create enhanced Modelfile with training data and configuration"""
        modelfile = f"FROM {config['base_model']}\n\n"
        
        # System prompt
        modelfile += f'SYSTEM """{config["system_prompt"]}"""\n\n'
        
        # Parameters
        for param, value in config["parameters"].items():
            modelfile += f"PARAMETER {param} {value}\n"
        
        # Add training examples if provided
        if training_data_file and os.path.exists(training_data_file):
            try:
                with open(training_data_file, 'r', encoding='utf-8') as f:
                    training_data = json.load(f)
                
                # Add high-quality examples as TEMPLATE
                focus_areas = config.get("training_focus", [])
                examples_added = 0
                
                for focus_area in focus_areas:
                    if focus_area in training_data:
                        samples = training_data[focus_area]
                        # Sort by feedback score and take top examples
                        top_samples = sorted(samples, 
                                           key=lambda x: x.get("feedback_score", 0), 
                                           reverse=True)[:3]
                        
                        for sample in top_samples:
                            if examples_added >= 10:  # Limit examples
                                break
                                
                            user_input = sample.get("input", "").strip()
                            assistant_output = sample.get("output", "").strip()
                            
                            if user_input and assistant_output:
                                # Escape quotes and format as template
                                user_escaped = user_input.replace('"', '\\"')
                                assistant_escaped = assistant_output.replace('"', '\\"')
                                
                                modelfile += f'\nTEMPLATE """{{ if .Prompt }}{{ .Prompt }}{{ else }}User: {user_escaped[:200]}...\nAssistant: {assistant_escaped[:200]}...{{ end }}"""\n'
                                examples_added += 1
                
                print(f"📚 Added {examples_added} training examples to Modelfile")
                
            except Exception as e:
                print(f"⚠️ Could not add training examples: {e}")
        
        return modelfile
    
    def evaluate_model_performance(self, model_name: str, 
                                 test_cases: List[Dict]) -> Dict:
        """
        Evaluate fine-tuned model performance against test cases
        """
        results = {
            "model_name": model_name,
            "total_tests": len(test_cases),
            "passed": 0,
            "failed": 0,
            "average_score": 0,
            "detailed_results": []
        }
        
        total_score = 0
        
        for i, test_case in enumerate(test_cases):
            try:
                # Call model with test input
                chat_url = f"{self.ollama_url}/api/chat"
                payload = {
                    "model": model_name,
                    "messages": [
                        {"role": "user", "content": test_case["input"]}
                    ],
                    "stream": False
                }
                
                response = requests.post(chat_url, json=payload)
                
                if response.status_code == 200:
                    model_output = response.json().get("message", {}).get("content", "")
                    
                    # Score the response (simplified scoring)
                    score = self._score_response(
                        model_output, 
                        test_case.get("expected_keywords", []),
                        test_case.get("expected_length", 100)
                    )
                    
                    test_result = {
                        "test_id": i + 1,
                        "input": test_case["input"][:100] + "...",
                        "output": model_output[:200] + "...",
                        "score": score,
                        "passed": score >= 70
                    }
                    
                    results["detailed_results"].append(test_result)
                    total_score += score
                    
                    if score >= 70:
                        results["passed"] += 1
                    else:
                        results["failed"] += 1
                        
                else:
                    results["failed"] += 1
                    results["detailed_results"].append({
                        "test_id": i + 1,
                        "input": test_case["input"][:100] + "...",
                        "error": f"HTTP {response.status_code}",
                        "score": 0,
                        "passed": False
                    })
                    
            except Exception as e:
                results["failed"] += 1
                results["detailed_results"].append({
                    "test_id": i + 1,
                    "input": test_case["input"][:100] + "...",
                    "error": str(e),
                    "score": 0,
                    "passed": False
                })
        
        results["average_score"] = total_score / len(test_cases) if test_cases else 0
        results["pass_rate"] = (results["passed"] / len(test_cases) * 100) if test_cases else 0
        
        # Save evaluation results
        eval_file = self.models_dir / f"{model_name}_evaluation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(eval_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        print(f"📊 Model evaluation completed")
        print(f"   - Pass rate: {results['pass_rate']:.1f}%")
        print(f"   - Average score: {results['average_score']:.1f}")
        print(f"📁 Results saved: {eval_file}")
        
        return results
    
    def _score_response(self, response: str, expected_keywords: List[str], 
                       expected_length: int) -> float:
        """Simple scoring function for model responses"""
        score = 0
        
        # Length check (20 points)
        if len(response) >= expected_length * 0.8:
            score += 20
        
        # Keyword presence (60 points)
        keyword_score = 0
        for keyword in expected_keywords:
            if keyword.lower() in response.lower():
                keyword_score += 60 / len(expected_keywords)
        score += keyword_score
        
        # Vietnamese language check (10 points)
        vietnamese_chars = "àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ"
        if any(char in response.lower() for char in vietnamese_chars):
            score += 10
        
        # Professional tone check (10 points)
        professional_indicators = ["khuyến nghị", "đề xuất", "phân tích", "đánh giá", "tư vấn"]
        if any(indicator in response.lower() for indicator in professional_indicators):
            score += 10
        
        return min(100, score)
    
    def list_custom_models(self) -> List[Dict]:
        """List all custom fine-tuned models"""
        try:
            # Get models from Ollama
            models_url = f"{self.ollama_url}/api/tags"
            response = requests.get(models_url)
            
            if response.status_code == 200:
                all_models = response.json().get("models", [])
                custom_models = []
                
                for model in all_models:
                    model_name = model.get("name", "")
                    if model_name in self.training_history["models"]:
                        training_info = self.training_history["models"][model_name]
                        custom_models.append({
                            "name": model_name,
                            "size": model.get("size", 0),
                            "modified": model.get("modified_at", ""),
                            "training_info": training_info
                        })
                
                return custom_models
            else:
                print(f"❌ Error fetching models: HTTP {response.status_code}")
                return []
                
        except Exception as e:
            print(f"❌ Error listing custom models: {e}")
            return []
    
    def delete_custom_model(self, model_name: str) -> bool:
        """Delete a custom fine-tuned model"""
        try:
            # Delete from Ollama
            delete_url = f"{self.ollama_url}/api/delete"
            payload = {"name": model_name}
            
            response = requests.delete(delete_url, json=payload)
            
            if response.status_code == 200:
                # Remove from training history
                if model_name in self.training_history["models"]:
                    del self.training_history["models"][model_name]
                    self._save_training_history()
                
                print(f"🗑️ Model '{model_name}' deleted successfully")
                return True
            else:
                print(f"❌ Error deleting model: HTTP {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Error deleting model: {e}")
            return False
    
    def get_training_stats(self) -> Dict:
        """Get training statistics and history"""
        return {
            "total_models": len(self.training_history["models"]),
            "total_training_sessions": len(self.training_history["training_sessions"]),
            "model_types": list(self.model_configs.keys()),
            "recent_sessions": self.training_history["training_sessions"][-5:],
            "available_configs": {
                name: {
                    "description": config["description"],
                    "training_focus": config["training_focus"]
                }
                for name, config in self.model_configs.items()
            }
        }

# Global fine-tuning manager instance
fine_tuning_manager = FineTuningManager()
