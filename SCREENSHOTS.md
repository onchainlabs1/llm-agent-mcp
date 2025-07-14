# 📸 Screenshot Documentation Guide

This guide explains how to generate and add screenshots to enhance the AgentMCP documentation.

## 🎯 Required Screenshots

### 1. Main Interface (`agentmcp-interface.png`)

**What to capture:**
- Full Streamlit interface at http://localhost:8501
- Natural language input field with example text
- Configuration sidebar (expanded)
- Available tools section
- System status indicators
- Recent actions or history (if available)

**Steps:**
1. Start AgentMCP: `streamlit run frontend/app.py`
2. Open browser to http://localhost:8501
3. Expand sidebar to show all configuration options
4. Type example prompt: "Create a new client named Alice Smith with email alice@acme.com"
5. Take full-page screenshot (1920x1080 or higher)
6. Save as `docs/screenshots/agentmcp-interface.png`

### 2. Tool Execution Demo (`tool-execution-demo.gif`)

**What to record:**
- User typing a natural language command
- Agent processing and tool selection
- Successful execution with results
- Updated data or confirmation

**Steps:**
1. Start screen recording software (OBS Studio, QuickTime, etc.)
2. Record browser window at http://localhost:8501
3. Type command: "List all clients with balance over 5000"
4. Wait for processing and show results
5. Keep recording under 20 seconds
6. Export as optimized GIF (max 3MB)
7. Save as `docs/screenshots/tool-execution-demo.gif`

### 3. MCP Tool Discovery (`mcp-tool-discovery.png`)

**What to capture:**
- Available tools section in sidebar
- Tool categories (CRM, ERP, HR)
- Tool descriptions and examples
- Schema loading status

**Steps:**
1. Focus on sidebar "Available Tools" section
2. Ensure all tool categories are visible
3. Show tool descriptions and example commands
4. Capture at high resolution
5. Save as `docs/screenshots/mcp-tool-discovery.png`

## 🛠️ Technical Requirements

### Screenshot Specifications
- **Format**: PNG for static images, GIF for animations
- **Resolution**: Minimum 1920x1080 for desktop screenshots
- **Size**: Max 5MB for PNG, max 3MB for GIF
- **Quality**: High quality, clear text readable at 100% zoom

### Screen Recording Setup
```bash
# For macOS (QuickTime)
# 1. Open QuickTime Player
# 2. File > New Screen Recording
# 3. Select browser window only
# 4. Keep duration under 20 seconds

# For Windows/Linux (OBS Studio)
# 1. Create new scene with browser window source
# 2. Start recording
# 3. Perform demo actions
# 4. Export as MP4, then convert to GIF
```

### GIF Optimization
```bash
# Using ffmpeg to create optimized GIF
ffmpeg -i input.mp4 -vf "fps=10,scale=1200:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" -loop 0 output.gif

# Alternative: Use online tools like ezgif.com for optimization
```

## 📝 Adding Screenshots to Documentation

### README.md Updates
Screenshots are already referenced in the README.md:

1. **Interface screenshot** in "Usage" section
2. **Tool execution GIF** in "Usage" section  
3. **Tool discovery screenshot** in "MCP Integration" section

### File Organization
```
docs/
├── screenshots/
│   ├── agentmcp-interface.png
│   ├── tool-execution-demo.gif
│   ├── mcp-tool-discovery.png
│   └── .gitkeep
└── SCREENSHOTS.md (this file)
```

## ✅ Quality Checklist

Before adding screenshots to the repository:

- [ ] **Text is readable** at normal viewing size
- [ ] **UI elements are clear** and properly focused
- [ ] **No sensitive information** visible (API keys, personal data)
- [ ] **Consistent styling** across all screenshots
- [ ] **File sizes optimized** (PNG < 5MB, GIF < 3MB)
- [ ] **Descriptive filenames** following naming convention
- [ ] **Alt text provided** in markdown for accessibility

## 🔄 Updating Screenshots

Screenshots should be updated when:

- **UI changes significantly** (new features, layout changes)
- **Tool functionality is added** or modified
- **Branding or styling** is updated
- **User feedback indicates** confusion about interface

## 📋 Screenshot Automation

For consistent updates, consider creating a script:

```bash
#!/bin/bash
# screenshot-automation.sh

echo "🚀 Starting AgentMCP for screenshots..."
streamlit run frontend/app.py &
APP_PID=$!

sleep 10  # Wait for app to start

echo "📸 Ready for screenshots at http://localhost:8501"
echo "Press Enter when screenshots are complete..."
read

kill $APP_PID
echo "✅ AgentMCP stopped"
```

## 📞 Support

If you need help with screenshot generation or have questions about the documentation:

1. Check existing screenshots in `docs/screenshots/`
2. Review this guide for technical requirements
3. Open an issue on GitHub with the `documentation` label
4. Include your operating system and browser information

---

**Note**: Screenshots are important for user onboarding and project presentation. High-quality visuals significantly improve the developer experience and project adoption. 