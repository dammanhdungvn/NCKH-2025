#!/usr/bin/env python3
"""
Comprehensive Testing Script for Enhanced Education Consultant System
Tests all AI features including RAG, Cache, Templates, and Enhanced Prompts
"""

import json
import requests
import time
import sys
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:5000"
TEST_DATA_FILE = "test_results.json"

def test_basic_endpoints():
    """Test basic system endpoints"""
    print("🔍 Testing Basic Endpoints...")
    
    endpoints = [
        ("/api/get-khaosat-summary", "GET"),
        ("/api/get-simplified-data", "GET"),
        ("/api/system-stats", "GET"),
        ("/api/response-mode", "GET")
    ]
    
    results = {}
    
    for endpoint, method in endpoints:
        try:
            if method == "GET":
                response = requests.get(f"{BASE_URL}{endpoint}")
            else:
                response = requests.post(f"{BASE_URL}{endpoint}")
            
            if response.status_code == 200:
                results[endpoint] = {
                    "status": "✅ SUCCESS",
                    "response_time": response.elapsed.total_seconds(),
                    "data_preview": str(response.json())[:200] + "..."
                }
                print(f"  ✅ {endpoint}: {response.status_code}")
            else:
                results[endpoint] = {
                    "status": "❌ FAILED",
                    "status_code": response.status_code,
                    "error": response.text[:200]
                }
                print(f"  ❌ {endpoint}: {response.status_code}")
                
        except Exception as e:
            results[endpoint] = {
                "status": "❌ ERROR",
                "error": str(e)
            }
            print(f"  ❌ {endpoint}: {str(e)}")
    
    return results

def test_quick_response():
    """Test quick template response system"""
    print("🚀 Testing Quick Response Templates...")
    
    try:
        response = requests.post(f"{BASE_URL}/api/quick-response", 
                               json={}, 
                               timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            print(f"  ✅ Quick Response: {data.get('template_name', 'Unknown')}")
            print(f"  📊 Confidence: {data.get('confidence', 0)}%")
            print(f"  ⚡ Response Time: {data.get('metadata', {}).get('response_time', 0):.3f}s")
            return {
                "status": "✅ SUCCESS",
                "template_name": data.get('template_name'),
                "confidence": data.get('confidence'),
                "response_preview": data.get('response', '')[:200] + "..."
            }
        else:
            print(f"  ❌ Quick Response failed: {response.status_code}")
            return {"status": "❌ FAILED", "error": response.text}
            
    except Exception as e:
        print(f"  ❌ Quick Response error: {str(e)}")
        return {"status": "❌ ERROR", "error": str(e)}

def test_enhanced_analysis():
    """Test enhanced analysis with different modes"""
    print("🧠 Testing Enhanced Analysis...")
    
    modes = ["template", "quick", "enhanced"]
    results = {}
    
    for mode in modes:
        print(f"  Testing mode: {mode}")
        try:
            response = requests.post(f"{BASE_URL}/api/enhanced-analysis",
                                   json={
                                       "response_mode": mode,
                                       "use_cache": True,
                                       "use_rag": True,
                                       "stage": "stage1"
                                   },
                                   timeout=60)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('requires_llm'):
                    print(f"    🔄 {mode}: Requires LLM call")
                    results[mode] = {
                        "status": "🔄 REQUIRES_LLM",
                        "payload_ready": True,
                        "cache_enabled": data.get('cache_enabled', False)
                    }
                else:
                    print(f"    ✅ {mode}: Instant response")
                    results[mode] = {
                        "status": "✅ SUCCESS",
                        "response_source": data.get('metadata', {}).get('source', 'unknown'),
                        "response_time": data.get('metadata', {}).get('response_time', 0),
                        "response_preview": data.get('response', '')[:200] + "..."
                    }
            else:
                print(f"    ❌ {mode}: Failed {response.status_code}")
                results[mode] = {"status": "❌ FAILED", "error": response.text}
                
        except Exception as e:
            print(f"    ❌ {mode}: Error {str(e)}")
            results[mode] = {"status": "❌ ERROR", "error": str(e)}
    
    return results

def test_knowledge_base():
    """Test RAG knowledge base functionality"""
    print("📚 Testing Knowledge Base (RAG)...")
    
    try:
        # Test search
        response = requests.get(f"{BASE_URL}/api/knowledge-base",
                              params={"query": "học tập", "top_k": 3},
                              timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            print(f"  ✅ Knowledge Search: Found {len(data.get('results', []))} results")
            print(f"  📖 Total Documents: {data.get('total_documents', 0)}")
            
            # Test add knowledge
            add_response = requests.post(f"{BASE_URL}/api/knowledge-base",
                                       json={
                                           "content": "Test knowledge for education consultation",
                                           "metadata": {"test": True, "timestamp": datetime.now().isoformat()}
                                       },
                                       timeout=30)
            
            if add_response.status_code == 200:
                add_data = add_response.json()
                print(f"  ✅ Knowledge Add: New total {add_data.get('total_documents', 0)}")
                
                return {
                    "status": "✅ SUCCESS",
                    "search_results": len(data.get('results', [])),
                    "total_documents": add_data.get('total_documents', 0),
                    "add_successful": True
                }
            else:
                return {
                    "status": "⚠️ PARTIAL",
                    "search_results": len(data.get('results', [])),
                    "add_failed": add_response.text
                }
        else:
            print(f"  ❌ Knowledge Base failed: {response.status_code}")
            return {"status": "❌ FAILED", "error": response.text}
            
    except Exception as e:
        print(f"  ❌ Knowledge Base error: {str(e)}")
        return {"status": "❌ ERROR", "error": str(e)}

def test_streaming_analysis():
    """Test streaming LLM analysis"""
    print("🌊 Testing Streaming Analysis...")
    
    try:
        # Start streaming analysis
        response = requests.get(f"{BASE_URL}/api/start-llm-analysis",
                              params={"enhanced": "true", "mode": "quick"},
                              stream=True,
                              timeout=120)
        
        if response.status_code == 200:
            chunks_received = 0
            stages_completed = []
            
            print("  📡 Receiving stream...")
            for line in response.iter_lines(decode_unicode=True):
                if line.startswith('data: '):
                    try:
                        data = json.loads(line[6:])  # Remove 'data: ' prefix
                        
                        if 'stage' in data:
                            stage = data['stage']
                            if stage not in stages_completed and stage.startswith('stage'):
                                stages_completed.append(stage)
                                print(f"    ✅ Stage completed: {stage}")
                        
                        chunks_received += 1
                        
                        # Stop after reasonable amount of data or completion
                        if chunks_received > 50 or data.get('status') == 'all_done':
                            break
                            
                    except json.JSONDecodeError:
                        continue
            
            print(f"  ✅ Streaming complete: {chunks_received} chunks, {len(stages_completed)} stages")
            return {
                "status": "✅ SUCCESS",
                "chunks_received": chunks_received,
                "stages_completed": stages_completed
            }
        else:
            print(f"  ❌ Streaming failed: {response.status_code}")
            return {"status": "❌ FAILED", "error": response.text}
            
    except Exception as e:
        print(f"  ❌ Streaming error: {str(e)}")
        return {"status": "❌ ERROR", "error": str(e)}

def test_cache_system():
    """Test cache feedback system"""
    print("💾 Testing Cache System...")
    
    try:
        # Test cache feedback
        response = requests.post(f"{BASE_URL}/api/cache-feedback",
                               json={
                                   "signature": "test_signature_123",
                                   "stage": "stage1",
                                   "response": "Test response for caching",
                                   "feedback_score": 5
                               },
                               timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            print(f"  ✅ Cache Feedback: {data.get('message')}")
            print(f"  💾 Cached: {data.get('cached', False)}")
            
            return {
                "status": "✅ SUCCESS",
                "cached": data.get('cached', False),
                "message": data.get('message')
            }
        else:
            print(f"  ❌ Cache failed: {response.status_code}")
            return {"status": "❌ FAILED", "error": response.text}
            
    except Exception as e:
        print(f"  ❌ Cache error: {str(e)}")
        return {"status": "❌ ERROR", "error": str(e)}

def run_comprehensive_test():
    """Run all tests and generate report"""
    print("🚀 Enhanced Education Consultant - Comprehensive Test Suite")
    print("=" * 70)
    print(f"🕐 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🌐 Base URL: {BASE_URL}")
    print("=" * 70)
    
    test_results = {
        "test_timestamp": datetime.now().isoformat(),
        "base_url": BASE_URL,
        "tests": {}
    }
    
    # Run all tests
    test_results["tests"]["basic_endpoints"] = test_basic_endpoints()
    print()
    
    test_results["tests"]["quick_response"] = test_quick_response()
    print()
    
    test_results["tests"]["enhanced_analysis"] = test_enhanced_analysis()
    print()
    
    test_results["tests"]["knowledge_base"] = test_knowledge_base()
    print()
    
    test_results["tests"]["cache_system"] = test_cache_system()
    print()
    
    test_results["tests"]["streaming_analysis"] = test_streaming_analysis()
    print()
    
    # Generate summary
    print("=" * 70)
    print("📊 TEST SUMMARY")
    print("=" * 70)
    
    total_tests = 0
    passed_tests = 0
    
    for test_name, test_data in test_results["tests"].items():
        print(f"🧪 {test_name.replace('_', ' ').title()}:")
        
        if isinstance(test_data, dict):
            if "status" in test_data:
                status = test_data["status"]
                print(f"   {status}")
                total_tests += 1
                if "✅" in status:
                    passed_tests += 1
            else:
                # Multiple sub-tests
                sub_passed = 0
                sub_total = 0
                for sub_test, sub_result in test_data.items():
                    if isinstance(sub_result, dict) and "status" in sub_result:
                        sub_total += 1
                        status = sub_result["status"]
                        if "✅" in status:
                            sub_passed += 1
                        print(f"   {sub_test}: {status}")
                
                total_tests += sub_total
                passed_tests += sub_passed
        print()
    
    success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
    test_results["summary"] = {
        "total_tests": total_tests,
        "passed_tests": passed_tests,
        "success_rate": success_rate
    }
    
    print(f"✅ Passed: {passed_tests}/{total_tests} ({success_rate:.1f}%)")
    print("=" * 70)
    
    # Save results
    with open(TEST_DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(test_results, f, ensure_ascii=False, indent=2)
    
    print(f"📁 Test results saved to: {TEST_DATA_FILE}")
    
    if success_rate >= 80:
        print("🎉 SYSTEM STATUS: EXCELLENT - AI features working properly!")
        return 0
    elif success_rate >= 60:
        print("⚠️ SYSTEM STATUS: GOOD - Some features may need attention")
        return 1
    else:
        print("❌ SYSTEM STATUS: NEEDS ATTENTION - Multiple failures detected")
        return 2

if __name__ == "__main__":
    exit(run_comprehensive_test())
