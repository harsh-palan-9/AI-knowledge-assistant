from utils.api_client import upload_file
import streamlit as st
from utils.styles import load_css
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

st.markdown(load_css(), unsafe_allow_html=True)

if "token" not in st.session_state or not st.session_state.token:
    st.warning("Please login to upload documents.")
    st.switch_page("pages/1_Login.py")

import jwt

decoded = jwt.decode(st.session_state.token, options={"verify_signature": False})

roles = decoded.get("realm_access", {}).get("roles", [])

if "admin" not in roles:
    st.error("You do not have permission to upload documents.")
    st.markdown("---")
    if st.button("➡️ Go to Chat"):
        st.switch_page("pages/3_Chat.py")
    st.stop()

st.title("📂 Upload Document")

uploaded_file = st.file_uploader(
    "Upload PDF/TXT",
    type=["pdf", "txt"]
)

if uploaded_file:
    if st.button("Upload"):
        logger.debug(f"Starting upload for file: {uploaded_file.name}")
        logger.debug(f"Token present: {'token' in st.session_state and bool(st.session_state.token)}")
        
        with st.spinner("Uploading..."):
            res = upload_file(uploaded_file)
        
        logger.debug(f"Upload response: {res}")
        
        if "error" in res:
            logger.error(f"Upload error - Status: {res.get('status_code')}, Message: {res.get('message')}, Error: {res.get('error')}")
            logger.error(f"Full error response: {res}")
            st.write("**Debug Info:** Check console logs for detailed error information")
            
            if res.get("status_code") == 401:
                st.error(res.get("message", "Authentication failed"))
                logger.warning("Authentication failed - Token may be invalid or expired")
                if st.button("Login Again"):
                    st.switch_page("pages/1_Login.py")
            else:
                st.error(f"Upload failed: {res.get('error', 'Unknown error')}")
        else:
            logger.info("Upload successful!")
            st.success("✅ Upload successful!")
            st.switch_page("pages/3_Chat.py")

