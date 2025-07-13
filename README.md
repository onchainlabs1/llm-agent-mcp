# AgentMCP – LLM-based CRM Agent

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
- Python 3.11 or higher
- pip package manager
- API key for LLM provider (Groq, OpenAI, or Anthropic) - *optional, works in simulated mode without*

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd agentmcp
   ```

2. **Initialize the project**
   ```bash
   python setup.py
   ```
   This will create necessary directories, configuration files, and initial data.

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

## 🚀 Usage

### Natural Language Commands

The agent understands natural language instructions for CRM operations:

- **"Show me all clients"** - Lists all customers in the system
- **"Get client information for John Doe"** - Retrieves specific client details
- **"Create a new client named Jane Smith with email jane@example.com"** - Adds new customer
- **"Update client balance for client ID 123 to $500"** - Modifies client financial data

### Features

- **Real-time Processing**: Immediate execution of commands
- **Action Logging**: All operations are logged with timestamps
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

This project is licensed under the MIT License - see the LICENSE file for details.

## 🔗 Related Links

- [Model Context Protocol Documentation](https://modelcontextprotocol.io/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Python Testing with pytest](https://docs.pytest.org/)

---

**AgentMCP** - Making CRM operations intelligent and accessible through natural language processing. 