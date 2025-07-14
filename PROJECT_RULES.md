# AgentMCP Project Rules & Best Practices

This document defines the technical rules and best practices that must be followed throughout the AgentMCP project development.

## 🔤 Language & Style

- **All code, variables, comments and docstrings must be in English**
- Use `snake_case` for functions and variables
- Follow PEP8 formatting guidelines
- Use type hints where applicable
- Maintain consistent naming conventions across all modules

## 📁 Project Structure

- **Organized by domain**: `agent/`, `services/`, `data/`, `mcp_server/`, `frontend/`, `logs/`, `tests/`
- Each business domain (CRM, ERP, HR) must have its own service module and MCP schema
- Keep related functionality grouped together
- Maintain clear separation of concerns between layers

### Directory Responsibilities:
- `agent/`: Core agent logic and MCP client implementation
- `services/`: Business logic for each domain (CRM, ERP, HR)
- `data/`: JSON data files for simulated persistence
- `mcp_server/`: MCP schema definitions for each domain
- `frontend/`: Streamlit web interface
- `logs/`: Application logs and action history
- `tests/`: Automated test suites

## 🤖 Agent Behavior

- **The agent must use MCP schemas to discover and call tools**
- No direct calls to service functions outside the MCP-defined interface
- All actions must be logged to `logs/actions.log`
- **Explainability is required**: log tool name, parameters, success/failure
- Agent should validate inputs before processing
- Handle errors gracefully with meaningful messages

### Agent Core Requirements:
- Load MCP schemas dynamically
- Parse natural language instructions
- Select appropriate tools based on MCP descriptions
- Extract parameters using defined patterns
- Execute tools through MCP interface
- Return formatted, user-friendly responses

## 💾 Persistence

- **Simulate persistence using JSON files in the `data/` folder**
- No use of external databases or cloud services
- Implement proper data validation before saving
- Use atomic write operations to prevent data corruption
- Maintain data consistency across operations

### Data Management:
- Validate JSON structure before loading/saving
- Implement backup mechanisms for critical data
- Use proper error handling for file operations
- Maintain data integrity across service boundaries

## 🧪 Testing

- **Use `pytest`** for all automated testing
- **All business logic and agent behaviors must be tested**
- **Use mocking when needed** to isolate units under test
- Maintain high test coverage for critical paths
- Test both success and failure scenarios

### Testing Requirements:
- Unit tests for all service functions
- Integration tests for agent workflows
- Mock external dependencies appropriately
- Test error handling and edge cases
- Verify logging behavior

## 🚫 Safety

- **No shell commands should be executed**
- **Do not overwrite data files without validation**
- **Logging must not expose sensitive data**
- Implement input sanitization
- Validate all user inputs before processing

### Security Guidelines:
- Never execute arbitrary code
- Validate file paths and prevent directory traversal
- Sanitize user inputs to prevent injection attacks
- Use safe file operations with proper permissions
- Log actions without exposing sensitive information

## 🔧 Development Workflow

### Code Quality:
- Write self-documenting code with clear variable names
- Add comprehensive docstrings for all public functions
- Use meaningful commit messages
- Review code before merging

### Documentation:
- Keep README.md updated with setup instructions
- Document API changes and new features
- Maintain inline documentation for complex logic
- Update project rules when new patterns emerge

## 📊 Monitoring & Logging

### Logging Standards:
- Use structured logging with consistent format
- Include timestamp, level, module, and message
- Log all agent actions with parameters
- Separate debug, info, warning, and error logs
- Rotate log files to prevent disk space issues

### Performance:
- Monitor agent response times
- Log resource usage for optimization
- Track tool usage patterns
- Monitor error rates and types

## 🔄 Version Control

- Use meaningful commit messages
- Create feature branches for new development
- Review code before merging to main
- Tag releases with semantic versioning
- Keep commit history clean and organized

---

**Remember**: These rules ensure consistency, maintainability, and reliability across the AgentMCP project. Follow them strictly to maintain code quality and project standards. 
