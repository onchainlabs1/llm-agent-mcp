# AgentMCP – LLM-based CRM Agent

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## 🧠 Overview

AgentMCP is an AI agent that uses large language models (LLMs) to interpret natural language instructions and execute real actions on a simulated CRM system, using the Model Context Protocol (MCP). All actions are logged and traceable.

The agent can:
- **Understand natural language** requests for CRM operations
- **Execute real actions** on simulated business data
- **Log all activities** for audit and debugging
- **Provide explainable results** with detailed reasoning
- **Handle complex workflows** through MCP tool orchestration

## 🛠️ Tech Stack

- **Python 3.11** - Core programming language
- **Streamlit** - Web-based user interface
- **JSON-based persistence** - Simulated database using JSON files
- **Model Context Protocol (Anthropic v1)** - Tool discovery and execution
- **pytest** - Automated testing framework
- **Agent logic** - Standard Python + MCP tool selection
- **Logging** - Structured action logging for traceability

## 🔧 Model Context Protocol (MCP) Integration

AgentMCP uses MCP schemas to define and discover available tools dynamically. Here's how it works:

### Example MCP Schema
Our CRM tools are defined in `mcp_server/crm_mcp.json`:

```json
{
  "name": "get_client_by_id",
  "description": "Retrieve detailed information about a specific client using their unique identifier",
  "input_schema": {
    "type": "object",
    "properties": {
      "client_id": {
        "type": "string",
        "description": "Unique identifier for the client (e.g., 'cli001', 'ACME_CORP')"
      }
    },
    "required": ["client_id"]
  }
}
```

### Tool Discovery Process
1. **Schema Loading**: Agent loads all `*.json` files from `mcp_server/`
2. **Tool Registration**: Each tool is registered with its parameters and validation rules
3. **Runtime Selection**: When user makes a request, LLM selects the best matching tool
4. **Parameter Extraction**: Agent extracts required parameters from natural language
5. **Validation & Execution**: Parameters are validated against schema before execution

### Available Tool Categories
- **CRM Tools** (`crm_mcp.json`): Client management, balance updates, filtering
- **ERP Tools** (`erp_mcp.json`): Order creation, status updates, inventory tracking
- **HR Tools** (`hr_mcp.json`): Employee management, department operations (planned)

![MCP Tool Discovery](docs/screenshots/mcp-tool-discovery.png)

*MCP tool discovery interface showing available tools, descriptions, and automatic schema loading*

### Adding New Tools
To extend AgentMCP with new capabilities:

1. **Define MCP Schema**:
   ```json
   {
     "name": "your_new_tool",
     "description": "Clear description of what the tool does",
     "input_schema": {
       "type": "object",
       "properties": {
         "param1": {"type": "string", "description": "Parameter description"}
       },
       "required": ["param1"]
     }
   }
   ```

2. **Implement Service Method**:
   ```python
   def your_new_tool(self, param1: str) -> Dict[str, Any]:
       # Implementation logic
       return {"success": True, "result": "Tool executed"}
   ```

3. **Agent Discovery**: The agent automatically discovers and registers the new tool

## 📁 Project Structure

```
agentmcp/
├── agent/                 # Core agent logic and MCP client
│   ├── agent_core.py     # Main agent orchestration
│   └── tools_mcp_client.py # MCP client implementation
├── services/             # Business logic modules
│   ├── crm_service.py    # CRM operations (clients, orders)
│   ├── erp_service.py    # ERP operations (inventory, finances)
│   └── hr_service.py     # HR operations (employees, payroll)
├── data/                 # JSON data persistence
│   ├── clients.json      # Customer data
│   ├── employees.json    # Employee records
│   └── orders.json       # Order management
├── mcp_server/           # MCP schema definitions
│   ├── crm_mcp.json      # CRM tool schemas
│   ├── erp_mcp.json      # ERP tool schemas
│   └── hr_mcp.json       # HR tool schemas
├── frontend/             # Streamlit web interface
│   └── app.py           # Main Streamlit application
├── logs/                 # Application logs
│   └── actions.log      # Agent action history
├── tests/               # Automated test suite
│   ├── test_agent.py    # Agent core tests
│   └── test_crm.py      # CRM service tests
├── requirements.txt     # Python dependencies
├── PROJECT_RULES.md     # Development guidelines
└── README.md           # This file
```

## ▶️ How to Run

### Prerequisites
- Python 3.9 or higher
- pip package manager
- API key for LLM provider (Groq, OpenAI, or Anthropic) - *optional, works in simulated mode without*

### Installation

#### Option 1: Development Installation (Recommended)
```bash
# Clone the repository
git clone https://github.com/onchainlabs1/llm-agent-mcp.git
cd llm-agent-mcp

# Install in development mode (resolves import issues)
pip install -e .

# Initialize project structure
python init_setup.py
```

**💡 Development Tip:** We strongly recommend Option 1 (editable installation) as it eliminates import issues and follows Python best practices. For detailed development setup and troubleshooting, see [DEVELOPMENT.md](DEVELOPMENT.md).

#### Option 2: Standard Installation
```bash
# Clone the repository
git clone https://github.com/onchainlabs1/llm-agent-mcp.git
cd llm-agent-mcp

# Install dependencies
pip install -r requirements.txt

# Initialize project structure  
python init_setup.py
```

#### Option 3: Development with All Tools
```bash
# For developers who want testing, linting, and documentation tools
pip install -r requirements-dev.txt
```

3. **Configure environment variables**
   ```bash
   # Edit .env file with your API keys (optional for demo mode)
   nano .env
   ```
   
   **Important:** The system will work in simulated mode if no API keys are provided. For full functionality, add your LLM provider API key:
   - For Groq: Set `GROQ_API_KEY`
   - For OpenAI: Set `OPENAI_API_KEY` 
   - For Anthropic: Set `ANTHROPIC_API_KEY`

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the application**
   ```bash
   streamlit run frontend/app.py
   ```

6. **Access the web interface**
   - Open your browser and navigate to `http://localhost:8501`
   - The AgentMCP interface will be available

### Configuration

The application uses environment variables for configuration. Key settings include:

- **GROQ_API_KEY**: Your Groq API key for LLM integration (recommended)
- **LLM_PROVIDER**: LLM provider (`groq`, `openai`, `anthropic`, `simulated`)
- **LOG_LEVEL**: Logging level (`DEBUG`, `INFO`, `WARNING`, `ERROR`)
- **LLM_MODEL**: Model to use (e.g., `llama3-70b-8192` for Groq)

See `.env.example` for all available configuration options.

### Demo Mode
The system includes a simulated LLM mode for testing without API keys. Simply run the setup and start the application - it will automatically use pattern matching for tool selection.

## 📊 Logging and Monitoring

AgentMCP provides comprehensive logging for all operations and activities:

### Log Structure
All logs follow a structured format with timestamp, module, level, and detailed messages:

```
2025-01-14 10:15:45,234 - agentmcp.core - INFO - Processing user request: "List all clients"
2025-01-14 10:15:45,456 - agentmcp.core - INFO - Selected tool: list_all_clients with parameters: {}
2025-01-14 10:15:45,789 - agentmcp.core - INFO - Tool execution successful - found 25 clients
```

### Log Locations
- **Real-time logs**: `logs/actions.log` (generated during application execution)
- **Example logs**: `logs/example_actions.log` (sample log entries showing typical operations)
- **Configuration**: Set `LOG_LEVEL` in `.env` file (DEBUG, INFO, WARNING, ERROR)

### What Gets Logged
- **Agent initialization** and configuration
- **Tool discovery** from MCP schemas
- **User requests** with natural language input
- **Tool selection** and parameter extraction
- **Execution results** (success/failure with details)
- **Error handling** and fallback mechanisms
- **Performance metrics** (execution times)

### Log Analysis
Use standard tools to analyze logs:
```bash
# View recent activity
tail -f logs/actions.log

# Search for specific operations
grep "create_client" logs/actions.log

# Filter by log level
grep "ERROR" logs/actions.log

# Count successful operations
grep "Tool execution successful" logs/actions.log | wc -l
```

## 🚀 Usage

### Natural Language Commands

The agent understands natural language instructions for CRM operations:

- **"Show me all clients"** - Lists all customers in the system
- **"Get client information for John Doe"** - Retrieves specific client details
- **"Create a new client named Jane Smith with email jane@example.com"** - Adds new customer
- **"Update client balance for client ID 123 to $500"** - Modifies client financial data

### Interface Overview

![AgentMCP Interface](docs/screenshots/agentmcp-interface.png)

*The main AgentMCP interface showing natural language input, tool execution results, and configuration options*

### Live Tool Execution

![Tool Execution Demo](docs/screenshots/tool-execution-demo.gif)

*Demonstration of creating a new client through natural language - from user input to successful execution*

### Features

- **Real-time Processing**: Immediate execution of commands
- **Action Logging**: All operations are logged with timestamps and full audit trail
- **Error Handling**: Graceful error management with user-friendly messages
- **Data Validation**: Input validation and data integrity checks
- **Audit Trail**: Complete history of all agent actions

## 🧪 Testing

Run the automated test suite:

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_agent.py

# Run with verbose output
pytest -v

# Run with coverage report
pytest --cov=agent --cov=services
```

## 📊 Logging

All agent actions are logged to `logs/actions.log` with detailed information:

- **Timestamp** of each action
- **Tool name** and parameters used
- **Success/failure** status
- **Execution time** and results
- **Error details** when applicable

## 🔧 Development

### Project Rules
Follow the guidelines in `PROJECT_RULES.md` for:
- Code style and naming conventions
- Architecture patterns
- Testing requirements
- Security considerations

### Adding New Tools
1. Define the tool in the appropriate MCP schema file
2. Implement the corresponding service function
3. Add tests for the new functionality
4. Update documentation

## 🤝 Contributing

1. Follow the project rules and coding standards
2. Write comprehensive tests for new features
3. Update documentation as needed
4. Ensure all tests pass before submitting

## 📝 License

This project is licensed under the [MIT License](LICENSE) - see the [LICENSE](LICENSE) file for full details.

**Summary**: You are free to use, modify, and distribute this software for any purpose, including commercial use, as long as you include the original copyright notice and license text.

## 🔗 Related Links

- [Model Context Protocol Documentation](https://modelcontextprotocol.io/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Python Testing with pytest](https://docs.pytest.org/)

---

**AgentMCP** - Making CRM operations intelligent and accessible through natural language processing. 