# ollama_session_manager.py - Ollama Session Management với Fine-tuning support
# 🔧 Quản lý session Ollama với các commands: /save, /load, /clear, /finetune
# Tích hợp với enhanced prompts system

import json
import os
import requests
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path

class OllamaSessionManager:
    """
    Quản lý Ollama sessions với fine-tuning và model customization
    """
    
    def __init__(self, ollama_url="http://192.168.2.114:11434", 
                 sessions_dir="ollama_sessions", models_dir="ollama_models"):
        self.ollama_url = ollama_url
        self.sessions_dir = Path(sessions_dir)
        self.models_dir = Path(models_dir)
        
        # Create directories
        self.sessions_dir.mkdir(exist_ok=True)
        self.models_dir.mkdir(exist_ok=True)
        
        # Current session state
        self.current_session = None
        self.active_model = "gemma3:latest"
        
        # Session templates
        self.session_templates = self._load_session_templates()
        
        print(f"🔧 Ollama Session Manager initialized - URL: {ollama_url}")
    
    def _load_session_templates(self) -> Dict:
        """Load session templates for different consultation types"""
        return {
            "education_consultation": {
                "system_context": """Bạn là hệ thống tư vấn giáo dục chuyên nghiệp cho sinh viên Việt Nam. 
                Hãy duy trì ngữ cảnh về học sinh và cung cấp lời khuyên nhất quán qua toàn bộ phiên tư vấn.""",
                "parameters": {
                    "temperature": 0.3,
                    "top_p": 0.9,
                    "top_k": 40
                }
            },
            "skills_analysis": {
                "system_context": """Bạn là chuyên gia phân tích kỹ năng học tập với 15+ năm kinh nghiệm. 
                Tập trung vào việc đánh giá chính xác và đưa ra roadmap cải thiện cụ thể.""",
                "parameters": {
                    "temperature": 0.1,
                    "top_p": 0.8,
                    "top_k": 30
                }
            },
            "career_guidance": {
                "system_context": """Bạn là cố vấn nghề nghiệp chuyên về thị trường lao động Việt Nam. 
                Hãy đưa ra lời khuyên dựa trên xu hướng ngành và cơ hội thực tế.""",
                "parameters": {
                    "temperature": 0.4,
                    "top_p": 0.9,
                    "top_k": 50
                }
            }
        }
    
    def save_session(self, session_name: str, context: Dict, 
                    conversation_history: List = None) -> bool:
        """
        Lưu session hiện tại với context và lịch sử hội thoại
        Command: /save session_name
        """
        try:
            session_data = {
                "name": session_name,
                "timestamp": datetime.now().isoformat(),
                "context": context,
                "conversation_history": conversation_history or [],
                "active_model": self.active_model,
                "session_type": context.get("session_type", "general")
            }
            
            session_file = self.sessions_dir / f"{session_name}.json"
            with open(session_file, 'w', encoding='utf-8') as f:
                json.dump(session_data, f, ensure_ascii=False, indent=2)
            
            self.current_session = session_data
            print(f"💾 Session '{session_name}' đã được lưu thành công")
            return True
            
        except Exception as e:
            print(f"❌ Lỗi lưu session: {e}")
            return False
    
    def load_session(self, session_name: str) -> Optional[Dict]:
        """
        Tải session đã lưu
        Command: /load session_name
        """
        try:
            session_file = self.sessions_dir / f"{session_name}.json"
            if not session_file.exists():
                print(f"❌ Session '{session_name}' không tồn tại")
                return None
            
            with open(session_file, 'r', encoding='utf-8') as f:
                session_data = json.load(f)
            
            self.current_session = session_data
            self.active_model = session_data.get("active_model", "gemma3:latest")
            
            print(f"📂 Session '{session_name}' đã được tải thành công")
            print(f"   - Thời gian: {session_data['timestamp']}")
            print(f"   - Model: {self.active_model}")
            print(f"   - Loại: {session_data.get('session_type', 'general')}")
            
            return session_data
            
        except Exception as e:
            print(f"❌ Lỗi tải session: {e}")
            return None
    
    def list_sessions(self) -> List[str]:
        """
        Liệt kê tất cả sessions đã lưu
        Command: /list
        """
        sessions = []
        for session_file in self.sessions_dir.glob("*.json"):
            try:
                with open(session_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    sessions.append({
                        "name": session_file.stem,
                        "timestamp": data.get("timestamp", "Unknown"),
                        "type": data.get("session_type", "general"),
                        "model": data.get("active_model", "Unknown")
                    })
            except:
                continue
        
        sessions.sort(key=lambda x: x["timestamp"], reverse=True)
        
        if sessions:
            print("📋 Danh sách sessions:")
            for session in sessions:
                print(f"   - {session['name']} ({session['type']}) - {session['timestamp'][:16]}")
        else:
            print("📋 Không có session nào được lưu")
        
        return sessions
    
    def clear_session(self) -> bool:
        """
        Xóa session hiện tại
        Command: /clear
        """
        try:
            self.current_session = None
            print("🗑️ Session hiện tại đã được xóa")
            return True
        except Exception as e:
            print(f"❌ Lỗi xóa session: {e}")
            return False
    
    def delete_session(self, session_name: str) -> bool:
        """
        Xóa session đã lưu
        Command: /delete session_name
        """
        try:
            session_file = self.sessions_dir / f"{session_name}.json"
            if session_file.exists():
                session_file.unlink()
                print(f"🗑️ Session '{session_name}' đã được xóa")
                return True
            else:
                print(f"❌ Session '{session_name}' không tồn tại")
                return False
        except Exception as e:
            print(f"❌ Lỗi xóa session: {e}")
            return False
    
    def create_custom_model(self, model_name: str, base_model: str = "gemma3:latest",
                           system_prompt: str = None, parameters: Dict = None) -> bool:
        """
        Tạo custom model với fine-tuning parameters
        Command: /finetune model_name base_model
        """
        try:
            # Create Modelfile
            modelfile_content = f"FROM {base_model}\n"
            
            if system_prompt:
                modelfile_content += f'SYSTEM """{system_prompt}"""\n'
            
            if parameters:
                for param, value in parameters.items():
                    modelfile_content += f"PARAMETER {param} {value}\n"
            
            # Default parameters for education consultation
            default_params = {
                "temperature": 0.3,
                "top_p": 0.9,
                "top_k": 40,
                "repeat_penalty": 1.1
            }
            
            for param, value in default_params.items():
                if parameters is None or param not in parameters:
                    modelfile_content += f"PARAMETER {param} {value}\n"
            
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
            
            response = requests.post(create_url, json=payload, stream=True)
            
            if response.status_code == 200:
                print(f"🎯 Custom model '{model_name}' được tạo thành công")
                print(f"📁 Modelfile saved: {modelfile_path}")
                return True
            else:
                print(f"❌ Lỗi tạo model: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Lỗi tạo custom model: {e}")
            return False
    
    def load_template_session(self, template_type: str) -> bool:
        """
        Tải template session cho consultation type cụ thể
        """
        if template_type not in self.session_templates:
            print(f"❌ Template '{template_type}' không tồn tại")
            print(f"📋 Available templates: {list(self.session_templates.keys())}")
            return False
        
        template = self.session_templates[template_type]
        
        session_context = {
            "session_type": template_type,
            "system_context": template["system_context"],
            "parameters": template["parameters"],
            "template_loaded": True
        }
        
        self.current_session = {
            "name": f"template_{template_type}",
            "timestamp": datetime.now().isoformat(),
            "context": session_context,
            "conversation_history": [],
            "active_model": self.active_model
        }
        
        print(f"📋 Template '{template_type}' đã được tải")
        return True
    
    def get_session_context(self) -> Optional[Dict]:
        """Lấy context của session hiện tại"""
        return self.current_session.get("context") if self.current_session else None
    
    def add_to_conversation_history(self, user_message: str, 
                                   assistant_response: str, metadata: Dict = None):
        """Thêm vào lịch sử hội thoại"""
        if not self.current_session:
            self.current_session = {
                "name": "default",
                "timestamp": datetime.now().isoformat(),
                "context": {},
                "conversation_history": [],
                "active_model": self.active_model
            }
        
        conversation_entry = {
            "timestamp": datetime.now().isoformat(),
            "user": user_message,
            "assistant": assistant_response,
            "metadata": metadata or {}
        }
        
        if "conversation_history" not in self.current_session:
            self.current_session["conversation_history"] = []
        
        self.current_session["conversation_history"].append(conversation_entry)
    
    def export_session(self, session_name: str, format: str = "json") -> Optional[str]:
        """
        Export session để chia sẻ hoặc backup
        """
        session_data = self.load_session(session_name) if session_name != "current" else self.current_session
        
        if not session_data:
            return None
        
        if format == "json":
            export_file = self.sessions_dir / f"{session_name}_export.json"
            with open(export_file, 'w', encoding='utf-8') as f:
                json.dump(session_data, f, ensure_ascii=False, indent=2)
            return str(export_file)
        
        elif format == "markdown":
            export_file = self.sessions_dir / f"{session_name}_export.md"
            
            with open(export_file, 'w', encoding='utf-8') as f:
                f.write(f"# Session: {session_data['name']}\n\n")
                f.write(f"**Timestamp:** {session_data['timestamp']}\n")
                f.write(f"**Model:** {session_data.get('active_model', 'Unknown')}\n")
                f.write(f"**Type:** {session_data.get('session_type', 'general')}\n\n")
                
                if "conversation_history" in session_data:
                    f.write("## Conversation History\n\n")
                    for entry in session_data["conversation_history"]:
                        f.write(f"### {entry['timestamp'][:16]}\n\n")
                        f.write(f"**User:** {entry['user']}\n\n")
                        f.write(f"**Assistant:** {entry['assistant']}\n\n")
                        f.write("---\n\n")
            
            return str(export_file)
        
        return None
    
    def process_command(self, command: str) -> Dict:
        """
        Xử lý các commands cho session management
        """
        parts = command.strip().split()
        if not parts or not parts[0].startswith('/'):
            return {"success": False, "message": "Invalid command format"}
        
        cmd = parts[0][1:].lower()  # Remove '/' prefix
        
        try:
            if cmd == "save" and len(parts) >= 2:
                session_name = parts[1]
                success = self.save_session(session_name, self.get_session_context() or {})
                return {"success": success, "message": f"Session {session_name} saved" if success else "Failed to save session"}
            
            elif cmd == "load" and len(parts) >= 2:
                session_name = parts[1]
                session_data = self.load_session(session_name)
                return {"success": session_data is not None, "data": session_data}
            
            elif cmd == "clear":
                success = self.clear_session()
                return {"success": success, "message": "Session cleared" if success else "Failed to clear session"}
            
            elif cmd == "list":
                sessions = self.list_sessions()
                return {"success": True, "sessions": sessions}
            
            elif cmd == "delete" and len(parts) >= 2:
                session_name = parts[1]
                success = self.delete_session(session_name)
                return {"success": success, "message": f"Session {session_name} deleted" if success else "Failed to delete session"}
            
            elif cmd == "template" and len(parts) >= 2:
                template_type = parts[1]
                success = self.load_template_session(template_type)
                return {"success": success, "message": f"Template {template_type} loaded" if success else "Failed to load template"}
            
            elif cmd == "finetune" and len(parts) >= 3:
                model_name = parts[1]
                base_model = parts[2]
                success = self.create_custom_model(model_name, base_model)
                return {"success": success, "message": f"Model {model_name} created" if success else "Failed to create model"}
            
            elif cmd == "export" and len(parts) >= 2:
                session_name = parts[1]
                format_type = parts[2] if len(parts) >= 3 else "json"
                export_path = self.export_session(session_name, format_type)
                return {"success": export_path is not None, "export_path": export_path}
            
            else:
                return {"success": False, "message": f"Unknown command or missing parameters: {command}"}
                
        except Exception as e:
            return {"success": False, "message": f"Error processing command: {e}"}

# Global session manager instance
session_manager = OllamaSessionManager()
