# 🤖 Agent Mode - Streamlit Cloud

This document describes how to use agent mode in the Streamlit Cloud environment.

## ✅ **Available Features**

### **1. Core Agent**
- **LLM Integration**: Support for Groq, OpenAI and Anthropic
- **Fallback Mode**: Simulated mode when APIs are not available
- **ISO Controls**: Complete implementation of ISO 42001:2023 controls

### **2. ISO 42001 Controls**
- **R001**: Bias Detection and Mitigation
- **R002**: Fact-checking and Confidence Scoring
- **R003**: Enhanced Prompt Sanitization
- **R008**: Data Encryption and Integrity

### **3. MCP Tools**
- **Tool Registry**: Tool registration system
- **Schema Validation**: MCP schema validation
- **Tool Execution**: Secure tool execution

## 🚀 **How to Use**

### **1. Access Agent Mode**
- Navigate to the "🤖 Agent Mode Test" page
- Run tests to verify functionality
- Use agent features as needed

### **2. Configuration**
- Agent works in simulated mode by default
- To use real APIs, configure environment variables
- See `env_example.txt` for configuration examples

### **3. Main Features**
```python
# Example agent usage
from agent.agent_core import call_llm

# Simple call
response = call_llm("Hello, how can I help?")

# Response includes ISO metadata
print(f"Response: {response['response']}")
print(f"Confidence: {response['confidence_score']}")
print(f"Bias Score: {response['bias_score']}")
```

## 🔧 **Advanced Configuration**

### **Environment Variables**
```bash
# LLM Configuration
LLM_PROVIDER=groq  # or openai, anthropic, simulated
LLM_MODEL=llama3-70b-8192

# API Keys
GROQ_API_KEY=your-key-here
OPENAI_API_KEY=your-key-here
ANTHROPIC_API_KEY=your-key-here

# MCP Configuration
MCP_SERVER_URL=http://localhost:8000
MCP_SCHEMAS_PATH=mcp_server/
```

### **Simulated Mode**
- Works without API keys
- Simulated responses for development
- ISO controls still active
- Ideal for testing and demonstrations

## 📊 **Monitoring and Logs**

### **Audit Logs**
- All actions are logged
- ISO controls applied and documented
- Complete traceability for audits

### **Quality Metrics**
- Bias scores for each interaction
- Confidence scores for responses
- Fact-checking results
- Operational control status

## 🛡️ **Security and Compliance**

### **ISO 42001:2023**
- ✅ Prompt sanitization
- ✅ Bias detection
- ✅ Fact-checking
- ✅ Data encryption
- ✅ Audit logging

### **Operational Controls**
- Rate limiting
- Session management
- Input validation
- Output sanitization

## 🚨 **Troubleshooting**

### **Common Errors**
1. **Import Errors**: Check if all dependencies are installed
2. **Config Errors**: Use simulated mode if APIs are not configured
3. **Permission Errors**: Check access to data directories

### **Diagnostic Tests**
- Run `test_agent_mode.py` to verify functionality
- Check logs to identify issues
- Use simulated mode for problem isolation

## 📚 **Additional Resources**

- **ISO Documentation**: See `docs/` for complete details
- **Usage Examples**: Check tests for usage patterns
- **Configuration**: Use `agent_config.py` for customizations

## 🎯 **Next Steps**

1. **Test Agent Mode**: Run `test_agent_mode.py`
2. **Configure APIs**: Add your API keys if needed
3. **Customize**: Adjust configuration as needed
4. **Monitor**: Use logs to track usage and quality

---

**Status**: ✅ Ready for use in Streamlit Cloud
**Version**: 1.0.0
**Last Update**: December 2024
