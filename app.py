"""
app.py
------
Streamlit UI layer for CareerIQ — AI Career Advisor
Clean, readable, professional UI (light theme).
"""

import streamlit as st
from chat_manager import ChatSession
from gemini_client import get_gemini_client
from prompt_manager import get_welcome_message
from utils.pdf_utils import extract_text_from_pdf
from logger import get_logger

logger = get_logger(__name__)

# ---------------------------------------------------------------------------
# Page Config
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="CareerIQ — AI Career Advisor",
    page_icon="🚀",
    layout="wide",
)

# ---------------------------------------------------------------------------
# Clean Light Theme CSS
# ---------------------------------------------------------------------------

st.markdown("""
<style>
.stApp {
    background-color: #f8fafc;
}

[data-testid="stSidebar"] {
    background-color: #ffffff;
    border-right: 1px solid #e5e7eb;
}

.main-header {
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    padding: 24px;
    border-radius: 14px;
    text-align: center;
    margin-bottom: 24px;
}

.main-header h1 {
    color: white;
    margin: 0;
    font-size: 2.2rem;
}

.main-header p {
    color: rgba(255,255,255,0.9);
    margin-top: 8px;
}

[data-testid="stChatMessage"] {
    background-color: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    padding: 10px;
    margin-bottom: 10px;
}

[data-testid="stChatInput"] textarea {
    background-color: #ffffff !important;
    border: 1px solid #d1d5db !important;
    color: #111827 !important;
    border-radius: 10px !important;
}

.footer-text {
    text-align: center;
    font-size: 0.8rem;
    color: #6b7280;
    margin-top: 20px;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Session State
# ---------------------------------------------------------------------------

def init_state():
    if "chat_session" not in st.session_state:
        st.session_state.chat_session = ChatSession()

    if "gemini_client" not in st.session_state:
        try:
            st.session_state.gemini_client = get_gemini_client()
            st.session_state.api_ok = True
        except Exception as e:
            st.session_state.api_ok = False
            st.session_state.api_error = str(e)

    if "welcome_shown" not in st.session_state:
        st.session_state.welcome_shown = False

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------

def render_sidebar():
    with st.sidebar:
        st.markdown("## 🚀 CareerIQ")
        st.caption("Your AI Career Advisor")

        if st.session_state.api_ok:
            st.success("API Connected")
        else:
            st.error("API Error")
            st.error(st.session_state.api_error)

        st.divider()

        session = st.session_state.chat_session
        st.metric("Messages", session.message_count)

        st.divider()

        if st.button("🧹 Clear Conversation", use_container_width=True):
            session.clear()
            st.session_state.welcome_shown = False
            st.rerun()

        st.markdown(
            '<div class="footer-text">Powered by Google Gemini & Streamlit</div>',
            unsafe_allow_html=True,
        )

# ---------------------------------------------------------------------------
# Main UI
# ---------------------------------------------------------------------------

def render_header():
    st.markdown("""
    <div class="main-header">
        <h1>🚀 CareerIQ — AI Career Advisor</h1>
        <p>Expert career guidance powered by Google Gemini</p>
    </div>
    """, unsafe_allow_html=True)

def show_welcome():
    if not st.session_state.welcome_shown and st.session_state.chat_session.is_empty():
        with st.chat_message("assistant"):
            st.markdown(get_welcome_message())
        st.session_state.welcome_shown = True

def render_history():
    session = st.session_state.chat_session
    for msg in session.get_history_for_display():
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

def handle_user_message(text: str):
    session = st.session_state.chat_session
    client = st.session_state.gemini_client

    session.add_user_message(text)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            reply, tokens = client.send_message(text, session)
        st.markdown(reply)

    session.add_model_message(reply)
    session.update_token_count(tokens)

# ---------------------------------------------------------------------------
# Optional PDF Resume Upload
# ---------------------------------------------------------------------------

def render_pdf_upload():
    st.divider()
    st.subheader("📄 Resume PDF Analysis (Optional)")

    pdf = st.file_uploader(
        "Upload your resume (text-based PDF only)",
        type=["pdf"]
    )

    if pdf:
        with st.spinner("Extracting text from resume..."):
            text = extract_text_from_pdf(pdf)

        if not text:
            st.warning("Unable to extract text. This may be a scanned PDF.")
            return

        st.success("Resume text extracted successfully.")

        if st.button("Analyze Resume"):
            prompt = (
                "Here is my resume content:\n\n"
                f"{text}\n\n"
                "Please review it and suggest improvements."
            )
            handle_user_message(prompt)
            st.rerun()

# ---------------------------------------------------------------------------
# App Entry
# ---------------------------------------------------------------------------

def main():
    init_state()
    render_sidebar()
    render_header()

    if not st.session_state.api_ok:
        st.stop()

    show_welcome()
    render_history()
    render_pdf_upload()

    user_input = st.chat_input("Ask me anything about your career...")
    if user_input:
        handle_user_message(user_input)
        st.rerun()

if __name__ == "__main__":
    main()