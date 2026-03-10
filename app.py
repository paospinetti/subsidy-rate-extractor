import streamlit as st
from google import genai
from google.genai import types
import pandas as pd
import io

st.title("State Subsidy Rate Extractor")
st.write("Upload state reimbursement rate PDFs here.")

uploaded_files = st.file_uploader(
    "Upload one or more PDF files",
    type=["pdf"],
    accept_multiple_files=True
)

if uploaded_files:
    st.success(f"{len(uploaded_files)} file(s) uploaded.")

    st.subheader("Uploaded Files")
    for uploaded_file in uploaded_files:
        st.write(uploaded_file.name)
