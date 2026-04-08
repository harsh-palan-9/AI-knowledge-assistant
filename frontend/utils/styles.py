def load_css():
    return """
    <style>

    /* ❌ HIDE DEFAULT STREAMLIT NAV */
    [data-testid="stSidebarNav"] {
        display: none;
    }

    /* 🔥 GLOBAL APP BACKGROUND */
    .stApp {
        background-color: #0E1117;
        color: white;
    }

    /* 🔥 SIDEBAR */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0B132B, #1C2541);
        color: white;
    }

    /* Sidebar text */
    section[data-testid="stSidebar"] * {
        color: white !important;
    }

    /* 🔥 HEADER */
    header[data-testid="stHeader"] {
        background: transparent;
    }

    /* 🔥 MAIN CONTAINER */
    .block-container {
        padding-top: 2rem;
    }

    /* 🔥 TITLES */
    h1, h2, h3 {
        color: #EAEAEA;
        font-weight: 600;
    }

    /* 🔥 INPUT FIELDS */
    input, textarea {
        background-color: #1E1E1E !important;
        color: white !important;
        border-radius: 8px !important;
        border: 1px solid #333 !important;
    }

    /* 🔥 BUTTONS */
    .stButton>button {
        background: linear-gradient(90deg, #1E88E5, #42A5F5);
        color: white;
        border-radius: 10px;
        border: none;
        padding: 10px 20px;
        font-weight: 500;
        transition: 0.3s;
    }

    .stButton>button:hover {
        transform: scale(1.05);
        background: linear-gradient(90deg, #1565C0, #1E88E5);
    }

    /* 🔥 CHAT MESSAGES */
    .stChatMessage {
        border-radius: 12px;
        padding: 10px;
        margin-bottom: 10px;
    }

    .user-msg {
        background: linear-gradient(90deg, #1E88E5, #42A5F5);
        color: white;
        border-radius: 12px;
        padding: 12px;
    }

    .ai-msg {
        background-color: #1E1E1E;
        color: #EAEAEA;
        border-radius: 12px;
        padding: 12px;
        border: 1px solid #333;
    }

    /* 🔥 FILE UPLOADER */
    .stFileUploader {
        background-color: #1E1E1E;
        padding: 10px;
        border-radius: 10px;
    }

    /* 🔥 SUCCESS / ERROR */
    .stSuccess {
        background-color: #1B5E20 !important;
        color: white !important;
    }

    .stError {
        background-color: #B71C1C !important;
        color: white !important;
    }

    </style>
    """