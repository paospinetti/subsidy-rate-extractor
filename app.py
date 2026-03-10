import streamlit as st
from google import genai
from google.genai import types
import pandas as pd
import io

st.title("State Subsidy Rate Extractor")
st.write("Upload state reimbursement rate PDFs here.")

target_location = st.text_input("Region, county, or market area to pull")
age_group = st.selectbox("Age group", ["Infant", "Toddler"])
include_centers = st.checkbox("Include centers", value=True)
include_home_based = st.checkbox("Include home-based providers", value=True)

uploaded_files = st.file_uploader(
    "Upload one or more PDF files",
    type=["pdf"],
    accept_multiple_files=True
)

if uploaded_files:
    st.success(f"{len(uploaded_files)} file(s) uploaded.")

    st.subheader("Your extraction settings")
    st.write(f"Location: {target_location if target_location else 'Not entered yet'}")
    st.write(f"Age group: {age_group}")
    st.write(f"Include centers: {include_centers}")
    st.write(f"Include home-based providers: {include_home_based}")

    st.subheader("Uploaded Files")
    for uploaded_file in uploaded_files:
        st.write(uploaded_file.name)
