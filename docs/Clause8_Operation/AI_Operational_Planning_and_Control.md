---
owner: Technical Lead
version: 1.0
approved_by: AIMS Manager
approved_on: 2024-12-20
next_review: 2025-06-20
---

# AI Operational Planning and Control
*AI Management System - ISO/IEC 42001:2023 Compliance*

**Document Control:**
- **Document ID:** AIMS-OPC-001
- **Version:** 1.0
- **Date:** 2024-12-19
- **Status:** Draft
- **Owner:** AI Management Team

---

## 8.1 Operational Planning and Control

### 8.1.1 General

The organization shall plan, implement, and control the processes needed to meet the AI management system requirements and to implement the actions determined in Clause 6.

#### 8.1.1.1 Operational Framework

The `llm-agent-mcp` project implements a comprehensive operational framework that ensures reliable, secure, and compliant operation of the AI management system through multiple interfaces and control mechanisms.

### 8.1.2 Operational Architecture

#### 8.1.2.1 Multi-Interface System Architecture

**Primary Interfaces:**
- **Streamlit Web Interface:** Primary user interface via `app.py` and `landing.py`
- **FastAPI REST API:** Enterprise integration interface via `api/` directory
- **MCP Protocol Server:** Tool discovery and execution via `mcp_server/*.json`
- **Agent Core Engine:** Central LLM agent orchestration via `agent/agent_core.py`

**Current Implementation Examples:**
```python
# Streamlit Interface (app.py)
streamlit run app.py  # Port 8501

# FastAPI Interface (api/main.py)
uvicorn api.main:app --host 0.0.0.0 --port 8000

# MCP Protocol (agent/tools_mcp_client.py)
# Tool discovery from mcp_server/*.json schemas

# Agent Core (agent/agent_core.py)
# Central LLM agent orchestration
```

#### 8.1.2.2 Workflow Orchestration

**Request Processing Workflow:**
```
User Input → Interface Layer → Agent Core → MCP Client → Business Services → JSON Data
```

**Current Implementation Examples:**
- **Input Validation:** Validation in Streamlit and FastAPI interfaces
- **Agent Processing:** LLM agent processing in `agent/agent_core.py`
- **Tool Execution:** MCP tool execution via `agent/tools_mcp_client.py`
- **Data Persistence:** JSON-based persistence in `data/` directory

### 8.1.3 Operational Controls

#### 8.1.3.1 MCP Protocol Controls

**Tool Discovery and Validation:**
- **Schema Validation:** Validation of tool schemas in `mcp_server/*.json`
- **Parameter Validation:** Validation of tool parameters against schemas
- **Execution Control:** Controlled execution of tools through MCP protocol
- **Error Handling:** Comprehensive error handling for tool execution failures

**Current Implementation Examples:**
```python
# Tool schema validation (agent/tools_mcp_client.py)
def validate_tool_schema(tool_name: str, parameters: dict) -> bool:
    schema = load_mcp_schema(tool_name)
    return validate_parameters(parameters, schema)

# Tool execution control
def execute_tool_safely(tool_name: str, parameters: dict) -> dict:
    if not validate_tool_schema(tool_name, parameters):
        raise ValidationError(f"Invalid parameters for tool {tool_name}")
    return execute_tool(tool_name, parameters)
```

#### 8.1.3.2 Fallback Mechanisms

**LLM Provider Fallback:**
- **Primary Providers:** OpenAI GPT and Anthropic Claude APIs
- **Simulated Mode:** Fallback to simulated mode when APIs unavailable
- **Graceful Degradation:** Reduced functionality with clear user notification
- **Health Monitoring:** Continuous monitoring of API availability

**Current Implementation Examples:**
```python
# Fallback mechanism (agent/agent_core.py)
def get_llm_response(prompt: str) -> str:
    try:
        if self.llm_provider == "openai":
            return self.openai_client.chat.completions.create(...)
        elif self.llm_provider == "anthropic":
            return self.anthropic_client.messages.create(...)
        else:
            return self._simulate_llm_response(prompt)
    except Exception as e:
        logger.warning(f"LLM API failed, using simulated mode: {e}")
        return self._simulate_llm_response(prompt)
```

#### 8.1.3.3 Input Validation and Security

**Input Validation Controls:**
- **Prompt Injection Prevention:** Validation of user inputs for malicious content
- **Parameter Sanitization:** Sanitization of all input parameters
- **Access Control:** Authentication and authorization for sensitive operations
- **Rate Limiting:** Rate limiting to prevent abuse

**Current Implementation Examples:**
```python
# Input validation (app.py and api/routers/agent.py)
def validate_user_input(user_input: str) -> bool:
    # Check for prompt injection patterns
    injection_patterns = [
        "ignore previous instructions",
        "system prompt",
        "override",
        "bypass"
    ]
    return not any(pattern in user_input.lower() for pattern in injection_patterns)

# Rate limiting (api/middleware/rate_limit.py)
def rate_limit_middleware(request: Request):
    client_ip = request.client.host
    if is_rate_limited(client_ip):
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
```

### 8.1.4 Operational Monitoring

#### 8.1.4.1 Performance Monitoring

**Response Time Monitoring:**
- **LLM Response Time:** Monitoring of LLM query response times
- **Tool Execution Time:** Monitoring of MCP tool execution times
- **Interface Response Time:** Monitoring of Streamlit and FastAPI response times
- **System Performance:** Overall system performance metrics

**Current Implementation Examples:**
```python
# Performance monitoring (agent/agent_core.py)
import time

def execute_with_monitoring(func, *args, **kwargs):
    start_time = time.time()
    try:
        result = func(*args, **kwargs)
        execution_time = time.time() - start_time
        logger.info(f"Function {func.__name__} executed in {execution_time:.2f}s")
        return result
    except Exception as e:
        execution_time = time.time() - start_time
        logger.error(f"Function {func.__name__} failed after {execution_time:.2f}s: {e}")
        raise
```

#### 8.1.4.2 Error Monitoring

**Error Detection and Logging:**
- **LLM Errors:** Detection and logging of LLM API errors
- **MCP Protocol Errors:** Detection and logging of MCP protocol errors
- **Business Logic Errors:** Detection and logging of business service errors
- **Interface Errors:** Detection and logging of interface errors

**Current Implementation Examples:**
```python
# Error monitoring (logs/actions.log)
def log_error(error_type: str, error_message: str, context: dict):
    error_log = {
        "timestamp": datetime.now().isoformat(),
        "error_type": error_type,
        "error_message": error_message,
        "context": context,
        "severity": "ERROR"
    }
    logger.error(json.dumps(error_log))
```

### 8.1.5 Operational Procedures

#### 8.1.5.1 Deployment Procedures

**Application Deployment:**
- **Streamlit Deployment:** Deployment to Streamlit Community Cloud
- **FastAPI Deployment:** Local or cloud deployment of REST API
- **Configuration Management:** Environment-specific configuration management
- **Health Checks:** Health check procedures for all interfaces

**Current Implementation Examples:**
```bash
# Streamlit deployment
streamlit run app.py --server.port 8501 --server.address 0.0.0.0

# FastAPI deployment
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload

# Health checks
curl http://localhost:8000/health
curl http://localhost:8501/_stcore/health
```

#### 8.1.5.2 Maintenance Procedures

**Regular Maintenance:**
- **Dependency Updates:** Regular updates of Python packages
- **Security Patches:** Application of security patches
- **Performance Optimization:** Continuous performance optimization
- **Documentation Updates:** Regular updates of operational documentation

**Current Implementation Examples:**
```bash
# Dependency updates
pip install -r requirements.txt --upgrade

# Security scanning
bandit -r agent/ services/ api/

# Performance testing
pytest tests/ -v --benchmark-only
```

### 8.1.6 Operational Safeguards

#### 8.1.6.1 Data Protection Safeguards

**Data Handling Controls:**
- **Input Validation:** Validation of all input data
- **Output Sanitization:** Sanitization of all output data
- **Data Encryption:** Encryption of sensitive data in transit and at rest
- **Access Controls:** Role-based access controls for data access

**Current Implementation Examples:**
```python
# Data validation (services/models.py)
from pydantic import BaseModel, EmailStr, validator

class ClientData(BaseModel):
    client_id: str
    name: str
    email: EmailStr
    balance: float
    
    @validator('balance')
    def validate_balance(cls, v):
        if v < 0:
            raise ValueError('Balance cannot be negative')
        return v
```

#### 8.1.6.2 Security Safeguards

**Security Controls:**
- **Authentication:** Multi-factor authentication for sensitive operations
- **Authorization:** Role-based authorization for different operations
- **Audit Logging:** Comprehensive audit logging of all operations
- **Incident Response:** Incident response procedures for security events

**Current Implementation Examples:**
```python
# Authentication (api/middleware/auth.py)
def verify_api_key(request: Request):
    api_key = request.headers.get("X-API-Key")
    if not api_key or not is_valid_api_key(api_key):
        raise HTTPException(status_code=401, detail="Invalid API key")

# Audit logging (logs/actions.log)
def log_audit_event(user_id: str, action: str, resource: str, result: str):
    audit_log = {
        "timestamp": datetime.now().isoformat(),
        "user_id": user_id,
        "action": action,
        "resource": resource,
        "result": result,
        "type": "AUDIT"
    }
    logger.info(json.dumps(audit_log))
```

### 8.1.7 Operational Metrics

#### 8.1.7.1 Key Performance Indicators

**Operational KPIs:**
- **System Uptime:** Target >99.5% uptime for all interfaces
- **Response Time:** Target <5 seconds for typical operations
- **Error Rate:** Target <1% error rate for all operations
- **User Satisfaction:** Target >90% user satisfaction

**Current Implementation Examples:**
```python
# KPI tracking (api/routers/health.py)
@app.get("/metrics")
def get_operational_metrics():
    return {
        "uptime": calculate_uptime(),
        "response_time_avg": calculate_avg_response_time(),
        "error_rate": calculate_error_rate(),
        "active_users": get_active_user_count()
    }
```

#### 8.1.7.2 Continuous Improvement

**Improvement Process:**
- **Performance Monitoring:** Continuous monitoring of operational performance
- **User Feedback:** Collection and analysis of user feedback
- **Process Optimization:** Continuous optimization of operational processes
- **Technology Updates:** Regular updates of technology and tools

**Current Implementation Examples:**
```python
# Feedback collection (app.py)
def collect_user_feedback(user_input: str, response: str, satisfaction: int):
    feedback = {
        "timestamp": datetime.now().isoformat(),
        "user_input": user_input,
        "response": response,
        "satisfaction": satisfaction
    }
    save_feedback(feedback)
```

### 8.1.8 Operational Documentation

#### 8.1.8.1 Procedure Documentation

**Operational Procedures:**
- **Deployment Procedures:** Documented deployment procedures
- **Maintenance Procedures:** Documented maintenance procedures
- **Troubleshooting Procedures:** Documented troubleshooting procedures
- **Emergency Procedures:** Documented emergency procedures

**Current Implementation Examples:**
- **README.md:** Comprehensive project documentation
- **DEVELOPMENT.md:** Development and deployment procedures
- **PROJECT_RULES.md:** Development guidelines and best practices
- **API Documentation:** FastAPI automatic documentation

#### 8.1.8.2 Training and Competence

**Operational Training:**
- **System Training:** Training on system operation and maintenance
- **Security Training:** Training on security procedures and best practices
- **Emergency Training:** Training on emergency response procedures
- **Continuous Learning:** Continuous learning and development programs

### 8.1.9 Decommissioning Procedure

Define safe retirement of AI components (tools, models, interfaces) to prevent residual risk and ensure controlled knowledge retention.

High-level steps:
- Obtain approval from AIMS Manager and Technical Lead
- Snapshot and archive configs, schemas (`mcp_server/*.json`), and critical logs (`logs/`)
- Disable API keys and revoke all related access
- Remove Streamlit/FastAPI routes referencing the component
- Tag release and archive documentation snapshot (`docs/Evidence_Index.md`)
- Update SoA control A.4.11 with evidence links

Checklist:
- [ ] Data retention/disposal per 8.3.8 completed
- [ ] Access revoked; secrets rotated
- [ ] SoA and Evidence Index updated
- [ ] Stakeholders notified and rollback plan documented

---

**Document Approval:**
- **Prepared by:** AI Management Team
- **Reviewed by:** Technical Lead
- **Approved by:** AI Management Team Lead
- **Next Review:** 2025-03-19

**References:**
- ISO/IEC 42001:2023 - Clause 8.1
- Aligned with ISO/IEC 42001:2023 - Clause 6.1.2(d)
- See Control A.2.1 for governance requirements 