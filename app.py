import streamlit as st

st.title("State Subsidy Rate Extractor")
st.write("Upload a state reimbursement rate table here.")

uploaded_file = st.file_uploader("Upload a PDF, PNG, or JPG file", type=["pdf", "png", "jpg", "jpeg"])

if uploaded_file is not None:
    st.success(f"File uploaded: {uploaded_file.name}")
