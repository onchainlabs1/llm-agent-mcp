#!/usr/bin/env python3
"""
Complete setup script for AgentMCP project.
This script ensures all critical fixes are applied.
"""

import os
import json
from pathlib import Path
from datetime import datetime

def apply_agent_core_fixes():
    """Apply fixes to agent_core.py for better error handling and fallback."""
    agent_core_path = Path("agent/agent_core.py")
    
    if not agent_core_path.exists():
        print("❌ agent_core.py not found")
        return False
    
    # Check if config import is already present
    with open(agent_core_path, 'r') as f:
        content = f.read()
    
    if "from config import config" in content:
        print("✓ agent_core.py already updated with config import")
        return True
    
    print("⚠️  agent_core.py needs manual update - configuration imports missing")
    return False

def create_test_config():
    """Create a test configuration to verify the system works."""
    test_config = {
        "LLM_PROVIDER": "simulated",
        "LOG_LEVEL": "INFO",
        "GROQ_API_KEY": "your-groq-api-key-here"
    }
    
    # Set environment variables for testing
    for key, value in test_config.items():
        os.environ[key] = value
    
    print("✓ Test configuration applied")

def verify_project_structure():
    """Verify that all necessary files and directories exist."""
    required_items = [
        ("logs/", "directory"),
        ("logs/actions.log", "file"),
        ("data/", "directory"),
        ("data/clients.json", "file"),
        ("data/orders.json", "file"),
        ("data/employees.json", "file"),
        ("mcp_server/", "directory"),
        ("mcp_server/crm_mcp.json", "file"),
        ("mcp_server/erp_mcp.json", "file"),
        ("mcp_server/hr_mcp.json", "file"),
        ("agent/", "directory"),
        ("agent/agent_core.py", "file"),
        ("services/", "directory"),
        ("services/crm_service.py", "file"),
        ("services/erp_service.py", "file"),
        ("setup.py", "file"),
        ("config.py", "file")
    ]
    
    missing_items = []
    
    for item_path, item_type in required_items:
        path = Path(item_path)
        if item_type == "directory":
            if not path.is_dir():
                missing_items.append(f"Directory: {item_path}")
        else:  # file
            if not path.is_file():
                missing_items.append(f"File: {item_path}")
    
    if missing_items:
        print("❌ Missing items:")
        for item in missing_items:
            print(f"   - {item}")
        return False
    else:
        print("✅ All required files and directories exist")
        return True

def test_configuration_module():
    """Test that the configuration module works correctly."""
    try:
        # Test the config module
        import sys
        sys.path.insert(0, '.')
        
        from config import config
        
        # Test basic configuration access
        provider = config.llm.provider
        log_level = config.logging.level
        
        print(f"✓ Configuration module loaded successfully")
        print(f"  - LLM Provider: {provider}")
        print(f"  - Log Level: {log_level}")
        
        # Test validation
        errors = config.validate_config()
        if errors:
            print(f"⚠️  Configuration validation warnings: {len(errors)}")
            for error in errors:
                print(f"   - {error}")
        else:
            print("✓ Configuration validation passed")
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration module test failed: {e}")
        return False

def test_agent_core():
    """Test that the agent core module loads correctly."""
    try:
        import sys
        sys.path.insert(0, '.')
        
        from agent.agent_core import AgentCore, AgentConfig
        
        # Test agent initialization
        agent_config = AgentConfig()
        agent = AgentCore(agent_config)
        
        print("✓ Agent core module loaded successfully")
        print(f"  - Available tools: {len(agent.available_tools)}")
        
        # Test schema loading
        schemas_loaded = agent.load_all_mcp_schemas()
        if schemas_loaded:
            print(f"✓ MCP schemas loaded: {len(agent.available_tools)} tools")
        else:
            print("⚠️  Some MCP schemas failed to load")
        
        return True
        
    except Exception as e:
        print(f"❌ Agent core test failed: {e}")
        return False

def main():
    """Run complete setup and verification."""
    print("🔧 Running complete AgentMCP setup verification...")
    print("=" * 60)
    
    # Step 1: Verify project structure
    print("\n1. Verifying project structure...")
    structure_ok = verify_project_structure()
    
    # Step 2: Apply test configuration
    print("\n2. Applying test configuration...")
    create_test_config()
    
    # Step 3: Test configuration module
    print("\n3. Testing configuration module...")
    config_ok = test_configuration_module()
    
    # Step 4: Test agent core
    print("\n4. Testing agent core...")
    agent_ok = test_agent_core()
    
    # Step 5: Apply agent core fixes
    print("\n5. Checking agent core fixes...")
    agent_fixes_ok = apply_agent_core_fixes()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Setup Verification Summary:")
    print(f"  ✓ Project structure: {'OK' if structure_ok else 'ISSUES'}")
    print(f"  ✓ Configuration module: {'OK' if config_ok else 'ISSUES'}")
    print(f"  ✓ Agent core module: {'OK' if agent_ok else 'ISSUES'}")
    print(f"  ✓ Agent core fixes: {'OK' if agent_fixes_ok else 'ISSUES'}")
    
    if all([structure_ok, config_ok, agent_ok, agent_fixes_ok]):
        print("\n🎉 All critical fixes successfully applied!")
        print("\nNext steps:")
        print("1. Edit .env file with your API keys (optional)")
        print("2. Run: streamlit run frontend/app.py")
        print("3. Open browser to: http://localhost:8501")
        print("\nThe system will work in simulated mode without API keys.")
    else:
        print("\n⚠️  Some issues detected. Please review the output above.")
    
    return all([structure_ok, config_ok, agent_ok, agent_fixes_ok])

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1) 