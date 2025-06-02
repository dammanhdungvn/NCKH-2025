#!/usr/bin/env python3
"""
Debug script để tìm lỗi trong chức năng "Bấm phân tích"
"""

import sys
import traceback
import json
from datetime import datetime

def debug_imports():
    """Debug import errors"""
    print("🔍 DEBUGGING IMPORTS...")
    
    try:
        from flask import Flask, request, jsonify, Response
        print("✅ Flask imported successfully")
    except Exception as e:
        print(f"❌ Flask import error: {e}")
        return False
    
    try:
        from LLM.enhanced_prompts import EnhancedEducationConsultant
        print("✅ EnhancedEducationConsultant imported successfully")
    except Exception as e:
        print(f"❌ EnhancedEducationConsultant import error: {e}")
        traceback.print_exc()
        return False
        
    try:
        from LLM.cache_system import SmartCacheSystem
        print("✅ SmartCacheSystem imported successfully")
    except Exception as e:
        print(f"❌ SmartCacheSystem import error: {e}")
        return False
        
    return True

def debug_enhanced_consultant():
    """Debug enhanced consultant initialization"""
    print("\n🔍 DEBUGGING ENHANCED CONSULTANT...")
    
    try:
        from LLM.enhanced_prompts import EnhancedEducationConsultant
        consultant = EnhancedEducationConsultant()
        print("✅ EnhancedEducationConsultant created successfully")
        
        # Check cache system
        if hasattr(consultant, 'cache_system'):
            print("✅ Cache system exists")
            cache = consultant.cache_system
            
            # Check required methods
            required_methods = ['get_cached_response', 'cache_response', 'generate_student_signature']
            for method in required_methods:
                if hasattr(cache, method):
                    print(f"✅ Method {method} exists")
                else:
                    print(f"❌ Method {method} MISSING")
        else:
            print("❌ Cache system MISSING")
            
        return consultant
    except Exception as e:
        print(f"❌ Error creating consultant: {e}")
        traceback.print_exc()
        return None

def debug_stage1_consultation():
    """Debug stage1 consultation method"""
    print("\n🔍 DEBUGGING STAGE 1 CONSULTATION...")
    
    try:
        consultant = debug_enhanced_consultant()
        if not consultant:
            return False
            
        # Test data
        test_khaosat = {
            "thong_tin_ca_nhan": {"khoa": "CNTT"},
            "Thai_do_hoc_tap": {"phan_tram_diem": 75},
            "Su_dung_mang_xa_hoi": {"phan_tram_diem": 65}
        }
        
        print("🔄 Testing enhanced_stage1_consultation...")
        result = consultant.enhanced_stage1_consultation(
            test_khaosat, "gemma3:latest", use_cache=False, use_rag=False
        )
        
        print(f"✅ Stage1 consultation result type: {type(result)}")
        print(f"✅ Stage1 consultation keys: {list(result.keys()) if isinstance(result, dict) else 'Not a dict'}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in stage1 consultation: {e}")
        traceback.print_exc()
        return False

def debug_template_system():
    """Debug template system"""
    print("\n🔍 DEBUGGING TEMPLATE SYSTEM...")
    
    try:
        from LLM.quick_response_templates import QuickResponseTemplates, quick_templates
        print("✅ QuickResponseTemplates imported successfully")
        
        # Test template generation
        test_data = {
            "skills_avg": 75,
            "grades_avg": 80,
            "weak_skills_detail": {"Thai_do_hoc_tap": 60},
            "major": "CNTT"
        }
        
        template_response = quick_templates.generate_quick_response(test_data)
        if template_response:
            print("✅ Template response generated successfully")
            print(f"Template name: {template_response.get('template_name', 'N/A')}")
        else:
            print("❌ No template response generated")
            
        return True
        
    except Exception as e:
        print(f"❌ Error in template system: {e}")
        traceback.print_exc()
        return False

def main():
    print("=" * 50)
    print("🚀 DEBUGGING 'BẤM PHÂN TÍCH' FUNCTION")
    print("=" * 50)
    
    # Step by step debugging
    if not debug_imports():
        print("❌ Import errors found. Cannot continue.")
        return
        
    debug_enhanced_consultant()
    debug_stage1_consultation() 
    debug_template_system()
    
    print("\n" + "=" * 50)
    print("✅ DEBUG COMPLETED")
    print("=" * 50)

if __name__ == "__main__":
    main()
