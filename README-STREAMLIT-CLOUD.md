# Streamlit Cloud Deployment Guide

## 🚀 Deploy no Streamlit Cloud

### **Arquivos de Configuração:**

1. **`requirements-streamlit.txt`** - Dependências Python para produção
2. **`.streamlit/config.toml`** - Configuração do Streamlit
3. **`packages.txt`** - Dependências do sistema

### **Passos para Deploy:**

#### **1. Conectar Repositório:**
- Acesse [share.streamlit.io](https://share.streamlit.io)
- Conecte seu repositório GitHub
- Selecione o branch `main`

#### **2. Configurar App:**
- **Main file path**: `app.py`
- **Requirements file**: `requirements-streamlit.txt`
- **Python version**: 3.9+

#### **3. Variáveis de Ambiente (Opcional):**
```
LLM_PROVIDER=simulated
STREAMLIT_SERVER_HEADLESS=true
```

### **Estrutura do App:**

- **`app.py`** - Página principal
- **`pages/1_📘_ISO_Docs.py`** - Documentação ISO
- **`pages/2_📋_ISO_Dashboard.py`** - Dashboard de Compliance

### **Troubleshooting:**

#### **Erro de Autenticação:**
- Verificar se o repositório está público
- Confirmar se o branch `main` existe
- Verificar se os arquivos de configuração estão corretos

#### **Erro de Dependências:**
- Usar `requirements-streamlit.txt` (versão limpa)
- Verificar se todas as dependências estão listadas
- Confirmar versões compatíveis

#### **Erro de Configuração:**
- Verificar `.streamlit/config.toml`
- Confirmar `packages.txt` para dependências do sistema
- Verificar se o app.py está na raiz

### **Status do Deploy:**

- ✅ **Requirements atualizados**
- ✅ **Configuração otimizada**
- ✅ **Estrutura de páginas correta**
- ✅ **Dependências do sistema configuradas**

---

**Última atualização**: 2025-01-19  
**Versão**: 1.0  
**Status**: Ready for Streamlit Cloud
