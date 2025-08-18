# 🧪 Guia de Teste Local - Integração Phoenix

## 🚀 **Passo a Passo para Testar Localmente**

### **1. Verificar Instalação Phoenix**
```bash
# Verificar se Phoenix está instalado
pip list | grep phoenix

# Verificar versão
python3 -c "import phoenix; print(phoenix.__version__)"
```

### **2. Testar Imports Phoenix**
```bash
# Executar script de teste básico
python3 test_phoenix_local.py
```

**Resultado esperado:**
```
🧪 Phoenix Integration Test Suite
========================================
🧪 Testing Phoenix imports...
✅ phoenix.trace imported successfully
✅ phoenix.evaluate imported successfully
✅ phoenix.evaluate.llm_eval imported successfully
```

### **3. Iniciar Servidor Phoenix (Opcional)**
```bash
# Iniciar servidor Phoenix em background
phoenix serve &

# Verificar se está rodando
lsof -i :6006

# Ou usar o script de configuração
python3 phoenix_config.py
```

**URLs disponíveis:**
- **Phoenix**: http://localhost:6006
- **Dashboard**: http://localhost:8501

### **4. Testar Dashboard com Phoenix**
```bash
# Executar dashboard
streamlit run iso_dashboard.py

# Ou em porta específica se 8501 estiver ocupada
streamlit run iso_dashboard.py --server.port 8502
```

### **5. Navegar para Nova Aba LLM Quality**
1. Abra o dashboard no navegador
2. Role para baixo até **"📚 Records (Evidence)"**
3. Clique na aba **"🔍 LLM Quality"** (6ª aba)

## 🔍 **O que Testar na Aba LLM Quality**

### **✅ Status Phoenix**
- Deve mostrar "✅ Phoenix Integration Active"
- Métricas de qualidade em tempo real

### **🚀 Botões de Ação**
- **"🔍 Run Quality Assessment"** - Executa avaliação
- **"📊 Show Quality Trends"** - Mostra tendências

### **📊 Métricas de Qualidade**
- Overall Quality Score
- Hallucination Risk
- Relevance Score
- Compliance Status

### **📈 Gráficos e Tendências**
- Quality Trends (últimos 7 dias)
- Quality Insights
- Compliance Information

## 🧪 **Scripts de Teste Disponíveis**

### **1. Teste Básico**
```bash
python3 test_phoenix_local.py
```

### **2. Configuração Phoenix**
```bash
python3 phoenix_config.py
```

### **3. Teste Dashboard**
```bash
streamlit run iso_dashboard.py
```

## 🚨 **Solução de Problemas**

### **Problema: Phoenix não encontrado**
```bash
# Reinstalar Phoenix
pip uninstall arize-phoenix
pip install arize-phoenix

# Verificar instalação
python3 -c "import phoenix; print('OK')"
```

### **Problema: Erro de import**
```bash
# Verificar Python path
python3 -c "import sys; print(sys.path)"

# Verificar versão Python
python3 --version
```

### **Problema: Dashboard não carrega**
```bash
# Verificar dependências
pip install -r requirements.txt

# Verificar sintaxe
python3 -m py_compile iso_dashboard.py
```

### **Problema: Phoenix server não inicia**
```bash
# Verificar se porta está livre
lsof -i :6006

# Matar processos na porta
pkill -f phoenix

# Tentar porta diferente
phoenix serve --port 6007
```

## 📊 **Resultados Esperados**

### **✅ Teste Bem-sucedido**
- Dashboard carrega sem erros
- Aba LLM Quality aparece
- Métricas de qualidade são exibidas
- Botões de ação funcionam
- Phoenix integration mostra "Active"

### **⚠️ Teste com Limitações**
- Dashboard carrega mas Phoenix não disponível
- Métricas básicas funcionam (fallback)
- Mensagem de aviso sobre Phoenix

### **❌ Teste Falhou**
- Erros de import ou sintaxe
- Dashboard não carrega
- Funcionalidades não funcionam

## 🔧 **Comandos Úteis para Debug**

```bash
# Verificar processos Python
ps aux | grep python

# Verificar portas em uso
lsof -i :8501
lsof -i :6006

# Verificar logs Streamlit
streamlit run iso_dashboard.py --logger.level debug

# Testar módulo específico
python3 -c "from iso_dashboard import run_phoenix_quality_check; print('OK')"
```

## 📝 **Checklist de Teste**

- [ ] Phoenix instalado e importável
- [ ] Dashboard carrega sem erros
- [ ] Nova aba LLM Quality aparece
- [ ] Métricas de qualidade são exibidas
- [ ] Botões de ação funcionam
- [ ] Phoenix integration status correto
- [ ] Gráficos e tendências funcionam
- [ ] Compliance information exibida
- [ ] Audit trail funciona

## 🎯 **Próximos Passos Após Teste**

1. **Se tudo funcionar**: Dashboard está pronto para portfolio
2. **Se houver problemas**: Usar troubleshooting acima
3. **Para demonstração**: Preparar dados de exemplo
4. **Para deploy**: Configurar hospedagem (Streamlit Cloud)

---

**Status**: ✅ Pronto para Teste  
**Última Atualização**: Janeiro 2025  
**Versão**: 1.0
