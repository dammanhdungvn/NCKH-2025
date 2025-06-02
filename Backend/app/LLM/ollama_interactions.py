# ollama_interactions.py
import requests
import json

# Cấu hình timeout mặc định
DEFAULT_ANALYSIS_TIMEOUT = 400  # seconds cho analysis
DEFAULT_CHAT_TIMEOUT = 180      # seconds cho chat
MAX_CHAT_HISTORY_MESSAGES = 10  # Giới hạn lịch sử chat

def call_ollama_stream_logic(ollama_api_url, payload, stage_key, analysis_results_ref, conversation_history_ref):
    """
    Gọi Ollama API và stream response cho các giai đoạn phân tích.
    
    Args:
        ollama_api_url (str): URL của Ollama API
        payload (dict): Payload gửi tới API
        stage_key (str): Khóa giai đoạn phân tích
        analysis_results_ref (dict): Reference tới dict kết quả phân tích
        conversation_history_ref (list): Reference tới lịch sử conversation
        
    Yields:
        str: SSE formatted response data
    """
    full_response_content = ""
    try:
        response = requests.post(
            ollama_api_url, 
            json=payload, 
            stream=True, 
            timeout=DEFAULT_ANALYSIS_TIMEOUT
        )
        response.raise_for_status()

        for line in response.iter_lines():
            if line:
                decoded_line = line.decode('utf-8')
                try:
                    json_chunk = json.loads(decoded_line)
                    token = json_chunk.get("message", {}).get("content", "")
                    if token:
                        full_response_content += token
                        yield f"data: {json.dumps({'stage': stage_key, 'token': token})}\n\n"

                    if json_chunk.get("done"):
                        analysis_results_ref[stage_key] = full_response_content
                        
                        # Cập nhật conversation history cho stage tổng hợp
                        if stage_key == "stage3_tonghop":
                            if payload.get("messages"):
                                conversation_history_ref[:] = list(payload["messages"]) 
                                conversation_history_ref.append({
                                    "role": "assistant", 
                                    "content": full_response_content
                                })
                            else:
                                conversation_history_ref[:] = [{
                                    "role": "assistant", 
                                    "content": full_response_content
                                }]
                                
                        yield f"data: {json.dumps({'stage': stage_key, 'status': 'done', 'full_response': full_response_content})}\n\n"
                        break
                        
                except json.JSONDecodeError:
                    print(f"DEBUG: Non-JSON line from Ollama stream for stage {stage_key}: {decoded_line}")

    except requests.exceptions.Timeout:
        error_message = f"Lỗi: Timeout ({DEFAULT_ANALYSIS_TIMEOUT}s) khi gọi Ollama API cho {stage_key}."
        print(error_message)
        analysis_results_ref[stage_key] = f"<p style='color:red;'>{error_message}</p>"
        yield f"data: {json.dumps({'stage': stage_key, 'error': error_message})}\n\n"
        
    except requests.exceptions.RequestException as e:
        error_message = f"Lỗi khi gọi Ollama API cho {stage_key}: {str(e)}"
        print(error_message)
        if hasattr(e, 'response') and e.response is not None:
            print(f"Ollama API Error Response: {e.response.text}")
            error_message += f" - Details: {e.response.text}"
        analysis_results_ref[stage_key] = f"<p style='color:red;'>{error_message}</p>"
        yield f"data: {json.dumps({'stage': stage_key, 'error': error_message})}\n\n"
        
    except Exception as e:
        error_message = f"Lỗi không xác định trong quá trình xử lý {stage_key}: {str(e)}"
        print(error_message)
        analysis_results_ref[stage_key] = f"<p style='color:red;'>{error_message}</p>"
        yield f"data: {json.dumps({'stage': stage_key, 'error': error_message})}\n\n"

def ollama_chat_streaming(ollama_api_url, ollama_model, conversation_history, user_message_content):
    """
    Handles streaming chat with Ollama.
    Modifies conversation_history in-place.
    """
    conversation_history.append({"role": "user", "content": user_message_content})

    MAX_CHAT_HISTORY_MESSAGES = 10 
    if len(conversation_history) > MAX_CHAT_HISTORY_MESSAGES:
        relevant_history = [conversation_history[0]] + conversation_history[-(MAX_CHAT_HISTORY_MESSAGES-1):]
    else:
        relevant_history = conversation_history

    payload = {
        "model": ollama_model,
        "messages": relevant_history,
        "stream": True,
        "options": {"temperature": 0.7, "num_ctx": 2048}
    }

    full_chat_response = ""
    try:
        response = requests.post(ollama_api_url, json=payload, stream=True, timeout=180)
        response.raise_for_status()
        for line in response.iter_lines():
            if line:
                decoded_line = line.decode('utf-8')
                try:
                    json_chunk = json.loads(decoded_line)
                    token = json_chunk.get("message", {}).get("content", "")
                    if token:
                        full_chat_response += token
                        yield f"data: {json.dumps({'token': token})}\n\n"
                    if json_chunk.get("done"):
                        conversation_history.append({"role": "assistant", "content": full_chat_response})
                        yield f"data: {json.dumps({'status': 'done'})}\n\n"
                        break
                except json.JSONDecodeError:
                    print(f"Chat stream JSON decode error: {decoded_line}")
    except requests.exceptions.RequestException as e:
        error_msg = f"Lỗi khi chat với Ollama: {str(e)}"
        print(error_msg)
        if conversation_history and conversation_history[-1]["role"] == "user" and conversation_history[-1]["content"] == user_message_content:
            conversation_history.pop()
        yield f"data: {json.dumps({'error': error_msg})}\n\n"