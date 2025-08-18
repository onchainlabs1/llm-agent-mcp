#!/usr/bin/env python3
"""
Phoenix Configuration for LLM Quality Evaluation
ISO/IEC 42001:2023 Compliance Dashboard

This file provides configuration and setup for Phoenix integration.
"""

import os
import subprocess
import time
import webbrowser
from pathlib import Path

def check_phoenix_installation():
    """Check if Phoenix is properly installed"""
    try:
        import phoenix
        print("✅ Phoenix is installed")
        return True
    except ImportError:
        print("❌ Phoenix not found. Install with: pip install arize-phoenix")
        return False

def start_phoenix_server():
    """Start Phoenix server in background"""
    try:
        # Check if Phoenix is already running
        import psutil
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            if proc.info['name'] and 'phoenix' in proc.info['name'].lower():
                print("✅ Phoenix server already running")
                return True
        
        # Start Phoenix server
        print("🚀 Starting Phoenix server...")
        process = subprocess.Popen(
            ["phoenix", "serve"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Wait a bit for server to start
        time.sleep(3)
        
        if process.poll() is None:
            print("✅ Phoenix server started successfully")
            return True
        else:
            print("❌ Failed to start Phoenix server")
            return False
            
    except Exception as e:
        print(f"❌ Error starting Phoenix: {e}")
        return False

def open_phoenix_interface():
    """Open Phoenix web interface in browser"""
    try:
        url = "http://localhost:6006"
        print(f"🌐 Opening Phoenix interface: {url}")
        webbrowser.open(url)
        return True
    except Exception as e:
        print(f"❌ Error opening browser: {e}")
        return False

def run_phoenix_demo():
    """Run a quick Phoenix demo"""
    try:
        from phoenix.evaluate import evaluate
        from phoenix.evaluate.llm_eval import llm_eval
        
        print("🧪 Running Phoenix demo...")
        
        # Sample evaluation
        sample_text = "The capital of France is Paris."
        result = evaluate(
            sample_text,
            criteria=["relevance", "toxicity"],
            evaluator="llm_eval"
        )
        
        print(f"✅ Demo completed. Sample evaluation result: {result}")
        return True
        
    except Exception as e:
        print(f"❌ Phoenix demo failed: {e}")
        return False

def main():
    """Main configuration function"""
    print("🔧 Phoenix Configuration for ISO 42001 Dashboard")
    print("=" * 50)
    
    # Check installation
    if not check_phoenix_installation():
        return
    
    # Start server
    if start_phoenix_server():
        print("\n📊 Phoenix is ready!")
        print("Dashboard URL: http://localhost:8501")
        print("Phoenix URL: http://localhost:6006")
        
        # Run demo
        run_phoenix_demo()
        
        # Open interface
        open_phoenix_interface()
        
        print("\n🎉 Setup complete! You can now:")
        print("1. Run your dashboard: streamlit run iso_dashboard.py")
        print("2. Access Phoenix: http://localhost:6006")
        print("3. Use the LLM Quality tab in your dashboard")
    else:
        print("❌ Phoenix setup failed")

if __name__ == "__main__":
    main()
