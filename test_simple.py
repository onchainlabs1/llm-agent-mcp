#!/usr/bin/env python3
"""
Teste Simples do Streamlit
"""

import streamlit as st

st.set_page_config(
    page_title="Teste Simples",
    page_icon="🧪",
    layout="wide"
)

st.title("🧪 Teste Simples do Streamlit")
st.write("Se você está vendo esta mensagem, o Streamlit está funcionando!")

st.success("✅ Teste bem-sucedido!")
st.info("ℹ️ Este é um teste básico para verificar se as dependências estão funcionando.")

# Teste de pandas
try:
    import pandas as pd
    st.success("✅ Pandas importado com sucesso!")
    
    # Criar um DataFrame simples
    df = pd.DataFrame({
        'Coluna 1': [1, 2, 3, 4, 5],
        'Coluna 2': ['A', 'B', 'C', 'D', 'E']
    })
    
    st.write("📊 DataFrame criado:")
    st.dataframe(df)
    
except ImportError as e:
    st.error(f"❌ Erro ao importar pandas: {e}")

# Teste de numpy
try:
    import numpy as np
    st.success("✅ Numpy importado com sucesso!")
    
    # Criar um array simples
    arr = np.array([1, 2, 3, 4, 5])
    st.write(f"🔢 Array numpy: {arr}")
    
except ImportError as e:
    st.error(f"❌ Erro ao importar numpy: {e}")

st.write("---")
st.write("🎯 Se tudo estiver funcionando, você pode tentar o dashboard principal!")
