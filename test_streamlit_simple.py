#!/usr/bin/env python3
"""
Simple Streamlit test file for debugging deployment issues
"""

import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Simple Test",
    page_icon="🧪",
    layout="wide"
)

st.title("🧪 Simple Streamlit Test")
st.write("This is a simple test to verify basic functionality.")

# Test basic imports
st.write("✅ Streamlit imported successfully")
st.write("✅ Pandas imported successfully")

# Test basic functionality
df = pd.DataFrame({
    'A': [1, 2, 3],
    'B': ['a', 'b', 'c']
})

st.write("✅ DataFrame created successfully")
st.dataframe(df)

st.success("🎉 All basic tests passed!")
