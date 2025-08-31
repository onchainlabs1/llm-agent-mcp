# 🚀 Streamlit Cloud Deployment Guide

## 📋 Pré-requisitos

- ✅ Conta GitHub com repositório público
- ✅ Conta Streamlit Cloud (gratuita)
- ✅ Projeto funcionando localmente

## 🔧 Configuração do Repositório

### 1. Estrutura de Arquivos
```
llm-agent-mcp/
├── requirements.txt          # Dependências Python
├── .streamlit/              # Configuração Streamlit
│   └── config.toml
├── app.py                   # Interface principal
├── data/                    # Dados estáticos
└── README.md               # Documentação
```

### 2. Criar requirements.txt
```bash
# Gerar requirements.txt
pip freeze > requirements.txt

# Ou criar manualmente:
streamlit>=1.28.0
pandas>=2.0.0
numpy>=1.24.0
plotly>=5.15.0
arize-phoenix>=2.0.0
```

### 3. Configuração Streamlit
```bash
mkdir .streamlit
```

Criar `.streamlit/config.toml`:
```toml
[server]
port = 8501
enableCORS = false
enableXsrfProtection = false

[browser]
gatherUsageStats = false

[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f5f7fb"
textColor = "#0f172a"
```

## 🌐 Deploy no Streamlit Cloud

### 1. Acessar Streamlit Cloud
- Vá para [share.streamlit.io](https://share.streamlit.io)
- Faça login com sua conta GitHub

### 2. Conectar Repositório
- Clique em "New app"
- Selecione seu repositório: `onchainlabs1/llm-agent-mcp`
- Branch: `main`
- Main file path: `app.py`

### 3. Configurar Variáveis de Ambiente
```bash
# Se necessário, adicione variáveis de ambiente
PHOENIX_ENABLED=true
STREAMLIT_SERVER_PORT=8501
```

### 4. Deploy
- Clique em "Deploy!"
- Aguarde o build (2-5 minutos)
- URL será: `https://llm-agent-mcp-iso.streamlit.app`

## 🔄 Deploy Automático

### 1. Push para GitHub
```bash
git add .
git commit -m "feat: prepare for Streamlit Cloud deployment"
git push origin main
```

### 2. Streamlit Cloud detecta mudanças
- Build automático a cada push
- Deploy em produção
- Logs disponíveis na interface

## 🐛 Troubleshooting

### Erro: "Module not found"
```bash
# Verificar requirements.txt
pip list > installed_packages.txt
# Comparar com requirements.txt
```

### Erro: "Port already in use"
```bash
# Verificar .streamlit/config.toml
# Porta deve ser 8501 para Streamlit Cloud
```

### Erro: "File not found"
```bash
# Verificar estrutura de arquivos
# Todos os arquivos devem estar no repositório
```

## 📊 Monitoramento

### 1. Logs do App
- Acesse Streamlit Cloud
- Clique em "Manage app"
- Aba "Logs"

### 2. Métricas
- Usuários ativos
- Tempo de resposta
- Erros

### 3. Versões
- Histórico de deploys
- Rollback se necessário

## 🔒 Segurança

### 1. Variáveis Sensíveis
```bash
# NÃO commitar senhas/API keys
# Usar variáveis de ambiente do Streamlit Cloud
```

### 2. Acesso
- Repositório pode ser público
- App será público por padrão
- Considere restrições se necessário

## 🎯 Próximos Passos

1. ✅ Teste local funcionando
2. 🔄 Push para GitHub
3. 🌐 Deploy no Streamlit Cloud
4. 🧪 Teste online
5. 📈 Compartilhe URL

## 📞 Suporte

- [Streamlit Cloud Docs](https://docs.streamlit.io/streamlit-community-cloud)
- [GitHub Issues](https://github.com/onchainlabs1/llm-agent-mcp/issues)
- [Streamlit Community](https://discuss.streamlit.io/)

---

**🎉 Seu dashboard ISO 42001 estará online e acessível globalmente!**
