import streamlit as st
import os
import google.generativeai as genai

st.title("State Subsidy Rate Extractor")
st.write("Upload a state reimbursement rate table here.")

uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

if uploaded_file is not None:
    st.success(f"File uploaded: {uploaded_file.name}")

    # Load API key from Streamlit secrets
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)

    model = genai.GenerativeModel("gemini-1.5-flash")

    st.write("Reading document with AI...")

    prompt = """
    Read this child care subsidy reimbursement rate table.
    Extract the infant full-time center-based monthly reimbursement rate.
    If multiple regions exist, list each separately.
    Return as:
    state | region | provider_type | age_group | attendance_type | rate_unit | amount
    """

    response = model.generate_content([
        prompt,
        uploaded_file.getvalue()
    ])

    st.subheader("Extracted Data")
    st.write(response.text)
