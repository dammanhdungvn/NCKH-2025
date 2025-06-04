"""
Ollama API interaction module.
This module handles streaming communication with the Ollama API for LLM analysis and chat functionality.
"""

import requests
import json
from typing import Dict, List, Any, Iterator, Optional


# Constants
DEFAULT_TIMEOUT = 400
CHAT_TIMEOUT = 180
MAX_CHAT_HISTORY_MESSAGES = 10


def call_ollama_stream_logic(
    ollama_api_url: str,
    payload: Dict[str, Any],
    stage_key: str,
    analysis_results_ref: Dict[str, str],
    conversation_history_ref: List[Dict[str, str]]
) -> Iterator[str]:
    """
    Call Ollama API and stream the response for analysis stages.
    
    Args:
        ollama_api_url (str): URL of the Ollama API
        payload (Dict[str, Any]): Request payload for the API
        stage_key (str): Key identifying the analysis stage
        analysis_results_ref (Dict[str, str]): Reference to store analysis results
        conversation_history_ref (List[Dict[str, str]]): Reference to conversation history
        
    Yields:
        str: Server-sent event formatted strings
    """
    full_response_content = ""
    
    try:
        response = requests.post(
            ollama_api_url, 
            json=payload, 
            stream=True, 
            timeout=DEFAULT_TIMEOUT
        )
        response.raise_for_status()

        for line in response.iter_lines():
            if not line:
                continue
                
            decoded_line = line.decode('utf-8')
            
            try:
                json_chunk = json.loads(decoded_line)
                token = json_chunk.get("message", {}).get("content", "")
                
                if token:
                    full_response_content += token
                    yield _format_sse_data({
                        'stage': stage_key, 
                        'token': token
                    })

                if json_chunk.get("done"):
                    _finalize_analysis_stage(
                        stage_key, 
                        full_response_content, 
                        payload, 
                        analysis_results_ref, 
                        conversation_history_ref
                    )
                    yield _format_sse_data({
                        'stage': stage_key, 
                        'status': 'done', 
                        'full_response': full_response_content
                    })
                    break
                    
            except json.JSONDecodeError:
                print(f"DEBUG: Non-JSON line from Ollama stream for stage {stage_key}: {decoded_line}")

    except requests.exceptions.Timeout:
        error_message = f"Timeout when calling Ollama API for {stage_key}."
        _handle_api_error(stage_key, error_message, analysis_results_ref)
        yield _format_sse_data({'stage': stage_key, 'error': error_message})
        
    except requests.exceptions.RequestException as e:
        error_message = f"Request error when calling Ollama API for {stage_key}: {str(e)}"
        if hasattr(e, 'response') and e.response is not None:
            error_details = e.response.text
            print(f"Ollama API Error Response: {error_details}")
            error_message += f" - Details: {error_details}"
            
        _handle_api_error(stage_key, error_message, analysis_results_ref)
        yield _format_sse_data({'stage': stage_key, 'error': error_message})
        
    except Exception as e:
        error_message = f"Unexpected error during {stage_key} processing: {str(e)}"
        _handle_api_error(stage_key, error_message, analysis_results_ref)
        yield _format_sse_data({'stage': stage_key, 'error': error_message})


def ollama_chat_streaming(
    ollama_api_url: str,
    ollama_model: str,
    conversation_history: List[Dict[str, str]],
    user_message_content: str
) -> Iterator[str]:
    """
    Handle streaming chat with Ollama.
    
    Args:
        ollama_api_url (str): URL of the Ollama API
        ollama_model (str): Model name to use
        conversation_history (List[Dict[str, str]]): Conversation history (modified in-place)
        user_message_content (str): User's message content
        
    Yields:
        str: Server-sent event formatted strings
    """
    # Add user message to history
    conversation_history.append({"role": "user", "content": user_message_content})

    # Trim conversation history if too long
    relevant_history = _trim_conversation_history(conversation_history)

    payload = {
        "model": ollama_model,
        "messages": relevant_history,
        "stream": True,
        "options": {"temperature": 0.7, "num_ctx": 2048}
    }

    full_chat_response = ""
    
    try:
        response = requests.post(
            ollama_api_url, 
            json=payload, 
            stream=True, 
            timeout=CHAT_TIMEOUT
        )
        response.raise_for_status()
        
        for line in response.iter_lines():
            if not line:
                continue
                
            decoded_line = line.decode('utf-8')
            
            try:
                json_chunk = json.loads(decoded_line)
                token = json_chunk.get("message", {}).get("content", "")
                
                if token:
                    full_chat_response += token
                    yield _format_sse_data({'token': token})
                    
                if json_chunk.get("done"):
                    conversation_history.append({
                        "role": "assistant", 
                        "content": full_chat_response
                    })
                    yield _format_sse_data({'status': 'done'})
                    break
                    
            except json.JSONDecodeError:
                print(f"Chat stream JSON decode error: {decoded_line}")
                
    except requests.exceptions.RequestException as e:
        error_msg = f"Error when chatting with Ollama: {str(e)}"
        print(error_msg)
        
        # Remove the user message if it was added but failed to process
        if (conversation_history and 
            conversation_history[-1]["role"] == "user" and 
            conversation_history[-1]["content"] == user_message_content):
            conversation_history.pop()
            
        yield _format_sse_data({'error': error_msg})


def _format_sse_data(data: Dict[str, Any]) -> str:
    """
    Format data as Server-Sent Event.
    
    Args:
        data (Dict[str, Any]): Data to format
        
    Returns:
        str: Formatted SSE string
    """
    return f"data: {json.dumps(data)}\n\n"


def _handle_api_error(
    stage_key: str, 
    error_message: str, 
    analysis_results_ref: Dict[str, str]
) -> None:
    """
    Handle API errors by logging and updating results.
    
    Args:
        stage_key (str): Analysis stage key
        error_message (str): Error message
        analysis_results_ref (Dict[str, str]): Reference to analysis results
    """
    print(error_message)
    analysis_results_ref[stage_key] = f"<p style='color:red;'>{error_message}</p>"


def _finalize_analysis_stage(
    stage_key: str,
    response_content: str,
    payload: Dict[str, Any],
    analysis_results_ref: Dict[str, str],
    conversation_history_ref: List[Dict[str, str]]
) -> None:
    """
    Finalize analysis stage by updating results and conversation history.
    
    Args:
        stage_key (str): Analysis stage key
        response_content (str): Full response content
        payload (Dict[str, Any]): Original request payload
        analysis_results_ref (Dict[str, str]): Reference to analysis results
        conversation_history_ref (List[Dict[str, str]]): Reference to conversation history
    """
    analysis_results_ref[stage_key] = response_content
    
    # Update conversation history for stage 3 (comprehensive analysis)
    if stage_key == "stage3_tonghop":
        if payload.get("messages"):
            conversation_history_ref[:] = list(payload["messages"])
            conversation_history_ref.append({
                "role": "assistant", 
                "content": response_content
            })
        else:
            conversation_history_ref[:] = [{
                "role": "assistant", 
                "content": response_content
            }]


def _trim_conversation_history(
    conversation_history: List[Dict[str, str]]
) -> List[Dict[str, str]]:
    """
    Trim conversation history to maintain reasonable length.
    
    Args:
        conversation_history (List[Dict[str, str]]): Full conversation history
        
    Returns:
        List[Dict[str, str]]: Trimmed conversation history
    """
    if len(conversation_history) > MAX_CHAT_HISTORY_MESSAGES:
        # Keep the first message and the most recent messages
        return ([conversation_history[0]] + 
                conversation_history[-(MAX_CHAT_HISTORY_MESSAGES-1):])
    return conversation_history