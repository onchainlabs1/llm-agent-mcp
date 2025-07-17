# AgentMCP REST API

🚀 **Enterprise-grade REST API** for AgentMCP business automation platform.

## ✨ Features

- **🤖 Natural Language Processing**: Convert business commands to API calls
- **🔐 Enterprise Security**: API key authentication with rate limiting
- **📊 Real-time Monitoring**: Health checks and system metrics
- **📚 Interactive Documentation**: Auto-generated OpenAPI/Swagger docs
- **🏢 Multi-domain Support**: CRM, ERP, and HR operations
- **⚡ High Performance**: Async FastAPI with middleware optimization

## 🚀 Quick Start

### 1. Start the API Server

```bash
# Option 1: Using the launcher script
python run_api.py

# Option 2: Direct uvicorn
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```

### 2. Access the Documentation

- **Interactive Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **API Info**: http://localhost:8000/

### 3. Health Check

```bash
curl http://localhost:8000/api/v1/health
```

## 🔐 Authentication

All endpoints (except public ones) require API key authentication:

```bash
curl -H "Authorization: Bearer your-api-key" http://localhost:8000/api/v1/endpoint
```

### Available Demo Keys

- `demo-key-123` (Free tier: 100 requests/hour)
- `premium-key-456` (Premium tier: 1000 requests/hour)  
- `dev-key-789` (Development: 10000 requests/hour)

## 📋 API Endpoints

### 🏥 Health & Monitoring

| Endpoint | Method | Description |
|----------|---------|-------------|
| `/api/v1/health` | GET | Basic health check |
| `/api/v1/health/detailed` | GET | Detailed system metrics |
| `/api/v1/health/status` | GET | Service status check |

### 🤖 AI Agent

| Endpoint | Method | Description |
|----------|---------|-------------|
| `/api/v1/agent/process` | POST | Process natural language commands |
| `/api/v1/agent/tools` | GET | List available MCP tools |
| `/api/v1/agent/examples` | GET | Get example commands |

## 💡 Usage Examples

### Natural Language Processing

```bash
curl -X POST "http://localhost:8000/api/v1/agent/process" \
  -H "Authorization: Bearer demo-key-123" \
  -H "Content-Type: application/json" \
  -d '{
    "command": "List all clients with balance over 5000",
    "context": {"department": "sales"}
  }'
```

### Get Available Tools

```bash
curl -H "Authorization: Bearer demo-key-123" \
  http://localhost:8000/api/v1/agent/tools
```

### System Health Check

```bash
curl http://localhost:8000/api/v1/health/detailed
```

## 🏗️ Architecture

```
api/
├── main.py              # FastAPI application
├── dependencies.py      # Dependency injection
├── middleware/          # Custom middleware
│   ├── auth.py         # Authentication & rate limiting
│   ├── cors.py         # CORS configuration
│   └── logging.py      # Request logging
├── routers/            # API endpoints
│   ├── health.py       # Health checks
│   └── agent.py        # Agent operations
└── schemas/            # Pydantic models
    ├── requests.py     # Request models
    └── responses.py    # Response models
```

## �� Configuration

The API uses the same configuration as the main AgentMCP application:

- **Environment Variables**: `.env` file
- **LLM Providers**: Groq, OpenAI, Anthropic
- **Fallback Mode**: Works without API keys in simulated mode

## 📊 Monitoring

### Request Logging

All requests are logged with:
- Unique request ID
- Execution time
- Status codes
- Rate limit headers

### System Metrics

Available via `/api/v1/health/detailed`:
- CPU usage
- Memory utilization
- Disk space
- Service health status

## 🚨 Error Handling

The API provides consistent error responses:

```json
{
  "error": {
    "code": 401,
    "message": "Invalid API key",
    "type": "AuthenticationError",
    "timestamp": 1640995200.0,
    "path": "/api/v1/agent/process"
  }
}
```

## 🌐 CORS Configuration

Configured for:
- Streamlit apps (ports 8501, 8502)
- React development (port 3000)
- Production domains

## 📈 Performance

- **Async/Await**: Non-blocking operations
- **Middleware**: GZip compression
- **Caching**: Configuration caching
- **Rate Limiting**: Per-tier request limits

## 🔮 Future Enhancements

- [ ] **Database Integration**: PostgreSQL support
- [ ] **Advanced Authentication**: JWT tokens, OAuth2
- [ ] **Metrics Export**: Prometheus integration
- [ ] **WebSocket Support**: Real-time updates
- [ ] **API Versioning**: v2 endpoints
- [ ] **Batch Operations**: Multiple commands
- [ ] **Webhook Support**: Event notifications

## 📞 Support

- **Documentation**: http://localhost:8000/docs
- **Issues**: [GitHub Issues](https://github.com/onchainlabs1/llm-agent-mcp/issues)
- **Email**: support@agentmcp.com
