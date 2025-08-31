# Streamlit Cloud Deployment Guide

## 🚀 Deploy to Streamlit Cloud

### **Configuration Files:**

1. **`requirements-streamlit.txt`** - Python dependencies for production
2. **`.streamlit/config.toml`** - Streamlit configuration
3. **`packages.txt`** - System dependencies

### **Deployment Steps:**

#### **1. Connect Repository:**
- Go to [share.streamlit.io](https://share.streamlit.io)
- Connect your GitHub repository
- Select the `main` branch

#### **2. Configure App:**
- **Main file path**: `app.py`
- **Requirements file**: `requirements-streamlit.txt`
- **Python version**: 3.9+

#### **3. Environment Variables (Optional):**
```
LLM_PROVIDER=simulated
STREAMLIT_SERVER_HEADLESS=true
```

### **App Structure:**

- **`app.py`** - Main page
- **`pages/1_📘_ISO_Docs.py`** - ISO documentation
- **`pages/2_📋_ISO_Dashboard.py`** - Compliance dashboard

### **Troubleshooting:**

#### **Authentication Error:**
- Verify repository is public
- Confirm `main` branch exists
- Check if configuration files are correct

#### **Dependencies Error:**
- Use `requirements-streamlit.txt` (clean version)
- Verify all dependencies are listed
- Confirm compatible versions

#### **Configuration Error:**
- Check `.streamlit/config.toml`
- Confirm `packages.txt` for system dependencies
- Verify app.py is in root directory

### **Deploy Status:**

- ✅ **Requirements updated**
- ✅ **Configuration optimized**
- ✅ **Page structure correct**
- ✅ **System dependencies configured**

---

**Last update**: 2025-01-19  
**Version**: 1.0  
**Status**: Ready for Streamlit Cloud
