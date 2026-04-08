import streamlit as st
from utils.api_client import ask_question
from utils.styles import load_css

st.markdown(load_css(), unsafe_allow_html=True)

if "token" not in st.session_state or not st.session_state.token:
    st.warning("Please login to start chatting.")
    st.stop()

st.title("💬 Chat with your AI Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

query = st.chat_input("Ask something about your documents...")

if query:
    st.session_state.messages.append({"role": "user", "content": query})

    with st.chat_message("user"):
        st.write(query)

    with st.chat_message("assistant"):
        with st.spinner("🤖 Thinking..."):
            response = ask_question(query)
            answer = response.get("answer", "No answer found")
            st.write(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})