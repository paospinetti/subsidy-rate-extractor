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
    instructions_df["source_file_clean"] = (
        instructions_df["source_file"]
        .astype(str)
        .str.strip()
        .str.lower()
    )
    st.success("Instruction file loaded.")

if uploaded_files:
    st.success(f"{len(uploaded_files)} PDF file(s) uploaded.")

if run_extraction and instruction_file and uploaded_files:
    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)

    all_dataframes = []

    for uploaded_file in uploaded_files:
        uploaded_name_clean = uploaded_file.name.strip().lower()

        matching_rows = instructions_df[
            instructions_df["source_file_clean"] == uploaded_name_clean
        ]

        if matching_rows.empty:
            st.error(f"No instruction row for {uploaded_file.name}")
            continue

        row = matching_rows.iloc[0]

        prompt = f"""
Read this child care subsidy reimbursement rate table.

Pull these fields:
- state
- matched_region
- provider_type
- age_group
- attendance_type
- rate_unit
- quality_tier_exact_name
- rate_amount
- source_file

Use these file-specific instructions:
- Target region: {row['target_region']}
- Center provider label: {row['center_provider_label']}
- Home provider label: {row['home_provider_label']}
- Exclude provider label: {row['exclude_provider_label']}
- Infant age label: {row['infant_age_label']}
- Toddler age label: {row['toddler_age_label']}
- Quality tier label: {row['quality_tier_label']}

Rules:
- Pull the target region listed above.
- Pull rows matching the exact provider labels listed above.
- Do not use the excluded provider label.
- Use the exact age labels listed above.
- Use the exact quality tier label listed above.
- If quality_tier_label is ALL, return all quality tiers for the matching region.
- Keep the exact wording used in the PDF.
- Only pull full-time care, unless attendance is listed by hour.
- Use only information shown in the PDF.
- Do not guess.
- Do not round numbers.

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

        csv_text = response.text.strip()

        try:
            df = pd.read_csv(io.StringIO(csv_text))
            all_dataframes.append(df)
        except:
            st.error(f"Could not parse results from {uploaded_file.name}")

    if all_dataframes:
        combined_df = pd.concat(all_dataframes, ignore_index=True)

        st.subheader("Combined Results")
        st.dataframe(combined_df)

        excel_buffer = io.BytesIO()
        combined_df.to_excel(excel_buffer, index=False)
        excel_buffer.seek(0)

        st.download_button(
            label="Download Excel file",
            data=excel_buffer,
            file_name="state_subsidy_rates.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
