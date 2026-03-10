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

run_extraction = st.button("Run extraction")

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

if run_extraction and uploaded_files:
    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)

    for uploaded_file in uploaded_files:
        st.subheader(f"Processing: {uploaded_file.name}")

        prompt = f"""
Read this child care subsidy reimbursement rate table.

For each PDF, pull:
- state
- the matching county or region based on what I type into the app
- provider type
- age group
- attendance type
- rate unit
- exact quality tier name as written in the PDF
- rate amount
- source file name

Rules:
- Look for the county, region, or market area that is the most populous region.
- If the PDF has multiple matching rows for that location, return all relevant rows.
- Pull both center-based and home-based providers.
- Never use large home-based providers.
- Pull for infants the closest to a 1 year old and for toddler close to a two year old.
- Only pull full-time care, unless the attendance type is listed by hour.
- Pull all quality tiers available for the matching location.
- Keep the exact quality-tier wording used by the state.
- Do not rename, simplify, or standardize tier labels.
- If a state does not use quality tiers, write null.
- If no matching region or county is found, write null.
- Use only information shown in the PDF.
- Do not guess.
- Do not round up or down. Keep all decimal points shown.

User selections:
- Target location: {target_location}
- Age group: {age_group}
- Include centers: {include_centers}
- Include home-based providers: {include_home_based}

Return the result as CSV with this exact header:
state,matched_region,provider_type,age_group,attendance_type,rate_unit,quality_tier_exact_name,rate_amount,source_file

Put each result on its own new line.
Do not include any explanation before or after the CSV.
Set source_file equal to the uploaded file name.
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

        st.text(response.text)
