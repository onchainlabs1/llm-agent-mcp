# 🤖 Agent Mode - Streamlit Cloud

Este documento descreve como usar o modo agente no ambiente Streamlit Cloud.

## ✅ **Funcionalidades Disponíveis**

### **1. Core Agent**
- **LLM Integration**: Suporte para Groq, OpenAI e Anthropic
- **Fallback Mode**: Modo simulado quando APIs não estão disponíveis
- **ISO Controls**: Implementação completa dos controles ISO 42001:2023

### **2. ISO 42001 Controls**
- **R001**: Bias Detection and Mitigation
- **R002**: Fact-checking and Confidence Scoring
- **R003**: Enhanced Prompt Sanitization
- **R008**: Data Encryption and Integrity

### **3. MCP Tools**
- **Tool Registry**: Sistema de registro de ferramentas
- **Schema Validation**: Validação de esquemas MCP
- **Tool Execution**: Execução segura de ferramentas

## 🚀 **Como Usar**

### **1. Acesso ao Modo Agente**
- Navegue para a página "🤖 Agent Mode Test"
- Execute os testes para verificar a funcionalidade
- Use as funcionalidades do agente conforme necessário

### **2. Configuração**
- O agente funciona em modo simulado por padrão
- Para usar APIs reais, configure as variáveis de ambiente
- Veja `env_example.txt` para exemplos de configuração

### **3. Funcionalidades Principais**
```python
# Exemplo de uso do agente
from agent.agent_core import call_llm

# Chamada simples
response = call_llm("Olá, como posso ajudar?")

# Resposta inclui metadados ISO
print(f"Response: {response['response']}")
print(f"Confidence: {response['confidence_score']}")
print(f"Bias Score: {response['bias_score']}")
```

## 🔧 **Configuração Avançada**

### **Variáveis de Ambiente**
```bash
# LLM Configuration
LLM_PROVIDER=groq  # ou openai, anthropic, simulated
LLM_MODEL=llama3-70b-8192

# API Keys
GROQ_API_KEY=your-key-here
OPENAI_API_KEY=your-key-here
ANTHROPIC_API_KEY=your-key-here

# MCP Configuration
MCP_SERVER_URL=http://localhost:8000
MCP_SCHEMAS_PATH=mcp_server/
```

### **Modo Simulado**
- Funciona sem chaves de API
- Respostas simuladas para desenvolvimento
- Controles ISO ainda ativos
- Ideal para testes e demonstrações

## 📊 **Monitoramento e Logs**

### **Logs de Auditoria**
- Todas as ações são registradas
- Controles ISO aplicados e documentados
- Rastreabilidade completa para auditorias

### **Métricas de Qualidade**
- Bias scores para cada interação
- Confidence scores para respostas
- Fact-checking results
- Operational control status

## 🛡️ **Segurança e Compliance**

### **ISO 42001:2023**
- ✅ Prompt sanitization
- ✅ Bias detection
- ✅ Fact-checking
- ✅ Data encryption
- ✅ Audit logging

### **Controles Operacionais**
- Rate limiting
- Session management
- Input validation
- Output sanitization

## 🚨 **Solução de Problemas**

### **Erros Comuns**
1. **Import Errors**: Verifique se todas as dependências estão instaladas
2. **Config Errors**: Use o modo simulado se as APIs não estiverem configuradas
3. **Permission Errors**: Verifique o acesso aos diretórios de dados

### **Testes de Diagnóstico**
- Execute `test_agent_mode.py` para verificar a funcionalidade
- Verifique os logs para identificar problemas
- Use o modo simulado para isolamento de problemas

## 📚 **Recursos Adicionais**

- **Documentação ISO**: Veja `docs/` para detalhes completos
- **Exemplos de Uso**: Verifique os testes para padrões de uso
- **Configuração**: Use `agent_config.py` para personalizações

## 🎯 **Próximos Passos**

1. **Teste o Modo Agente**: Execute `test_agent_mode.py`
2. **Configure APIs**: Adicione suas chaves de API se necessário
3. **Personalize**: Ajuste a configuração conforme suas necessidades
4. **Monitore**: Use os logs para acompanhar o uso e qualidade

---

**Status**: ✅ Pronto para uso em Streamlit Cloud
**Versão**: 1.0.0
**Última Atualização**: Dezembro 2024
