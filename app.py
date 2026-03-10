import streamlit as st
from google import genai
import tempfile
import os

st.title("State Subsidy Rate Extractor")
st.write("Upload a state reimbursement rate table here.")

uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

if uploaded_file is not None:
    st.success(f"File uploaded: {uploaded_file.name}")

    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)

    st.write("Reading document with AI...")

    prompt = """
    Read this child care subsidy reimbursement rate table.
    Extract the infant full-time center-based monthly reimbursement rate.
    If multiple regions exist, list each separately.
    Return as:
    state | region | provider_type | age_group | attendance_type | rate_unit | amount
    """

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.getbuffer())
        tmp_file_path = tmp_file.name

    try:
        gemini_file = client.files.upload(file=tmp_file_path)

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[prompt, gemini_file]
        )

        st.subheader("Extracted Data")
        st.write(response.text)

    finally:
        os.remove(tmp_file_path)
