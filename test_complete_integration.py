#!/usr/bin/env python3
"""
Complete Phoenix Integration Test
Tests all aspects of the Phoenix + Dashboard integration
"""

import time
import requests
import json
import os
from datetime import datetime

def test_phoenix_server():
    """Test if Phoenix server is responding"""
    print("🔍 Testing Phoenix Server...")
    
    try:
        response = requests.get("http://localhost:6006", timeout=5)
        if response.status_code == 200:
            print("✅ Phoenix server is running and responding")
            return True
        else:
            print(f"⚠️ Phoenix server responded with status: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Phoenix server not accessible: {e}")
        return False

def test_dashboard():
    """Test if Streamlit dashboard is responding"""
    print("🔍 Testing Streamlit Dashboard...")
    
    try:
        response = requests.get("http://localhost:8503", timeout=5)
        if response.status_code == 200:
            print("✅ Streamlit dashboard is running and responding")
            return True
        else:
            print(f"⚠️ Dashboard responded with status: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Dashboard not accessible: {e}")
        return False

def test_phoenix_data():
    """Test if Phoenix data files exist and are valid"""
    print("🔍 Testing Phoenix Data Files...")
    
    data_files = [
        "data/phoenix/llm_traces.csv",
        "data/phoenix/llm_traces.json",
        "data/phoenix/quality_trends.csv",
        "data/phoenix/quality_trends.json"
    ]
    
    all_exist = True
    for file_path in data_files:
        if os.path.exists(file_path):
            file_size = os.path.getsize(file_path)
            print(f"✅ {file_path} exists ({file_size} bytes)")
        else:
            print(f"❌ {file_path} missing")
            all_exist = False
    
    return all_exist

def test_data_content():
    """Test the content of generated data"""
    print("🔍 Testing Data Content...")
    
    try:
        # Test CSV data
        import pandas as pd
        
        # LLM traces
        if os.path.exists("data/phoenix/llm_traces.csv"):
            df_traces = pd.read_csv("data/phoenix/llm_traces.csv")
            print(f"✅ LLM traces CSV: {len(df_traces)} rows, {len(df_traces.columns)} columns")
            print(f"   Columns: {list(df_traces.columns)}")
            
            if len(df_traces) > 0:
                latest_trace = df_traces.iloc[0]
                print(f"   Latest trace: Quality={latest_trace['quality_score']}, Risk={latest_trace['hallucination_risk']}")
        
        # Quality trends
        if os.path.exists("data/phoenix/quality_trends.csv"):
            df_quality = pd.read_csv("data/phoenix/quality_trends.csv")
            print(f"✅ Quality trends CSV: {len(df_quality)} rows, {len(df_quality.columns)} columns")
            
            if len(df_quality) > 0:
                latest_quality = df_quality.iloc[-1]
                print(f"   Latest quality: Score={latest_quality['quality_score']}, Requests={latest_quality['total_requests']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Data content test failed: {e}")
        return False

def generate_additional_data():
    """Generate additional test data"""
    print("🔍 Generating Additional Test Data...")
    
    try:
        # Run the data generation script
        import subprocess
        result = subprocess.run(["python3", "generate_phoenix_data.py"], 
                              capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ Additional data generated successfully")
            return True
        else:
            print(f"⚠️ Data generation had issues: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Data generation failed: {e}")
        return False

def run_complete_test():
    """Run the complete integration test"""
    print("🚀 Complete Phoenix Integration Test")
    print("=" * 50)
    
    tests = [
        ("Phoenix Server", test_phoenix_server),
        ("Streamlit Dashboard", test_dashboard),
        ("Phoenix Data Files", test_phoenix_data),
        ("Data Content", test_data_content),
        ("Additional Data Generation", generate_additional_data)
    ]
    
    results = {}
    for test_name, test_func in tests:
        print(f"\n📋 Running: {test_name}")
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results[test_name] = False
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    
    passed = sum(results.values())
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {test_name}: {status}")
    
    print(f"\n🎯 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Integration is working perfectly!")
        print("\n🌐 Your setup is ready:")
        print("  1. Phoenix UI: http://localhost:6006")
        print("  2. Dashboard: http://localhost:8503")
        print("  3. Navigate to '🔍 LLM Quality' tab")
        print("  4. Click '🔄 Refresh Data' to see real data")
        print("  5. Click '📊 Show Quality Trends' for charts")
    else:
        print(f"\n⚠️ {total - passed} test(s) failed. Check the errors above.")
        print("\n🔧 Troubleshooting:")
        print("  1. Ensure Phoenix server is running: phoenix serve")
        print("  2. Ensure Dashboard is running: streamlit run iso_dashboard.py --server.port 8503")
        print("  3. Check data files in data/phoenix/")
        print("  4. Run: python3 generate_phoenix_data.py")
    
    return results

if __name__ == "__main__":
    run_complete_test()
