def load_css():
    return """
    <style>

    /*  GLOBAL RESET */
    * {
        font-family: 'Inter', sans-serif;
    }

    /*  BACKGROUND */
    .stApp {
        background: linear-gradient(135deg, #0F172A, #020617);
        color: #E2E8F0;
    }

    /*  REMOVE SIDEBAR */
    [data-testid="stSidebarNav"] {
        display: none;
    }

    header[data-testid="stHeader"] {
        background: transparent;
    }

    /*  CENTER LAYOUT */
    /*  CENTER LAYOUT (UPDATED) */
    section.main {
        display: flex;
        justify-content: center;
        align-items: center;   /* vertical center */
        min-height: 100vh;     /* full screen height */
    }

    .block-container {
        max-width: 900px;
        padding-top: 0rem;     /* remove top spacing */
        text-align: center;    /* optional */
    }

    /*  HOME PAGE CENTER ONLY */
    .home-page .block-container {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 80vh;
        text-align: center;
        padding-top: 0 !important;
    }

    /*  TITLES */
    h1 {
        text-align: center;
        font-size: 2.4rem;
        font-weight: 700;
        color: #60A5FA;
        margin-bottom: 25px;
    }

    h2, h3 {
        color: #E2E8F0;
    }

    /*  LABELS (FIXED) */
    label {
        color: #CBD5F5 !important;
        font-size: 14px;
        font-weight: 500;
    }

    /*  INPUT FIELDS */
    input, textarea {
        background-color: #020617 !important;
        color: #FFFFFF !important;
        border: 1px solid #334155 !important;
        border-radius: 10px !important;
        padding: 12px !important;
    }

    input::placeholder, textarea::placeholder {
        color: #94A3B8 !important;
    }

    /*  BUTTONS */
    .stButton > button {
        width: 100%;
        background: linear-gradient(90deg, #2563EB, #3B82F6);
        color: white;
        border-radius: 10px;
        border: none;
        padding: 12px;
        font-weight: 600;
        transition: 0.2s ease;
    }

    .stButton > button:hover {
        background: linear-gradient(90deg, #1D4ED8, #2563EB);
        transform: translateY(-1px);
    }

    /*  FILE UPLOADER */
    .stFileUploader {
        background: #020617;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 15px;
    }

    /*  ALERTS */
    .stWarning {
        background: #7F1D1D !important;
        color: #FECACA !important;
        border-radius: 10px;
        padding: 12px;
    }

    .stError {
        background: #991B1B !important;
        color: #FECACA !important;
        border-radius: 10px;
        padding: 12px;
    }

    .stSuccess {
        background: #14532D !important;
        color: #BBF7D0 !important;
        border-radius: 10px;
        padding: 12px;
    }

    /*  CHAT MESSAGES BASE */
    .stChatMessage {
        background: #020617;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 12px;
        margin-bottom: 12px;
    }

    /*  USER MESSAGE */
    .stChatMessage[data-testid="stChatMessage-user"] {
        background: #2563EB;
    }

    /*  ASSISTANT MESSAGE */
    .stChatMessage[data-testid="stChatMessage-assistant"] {
        background: #020617;
    }

    /*  FORCE TEXT VISIBILITY (CRITICAL FIX) */
    .stChatMessage * {
        color: #F1F5F9 !important;
        opacity: 1 !important;
    }

    .stChatMessage[data-testid="stChatMessage-user"] * {
        color: #FFFFFF !important;
    }

    .stChatMessage[data-testid="stChatMessage-assistant"] * {
        color: #E2E8F0 !important;
    }

    .stChatMessage p,
    .stChatMessage span,
    .stChatMessage div {
        color: inherit !important;
    }

    /*  CHAT INPUT */
    textarea {
        background-color: #020617 !important;
        color: #FFFFFF !important;
        font-weight: 500;
    }

    textarea::placeholder {
        color: #94A3B8 !important;
    }

    /*  SCROLLBAR */
    ::-webkit-scrollbar {
        width: 6px;
    }

    ::-webkit-scrollbar-thumb {
        background: #475569;
        border-radius: 10px;
    }

    </style>
    """