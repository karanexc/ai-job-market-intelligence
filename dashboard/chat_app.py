import sys
import os

# allow imports from project root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import pandas as pd
from ai.sql_agent import ask

st.set_page_config(page_title="AI Job Market Assistant")

st.title("AI Job Market Intelligence Assistant")

st.write("Ask questions about the tech job market.")

question = st.text_input("Ask a question")

if question:

    result = ask(question)

    st.subheader("Answer")

    if len(result) == 0:
        st.write("No results found.")
    else:
        df = pd.DataFrame(result)
        st.dataframe(df)