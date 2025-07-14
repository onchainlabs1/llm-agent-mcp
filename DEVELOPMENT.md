# Development Guide

## 🚀 Recommended Setup

To avoid import issues and sys.path manipulations, we strongly recommend using the **editable installation** method:

### Installation Methods (in order of preference)

#### 1. **Editable Installation (Recommended)**
```bash
# Install in development mode - changes to code are immediately reflected
pip install -e .

# All imports will work cleanly without sys.path manipulation
python -c "from agentmcp.agent.agent_core import AgentCore; print('✅ Clean imports work!')"
```

#### 2. **Standard Installation**
```bash
# Install as a standard package
pip install -r requirements.txt

# Works but requires reinstallation after code changes
```

#### 3. **Development Mode (Fallback)**
```bash
# Only if you can't use pip install -e .
# The code will use sys.path fallbacks automatically
```

## 📦 Import Pattern Strategy

The codebase uses a multi-layer import strategy:

```python
try:
    # 1. Try relative imports (when used as a package)
    from ..config import config
except ImportError:
    try:
        # 2. Try absolute package imports (recommended: pip install -e .)
        from agentmcp.config import config
    except ImportError:
        # 3. Final fallback for development (avoid sys.path when possible)
        import sys
        from pathlib import Path
        sys.path.append(str(Path(__file__).parent.parent))
        from config import config
```

This approach:
- ✅ **Eliminates sys.path manipulation** when using proper installation
- ✅ **Maintains backward compatibility** for development scenarios
- ✅ **Follows Python packaging best practices**
- ✅ **Works in all environments** (development, testing, production)

## 🔧 Development Workflow

### Initial Setup
```bash
# 1. Clone the repository
git clone https://github.com/onchainlabs1/llm-agent-mcp.git
cd llm-agent-mcp

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install in editable mode (RECOMMENDED)
pip install -e .

# 4. Install development dependencies
pip install -r requirements-dev.txt

# 5. Verify installation
python -c "from agentmcp import AgentCore; print('✅ Package installed correctly')"
```

### Running Tests
```bash
# Tests will use clean package imports
pytest tests/ -v
```

### Running the Application
```bash
# Frontend will use clean package imports
streamlit run frontend/app.py
```

## 📁 Package Structure

When installed with `pip install -e .`, the package structure becomes:

```
agentmcp/                 # Main package
├── agent/               # agentmcp.agent
│   ├── agent_core.py    # agentmcp.agent.agent_core
│   └── tools_mcp_client.py
├── services/            # agentmcp.services
│   ├── crm_service.py   # agentmcp.services.crm_service
│   ├── erp_service.py
│   └── hr_service.py
├── config.py            # agentmcp.config
└── __init__.py
```

## 🎯 Benefits of Proper Installation

### Before (with sys.path manipulation):
- ❌ Import paths dependent on file location
- ❌ sys.path pollution
- ❌ IDE/editor confusion with imports
- ❌ Difficult to package for distribution

### After (with pip install -e .):
- ✅ Clean, predictable import paths
- ✅ No sys.path manipulation needed
- ✅ Better IDE support and autocomplete
- ✅ Ready for packaging and distribution
- ✅ Follows Python best practices

## 🐛 Troubleshooting

### Import Errors
If you see import errors:

1. **Check installation**:
   ```bash
   pip list | grep agentmcp
   ```

2. **Reinstall in editable mode**:
   ```bash
   pip uninstall agentmcp
   pip install -e .
   ```

3. **Verify Python path**:
   ```bash
   python -c "import agentmcp; print(agentmcp.__file__)"
   ```

### Legacy Development Mode
If you must use the old development mode:
- The code will automatically fall back to sys.path manipulation
- All functionality remains the same
- Consider upgrading to editable installation when possible

## 📋 Migration Checklist

- [x] Created proper setup.py with package metadata
- [x] Added __init__.py files for proper package structure
- [x] Updated all import statements to use multi-layer strategy
- [x] Reduced sys.path manipulations to fallback only
- [x] Documented recommended installation method
- [x] Verified all imports work with pip install -e .

## 🏆 Best Practices

1. **Always use `pip install -e .` for development**
2. **Import from agentmcp.* when possible**
3. **Avoid adding new sys.path manipulations**
4. **Test imports after any structural changes**
5. **Keep fallback imports for compatibility** 