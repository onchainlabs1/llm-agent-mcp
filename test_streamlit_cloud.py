#!/usr/bin/env python3
"""
Teste Ultra-Simples para Streamlit Cloud
"""

import streamlit as st

st.set_page_config(
    page_title="Teste Simples",
    page_icon="🧪",
    layout="wide"
)

st.title("🧪 Teste Ultra-Simples")
st.write("Se você está vendo esta mensagem, o Streamlit está funcionando!")

st.success("✅ Teste bem-sucedido!")

# Teste básico de pandas
try:
    import pandas as pd
    st.success("✅ Pandas funcionando!")
    
    # DataFrame simples
    df = pd.DataFrame({
        'Teste': ['OK', 'OK', 'OK'],
        'Status': ['✅', '✅', '✅']
    })
    st.dataframe(df)
    
except Exception as e:
    st.error(f"❌ Erro com pandas: {e}")

# Teste básico de numpy
try:
    import numpy as np
    st.success("✅ Numpy funcionando!")
    st.write(f"Array: {np.array([1, 2, 3])}")
    
except Exception as e:
    st.error(f"❌ Erro com numpy: {e}")

st.write("---")
st.write("🎯 Se tudo estiver funcionando, o problema está no dashboard principal!")
