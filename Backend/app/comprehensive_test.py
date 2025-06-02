#!/usr/bin/env python3
"""
Comprehensive test và báo cáo về chức năng "Bấm phân tích"
"""

import requests
import json
import time

def test_analysis_mode(mode, enhanced=True, timeout=15):
    """Test một mode cụ thể"""
    url = f"http://localhost:5000/api/start-llm-analysis?mode={mode}&enhanced={enhanced}&cache=false&rag=false"
    
    try:
        print(f"🔄 Testing mode '{mode}' (enhanced={enhanced})...")
        
        start_time = time.time()
        response = requests.get(url, timeout=timeout, stream=True)
        
        if response.status_code == 200:
            messages_received = 0
            first_message_time = None
            last_message_time = None
            
            for line in response.iter_lines(decode_unicode=True):
                if line.startswith('data: '):
                    data_str = line[6:]
                    try:
                        data = json.loads(data_str)
                        messages_received += 1
                        
                        if messages_received == 1:
                            first_message_time = time.time()
                        last_message_time = time.time()
                        
                        # Hiển thị một số messages đầu
                        if messages_received <= 3:
                            print(f"  📦 {data}")
                            
                        # Stop early for quick test
                        if messages_received >= 5 or data.get('status') in ['template_complete', 'all_done', 'error']:
                            break
                            
                    except json.JSONDecodeError:
                        continue
                        
            total_time = last_message_time - start_time if last_message_time else 0
            response_time = first_message_time - start_time if first_message_time else 0
            
            return {
                'success': True,
                'messages_received': messages_received,
                'total_time': round(total_time, 2),
                'first_response_time': round(response_time, 2)
            }
        else:
            return {'success': False, 'error': f'HTTP {response.status_code}'}
            
    except requests.exceptions.Timeout:
        return {'success': False, 'error': 'Timeout'}
    except Exception as e:
        return {'success': False, 'error': str(e)}

def main():
    print("=" * 60)
    print("🚀 COMPREHENSIVE TEST - 'BẤM PHÂN TÍCH' FUNCTION")
    print("=" * 60)
    
    # Test các modes khác nhau
    modes_to_test = [
        ('template', True),
        ('quick', True), 
        ('basic', False),
        ('enhanced', True),
    ]
    
    results = {}
    
    for mode, enhanced in modes_to_test:
        result = test_analysis_mode(mode, enhanced, timeout=20)
        results[f"{mode}_enhanced_{enhanced}"] = result
        
        if result['success']:
            print(f"  ✅ Success: {result['messages_received']} messages, "
                  f"first response: {result['first_response_time']}s, "
                  f"total: {result['total_time']}s")
        else:
            print(f"  ❌ Failed: {result['error']}")
        print()
    
    # Tổng kết
    print("=" * 60)
    print("📊 SUMMARY REPORT")
    print("=" * 60)
    
    successful_modes = [k for k, v in results.items() if v['success']]
    failed_modes = [k for k, v in results.items() if not v['success']]
    
    print(f"✅ Successful modes ({len(successful_modes)}):")
    for mode in successful_modes:
        result = results[mode]
        print(f"  - {mode}: {result['first_response_time']}s response time")
    
    if failed_modes:
        print(f"\n❌ Failed modes ({len(failed_modes)}):")
        for mode in failed_modes:
            result = results[mode]
            print(f"  - {mode}: {result['error']}")
    
    # Performance analysis
    if successful_modes:
        avg_response_time = sum(results[m]['first_response_time'] for m in successful_modes) / len(successful_modes)
        print(f"\n⚡ Average first response time: {avg_response_time:.2f}s")
        
        fastest = min(successful_modes, key=lambda m: results[m]['first_response_time'])
        print(f"🏆 Fastest mode: {fastest} ({results[fastest]['first_response_time']}s)")
    
    print("\n" + "=" * 60)
    if len(successful_modes) >= 3:
        print("🎉 OVERALL STATUS: GOOD - Chức năng 'Bấm phân tích' hoạt động tốt!")
    elif len(successful_modes) >= 1:
        print("⚠️  OVERALL STATUS: PARTIAL - Một số mode hoạt động")
    else:
        print("❌ OVERALL STATUS: FAILED - Cần sửa lỗi")
    print("=" * 60)

if __name__ == "__main__":
    main()
