#!/usr/bin/env python3
"""
Simple test script to verify AI system functionality
"""
import requests
import json
import time

BASE_URL = "http://localhost:5000"

def test_basic_functionality():
    """Test basic endpoints to ensure system is working"""
    print("🔍 Testing Enhanced Education Consultant System")
    print("=" * 50)
    
    # Test 1: System Stats
    try:
        response = requests.get(f"{BASE_URL}/api/system-stats", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("✅ System Stats:")
            print(f"   📊 Total consultations: {data['enhanced_consultant']['total_consultations']}")
            print(f"   📚 Knowledge base: {data['enhanced_consultant']['rag_knowledge_count']} documents")
            print(f"   🎯 Templates available: {data['template_system']['total_templates']}")
            print(f"   💾 Cache hit rate: {data['enhanced_consultant']['cache_hit_rate']}")
        else:
            print(f"❌ System Stats failed: {response.status_code}")
    except Exception as e:
        print(f"❌ System Stats error: {e}")
    
    print()
    
    # Test 2: Response Mode
    try:
        response = requests.get(f"{BASE_URL}/api/response-mode", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("✅ Response Mode:")
            print(f"   🎛️ Current mode: {data['current_mode']}")
            print(f"   🔧 Available modes: {', '.join(data['available_modes'])}")
        else:
            print(f"❌ Response Mode failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Response Mode error: {e}")
    
    print()
    
    # Test 3: Data Endpoints
    try:
        response = requests.get(f"{BASE_URL}/api/get-khaosat-summary", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("✅ Survey Data:")
            if 'thong_tin_ca_nhan' in data:
                print(f"   👤 Student: {data['thong_tin_ca_nhan'].get('ho_ten', 'N/A')}")
                print(f"   🏢 Department: {data['thong_tin_ca_nhan'].get('khoa', 'N/A')}")
            print(f"   📝 Data fields: {len(data)} sections")
        else:
            print(f"❌ Survey Data failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Survey Data error: {e}")
    
    print()
    
    # Test 4: Simplified Grades
    try:
        response = requests.get(f"{BASE_URL}/api/get-simplified-data", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("✅ Grade Data:")
            print(f"   📊 Records available: {len(data) if isinstance(data, list) else 1}")
            if isinstance(data, list) and len(data) > 0:
                first_record = data[0]
                if 'subjects' in first_record:
                    print(f"   📚 Subjects tracked: {len(first_record['subjects'])}")
                    print(f"   🎯 GPA: {first_record.get('gpa', 'N/A')}")
        else:
            print(f"❌ Grade Data failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Grade Data error: {e}")
    
    print()
    
    # Test 5: Quick Template Response
    try:
        response = requests.post(f"{BASE_URL}/api/quick-response", 
                               json={},
                               timeout=15)
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print("✅ Quick Response:")
                print(f"   🎯 Template: {data.get('template_name', 'N/A')}")
                print(f"   📊 Confidence: {data.get('confidence', 0)}%")
                print(f"   📝 Response length: {len(data.get('response', ''))} chars")
            else:
                print("⚠️ Quick Response (no template match):")
                templates = data.get('available_templates', [])
                print(f"   📋 Available templates: {len(templates)}")
        else:
            print(f"❌ Quick Response failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Quick Response error: {e}")
    
    print()
    print("=" * 50)
    print("🎉 Basic functionality test completed!")
    print()
    print("💡 Next steps:")
    print("   1. Test streaming analysis at: /api/start-llm-analysis")
    print("   2. Try enhanced analysis modes")
    print("   3. Test knowledge base search")
    print("   4. Experiment with different response modes")
    
if __name__ == "__main__":
    test_basic_functionality()
