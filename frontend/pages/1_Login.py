import streamlit as st
from utils.api_client import login
from utils.styles import load_css

st.set_page_config(
    page_title="Login - AI Knowledge Assistant",
    page_icon="🔒"
)

st.markdown(load_css(), unsafe_allow_html=True)

st.title("🔒 Login to AI Knowledge Assistant")

if "token" not in st.session_state:
    st.session_state.token = None

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login"):
    with st.spinner("Authenticating..."):
        response = login(username, password)

    if "access_token" in response:
        st.session_state.token = response["access_token"]
        st.success("✅ Login successful!")
        st.switch_page("pages/2_Upload.py")
    else:
        status = response.get("status_code")
        error_message = response.get("error_description") or response.get("error") or str(response)
        st.error(f"❌ Login failed ({status}): {error_message}")
        st.write(response)