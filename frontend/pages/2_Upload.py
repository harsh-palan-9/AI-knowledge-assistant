from utils.api_client import upload_file
import streamlit as st
from utils.styles import load_css

st.markdown(load_css(), unsafe_allow_html=True)

if "token" not in st.session_state or not st.session_state.token:
    st.warning("Please login to upload documents.")
    st.stop()

st.title("📂 Upload Document")

uploaded_file = st.file_uploader(
    "Upload PDF/TXT",
    type=["pdf", "txt"]
)

if uploaded_file:
    if st.button("Upload"):
        with st.spinner("Uploading..."):
            res = upload_file(uploaded_file)
        st.success("✅ Document Uploaded!")
        