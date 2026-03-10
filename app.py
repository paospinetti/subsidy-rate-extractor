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

instructions_df = None

if instruction_file:
    instructions_df = pd.read_excel(instruction_file)
    st.success("Instruction file loaded.")
    st.dataframe(instructions_df.head())

if uploaded_files:
    st.success(f"{len(uploaded_files)} PDF file(s) uploaded.")
    for f in uploaded_files:
        st.write(f.name)

if run_extraction and instruction_file and uploaded_files:
    st.subheader("Instruction match check")

    for uploaded_file in uploaded_files:
        matching_rows = instructions_df[instructions_df["source_file"] == uploaded_file.name]

        st.write(f"PDF: {uploaded_file.name}")

        if not matching_rows.empty:
            st.success("Match found in instruction file")
            st.dataframe(matching_rows)
        else:
            st.error("No matching row found in instruction file")
