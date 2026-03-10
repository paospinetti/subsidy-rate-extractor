import streamlit as st
from google import genai
from google.genai import types

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
If multiple regions or categories exist, list each separately.

Return the result as CSV with this exact header on the first line:
state,region,provider_type,age_group,attendance_type,rate_unit,amount

After the header, put each result on its own new line.
Do not combine multiple rows into one paragraph.
Do not include bullets, explanations, or extra text.

Use only information that appears in the document.
If something is missing, write null.
"""

    pdf_bytes = uploaded_file.read()

    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=[
            types.Part.from_bytes(
                data=pdf_bytes,
                mime_type="application/pdf",
            ),
            prompt,
        ],
    )

    st.subheader("Extracted Data")
    st.write(response.text)
