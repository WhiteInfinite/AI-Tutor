import streamlit as st
import google.generativeai as genai
st.set_page_config(page_title="📘 Yuga AI - Tutor", layout="centered")
st.title("📘 Yuga AI Tutor — Your Friendly AI Teaching Assistant")
st.caption("Ask anything educational — science, math, tech, history, and more! 🎓")
st.markdown("""
    <style>
    body {
        background-color: #f8f9fa;
    }
    .chat-container {
        padding-bottom: 100px;
    }
    .chat-bubble {
        background-color: #f1f3f6;
        border-radius: 10px;
        padding: 10px 15px;
        margin-bottom: 10px;
        color: #1c1c1e;
    }
    .user-bubble {
        background-color: #d1e7dd;
        color: #0f5132;
    }
    .fixed-bottom {
        position: fixed;
        bottom: 10px;
        left: 10px;
        right: 10px;
        background-color: transparent;
        box-shadow: none;
        padding: 0;
        z-index: 999;
    }
    .stTextInput > label {
        display: none;
    }
    input::placeholder {
        color: transparent;
    }
    </style>
""", unsafe_allow_html=True)
st.sidebar.title("🔐 Gemini API")
api_key = st.sidebar.text_input("Enter your Gemini API key", type="password")
if "chat" not in st.session_state:
    st.session_state.chat = None
if "messages" not in st.session_state:
    st.session_state.messages = []

system_instruction = (
    "You are an intelligent, friendly, and strict teaching assistant whose sole purpose is to help users learn. "
    "You only discuss educational topics such as science, math, technology, languages, history, and academic skills. "
    "You do not respond to questions that are off-topic, personal, or unrelated to learning. "
    "You explain concepts in a clear, step-by-step, and beginner-friendly way. Avoid jargon unless necessary, and use simple analogies or examples when helpful. "
    "Stay on topic and maintain a professional but encouraging tone. "
    "Be punctual and concise—get straight to the point, and organize your answers logically. "
    "You may use appropriate emojis 🎓📘✏️🧠 to emphasize ideas, highlight key points, or make concepts easier to understand. Emojis should support the explanation, not distract from it."
)
if api_key and st.session_state.chat is None:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(
        model_name="models/gemini-2.0-flash",
        system_instruction=system_instruction
    )
    st.session_state.chat = model.start_chat(history=[])
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)

for msg in st.session_state.messages:
    role = msg["role"]
    content = msg["content"]
    if role == "user":
        st.markdown(f"<div class='chat-bubble user-bubble'><b>You:</b> {content}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='chat-bubble'><b>📘 Tutor:</b> {content}</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

with st.container():
    st.markdown("<div class='fixed-bottom'>", unsafe_allow_html=True)
    if "message_sent" not in st.session_state:
        st.session_state.message_sent = False
    if not st.session_state.message_sent:
        user_input = st.text_input(" ", key="user_input", label_visibility="collapsed")
        if user_input:
            st.session_state.messages.append({"role": "user", "content": user_input})
            with st.spinner("Tutor is thinking... 🧠"):
                try:
                    response = st.session_state.chat.send_message(user_input)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                except Exception as e:
                    st.error(f"❌ Error: {e}")
            st.session_state.message_sent = True
            st.rerun()
    else:
        st.session_state.message_sent = False
        st.session_state.user_input = ""
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
