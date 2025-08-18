#!/usr/bin/env python3
"""
Test Script for Phoenix Integration
Test the Phoenix integration locally before running the full dashboard
"""

import streamlit as st
import sys
import os

def test_phoenix_imports():
    """Test if Phoenix imports work correctly"""
    print("🧪 Testing Phoenix imports...")
    
    try:
        from phoenix import trace, evals
        print("✅ phoenix.trace and phoenix.evals imported successfully")
    except ImportError as e:
        print(f"❌ phoenix.trace/evals import failed: {e}")
        return False
    
    try:
        from phoenix.evals import LLMEvaluator, RelevanceEvaluator, ToxicityEvaluator
        print("✅ phoenix.evals evaluators imported successfully")
    except ImportError as e:
        print(f"❌ phoenix.evals evaluators import failed: {e}")
        return False
    
    return True

def test_phoenix_functions():
    """Test Phoenix functions from the dashboard"""
    print("\n🧪 Testing Phoenix functions...")
    
    try:
        # Import the functions from the dashboard
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        
        # Test the quality check function
        from iso_dashboard import run_phoenix_quality_check, display_phoenix_results
        
        print("✅ Dashboard functions imported successfully")
        
        # Test quality check
        results = run_phoenix_quality_check()
        if results:
            print(f"✅ Quality check returned {len(results)} results")
            for i, result in enumerate(results):
                print(f"  Result {i+1}: Quality={result['quality_score']}, Risk={result['hallucination_risk']}")
        else:
            print("⚠️ Quality check returned no results")
        
        return True
        
    except Exception as e:
        print(f"❌ Function test failed: {e}")
        return False

def test_streamlit_integration():
    """Test if Streamlit can run with Phoenix"""
    print("\n🧪 Testing Streamlit integration...")
    
    try:
        # Test basic Streamlit functionality
        st.set_page_config(page_title="Phoenix Test", page_icon="🧪")
        st.title("🧪 Phoenix Integration Test")
        
        # Test Phoenix status
        try:
            from phoenix.trace import trace
            st.success("✅ Phoenix is available!")
            phoenix_available = True
        except ImportError:
            st.warning("⚠️ Phoenix not available")
            phoenix_available = False
        
        # Test dashboard functions
        if phoenix_available:
            st.subheader("Testing Dashboard Functions")
            
            if st.button("🔍 Test Quality Check"):
                try:
                    from iso_dashboard import run_phoenix_quality_check
                    results = run_phoenix_quality_check()
                    if results:
                        st.success(f"✅ Quality check successful! {len(results)} results")
                        st.json(results)
                    else:
                        st.warning("⚠️ Quality check returned no results")
                except Exception as e:
                    st.error(f"❌ Quality check failed: {e}")
        
        st.info("🎉 Streamlit integration test completed!")
        return True
        
    except Exception as e:
        print(f"❌ Streamlit test failed: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 Phoenix Integration Test Suite")
    print("=" * 40)
    
    # Test 1: Imports
    imports_ok = test_phoenix_imports()
    
    # Test 2: Functions
    functions_ok = test_phoenix_functions() if imports_ok else False
    
    # Test 3: Streamlit
    streamlit_ok = test_streamlit_integration() if functions_ok else False
    
    # Summary
    print("\n" + "=" * 40)
    print("📊 Test Results Summary:")
    print(f"  Imports: {'✅ PASS' if imports_ok else '❌ FAIL'}")
    print(f"  Functions: {'✅ PASS' if functions_ok else '❌ FAIL'}")
    print(f"  Streamlit: {'✅ PASS' if streamlit_ok else '❌ FAIL'}")
    
    if all([imports_ok, functions_ok, streamlit_ok]):
        print("\n🎉 All tests passed! Phoenix integration is ready.")
        print("\n🚀 Next steps:")
        print("  1. Start Phoenix server: phoenix serve")
        print("  2. Run dashboard: streamlit run iso_dashboard.py")
        print("  3. Test the LLM Quality tab")
    else:
        print("\n❌ Some tests failed. Check the errors above.")
        print("\n🔧 Troubleshooting:")
        print("  1. Ensure Phoenix is installed: pip install arize-phoenix")
        print("  2. Check Python path and dependencies")
        print("  3. Restart your terminal/IDE")

if __name__ == "__main__":
    main()
