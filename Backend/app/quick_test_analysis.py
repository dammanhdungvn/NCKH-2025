#!/usr/bin/env python3
"""
Quick test cho chức năng "Bấm phân tích"
"""

import requests
import json
import time

def test_analysis_endpoint():
    """Test endpoint /api/start-llm-analysis"""
    base_url = "http://localhost:5000"
    
    print("🔍 Testing Analysis Endpoint...")
    
    # Test với mode basic trước
    test_url = f"{base_url}/api/start-llm-analysis?mode=basic&enhanced=false&cache=false&rag=false"
    
    try:
        print(f"📡 Calling: {test_url}")
        response = requests.get(test_url, timeout=30, stream=True)
        
        if response.status_code == 200:
            print("✅ Response received. Streaming content:")
            
            content_received = False
            for line in response.iter_lines(decode_unicode=True):
                if line.startswith('data: '):
                    data_str = line[6:]  # Remove 'data: ' prefix
                    try:
                        data = json.loads(data_str)
                        print(f"📦 {data}")
                        content_received = True
                        
                        # Stop after a few messages to avoid flooding
                        if data.get('status') in ['all_done', 'error']:
                            break
                            
                    except json.JSONDecodeError:
                        print(f"⚠️ Non-JSON data: {data_str}")
                        
            if not content_received:
                print("❌ No streaming content received")
        else:
            print(f"❌ HTTP {response.status_code}: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

def test_system_status():
    """Test system status endpoints"""
    base_url = "http://localhost:5000"
    
    try:
        # Test basic connectivity
        response = requests.get(f"{base_url}/api/system-stats", timeout=10)
        if response.status_code == 200:
            print("✅ System stats endpoint working")
            stats = response.json()
            print(f"📊 Stats: {json.dumps(stats, indent=2)}")
        else:
            print(f"❌ System stats failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ System stats error: {e}")

def main():
    print("=" * 50)
    print("🚀 QUICK TEST - 'BẤM PHÂN TÍCH' FUNCTION")
    print("=" * 50)
    
    test_system_status()
    print("\n" + "-" * 30)
    test_analysis_endpoint()
    
    print("\n" + "=" * 50)
    print("✅ QUICK TEST COMPLETED")
    print("=" * 50)

if __name__ == "__main__":
    main()
