import streamlit as st
from google import genai
from google.genai import types
import pandas as pd
import io

st.title("State Subsidy Rate Extractor")

st.write("Step 1 — Upload instruction spreadsheet")
instruction_file = st.file_uploader("Upload instruction Excel file", type=["xlsx"])

st.write("Step 2 — Upload state reimbursement rate PDFs")
uploaded_files = st.file_uploader(
    "Upload one or more PDF files",
    type=["pdf"],
    accept_multiple_files=True
)

run_extraction = st.button("Run extraction")

if instruction_file:
    instructions_df = pd.read_excel(instruction_file)
    st.success("Instruction file loaded.")
    st.dataframe(instructions_df.head())

if uploaded_files:
    st.success(f"{len(uploaded_files)} PDF file(s) uploaded.")
    for f in uploaded_files:
        st.write(f.name)

if run_extraction and instruction_file and uploaded_files:
    st.info("Next step will connect instructions to each PDF.")
