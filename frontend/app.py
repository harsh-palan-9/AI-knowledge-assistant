import streamlit as st
from utils.styles import load_css

st.set_page_config(
    page_title="AI Knowledge Assistant",
    page_icon="🤖",
    layout="wide"
)

st.markdown(load_css(), unsafe_allow_html=True)

st.markdown('<div class="home-page">', unsafe_allow_html=True)

st.title("🤖 AI Knowledge Assistant")

with st.sidebar:
    st.title("🤖 AI Assistant")
    st.markdown("---")

    st.page_link("app.py", label="🏠 Home")
    st.page_link("pages/1_Login.py", label="🔐 Login")
    st.page_link("pages/2_Upload.py", label="📂 Upload")
    st.page_link("pages/3_Chat.py", label="💬 Chat")