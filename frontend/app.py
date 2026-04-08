import streamlit as st
from utils.api_client import upload_file, ask_question

# 🔹 Page Config
st.set_page_config(
    page_title="AI Knowledge Assistant",
    page_icon="🤖",
    layout="wide"
)

# 🔹 Custom CSS (🔥 makes UI look premium)
st.markdown("""
<style>
    .main {
        background-color: #0E1117;
    }
    .stChatMessage {
        border-radius: 12px;
        padding: 10px;
        margin-bottom: 10px;
    }
    .user-msg {
        background-color: #1E88E5;
        color: white;
        border-radius: 10px;
        padding: 10px;
    }
    .ai-msg {
        background-color: #2E2E2E;
        color: white;
        border-radius: 10px;
        padding: 10px;
    }
</style>
""", unsafe_allow_html=True)

# 🔹 Sidebar
with st.sidebar:
    st.title("🤖 AI Assistant")
    st.markdown("### 📂 Upload Document")

    uploaded_file = st.file_uploader(
        "Upload PDF/TXT",
        type=["pdf", "txt"]
    )

    if uploaded_file:
        if st.button("🚀 Process Document"):
            with st.spinner("Processing..."):
                res = upload_file(uploaded_file)
            st.success("✅ Document Ready!")

    st.markdown("---")
    st.markdown("### ℹ️ About")
    st.write("Ask questions from your documents using AI.")

# 🔹 Main Title
st.title("💬 AI Knowledge Assistant")

# 🔹 Chat Session Memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# 🔹 Display Chat History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg["role"] == "user":
            st.markdown(f'<div class="user-msg">{msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="ai-msg">{msg["content"]}</div>', unsafe_allow_html=True)

# 🔹 Chat Input
query = st.chat_input("Ask something about your documents...")

if query:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": query})

    with st.chat_message("user"):
        st.markdown(f'<div class="user-msg">{query}</div>', unsafe_allow_html=True)

    # AI response
    with st.chat_message("assistant"):
        with st.spinner("🤖 Thinking..."):
            response = ask_question(query)
            answer = response.get("answer", "No answer found")

            st.markdown(f'<div class="ai-msg">{answer}</div>', unsafe_allow_html=True)

    # Save AI response
    st.session_state.messages.append({"role": "assistant", "content": answer})