"""
Streamlit Web UI for DSA Learning Assistant
"""

import streamlit as st
import os
from dotenv import load_dotenv
from dsa_assistant import DSAAssistant

# Page configuration
st.set_page_config(
    page_title="DSA Learning Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': "# DSA Learning Assistant 🎓\nYour personal Data Structures & Algorithms tutor powered by RAG and Groq AI!"
    }
)

# Custom CSS
st.markdown("""
    <style>
    /* Keyframe Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes slideIn {
        from { transform: translateX(-20px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }
    
    @keyframes wiggle {
        0%, 100% { transform: rotate(-3deg); }
        50% { transform: rotate(3deg); }
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-15px); }
    }
    
    @keyframes glow {
        0%, 100% { box-shadow: 0 0 5px rgba(255, 215, 0, 0.5); }
        50% { box-shadow: 0 0 20px rgba(255, 215, 0, 0.8), 0 0 30px rgba(255, 215, 0, 0.6); }
    }
    
    @keyframes rainbow {
        0% { filter: hue-rotate(0deg); }
        100% { filter: hue-rotate(360deg); }
    }
    
    @keyframes typewriter {
        from { width: 0; }
        to { width: 100%; }
    }
    
    @keyframes sparkle {
        0%, 100% { opacity: 0; transform: scale(0) rotate(0deg); }
        50% { opacity: 1; transform: scale(1) rotate(180deg); }
    }
    
    @keyframes slideUp {
        from { transform: translateY(30px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }
    
    @keyframes rotate3D {
        0% { transform: perspective(1000px) rotateY(0deg); }
        100% { transform: perspective(1000px) rotateY(360deg); }
    }
    
    @keyframes flip3D {
        0% { transform: perspective(1000px) rotateX(0deg); }
        100% { transform: perspective(1000px) rotateX(360deg); }
    }
    
    @keyframes tilt3D {
        0%, 100% { transform: perspective(1000px) rotateY(-5deg) rotateX(2deg); }
        50% { transform: perspective(1000px) rotateY(5deg) rotateX(-2deg); }
    }
    
    @keyframes pop3D {
        0% { transform: perspective(1000px) translateZ(0px) scale(1); }
        50% { transform: perspective(1000px) translateZ(50px) scale(1.1); }
        100% { transform: perspective(1000px) translateZ(0px) scale(1); }
    }
    
    @keyframes spin3D {
        0% { transform: perspective(1000px) rotateY(0deg) rotateX(0deg); }
        100% { transform: perspective(1000px) rotateY(360deg) rotateX(360deg); }
    }
    
    @keyframes wave {
        0%, 100% { transform: rotate(0deg); }
        25% { transform: rotate(20deg); }
        75% { transform: rotate(-20deg); }
    }
    
    @keyframes typing {
        0%, 100% { opacity: 0.3; }
        50% { opacity: 1; }
    }
    
    @keyframes confetti {
        0% { transform: translateY(0) rotateZ(0deg); opacity: 1; }
        100% { transform: translateY(100px) rotateZ(360deg); opacity: 0; }
    }
    
    /* Main container with animated background */
    .main {
        padding: 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        animation: fadeIn 0.5s ease-in;
        position: relative;
        overflow-x: hidden;
        perspective: 1000px;
        transform-style: preserve-3d;
    }
    
    /* Animated background particles */
    .main::before {
        content: '✨';
        position: fixed;
        font-size: 30px;
        animation: float 3s ease-in-out infinite, sparkle 2s ease-in-out infinite;
        top: 10%;
        left: 10%;
        z-index: 0;
    }
    
    .main::after {
        content: '🌟';
        position: fixed;
        font-size: 25px;
        animation: float 4s ease-in-out infinite 1s, sparkle 2.5s ease-in-out infinite 0.5s;
        top: 30%;
        right: 15%;
        z-index: 0;
    }
    
    /* Input styling with glow effect */
    .stTextInput > div > div > input {
        font-size: 16px;
        border-radius: 15px;
        border: 3px solid transparent;
        background: linear-gradient(white, white) padding-box,
                    linear-gradient(135deg, #667eea, #764ba2, #f093fb, #f5576c) border-box;
        padding: 14px;
        transition: all 0.4s ease;
        animation: slideUp 0.6s ease-out;
    }
    
    .stTextInput > div > div > input:focus {
        animation: glow 1.5s ease-in-out infinite;
        transform: scale(1.02);
    }
    
    /* Chat message containers with playful animations */
    .chat-message {
        padding: 1.5rem;
        border-radius: 20px;
        margin-bottom: 1.5rem;
        display: flex;
        flex-direction: column;
        animation: slideIn 0.5s ease-out, bounce 0.3s ease-out 0.5s;
        box-shadow: 0 12px 24px rgba(0, 0, 0, 0.3);
        transition: all 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55);
        position: relative;
        overflow: hidden;
        transform-style: preserve-3d;
    }
    
    .chat-message::before {
        content: '✨';
        position: absolute;
        top: 10px;
        right: 10px;
        font-size: 20px;
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .chat-message:hover {
        transform: perspective(1000px) translateZ(30px) rotateY(3deg) rotateX(3deg) scale(1.03);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
    }
    
    .chat-message:hover::before {
        opacity: 1;
        animation: spin3D 2s ease-in-out infinite;
    }
    
    /* User message with dancing gradient */
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-left: 6px solid #ffd700;
        color: white;
        animation: slideIn 0.5s ease-out, tilt3D 5s ease-in-out infinite;
    }
    
    .user-message::after {
        content: '💭';
        position: absolute;
        top: 10px;
        left: 10px;
        font-size: 30px;
        animation: float 2s ease-in-out infinite, wave 1s ease-in-out infinite;
    }
    
    .user-message:hover {
        animation: pop3D 0.6s ease-in-out;
    }
    
    /* Assistant message with rainbow effect */
    .assistant-message {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        border-left: 6px solid #4caf50;
        color: white;
        animation: slideIn 0.5s ease-out 0.2s backwards, tilt3D 5s ease-in-out infinite 1s;
    }
    
    .assistant-message::after {
        content: '🎓';
        position: absolute;
        top: 10px;
        left: 10px;
        font-size: 30px;
        animation: bounce 1s ease-in-out infinite, rotate3D 8s linear infinite;
    }
    
    .assistant-message:hover {
        animation: flip3D 1s ease-in-out;
    }
    
    /* Typing indicator */
    .typing-indicator {
        display: inline-flex;
        align-items: center;
        gap: 10px;
        padding: 1.5rem 2rem;
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        border-radius: 25px;
        margin: 1rem 0;
        animation: pop3D 1.5s ease-in-out infinite;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
        transform-style: preserve-3d;
    }
    
    .typing-indicator:hover {
        transform: perspective(1000px) translateZ(20px) scale(1.05);
    }
    
    .typing-dot {
        width: 14px;
        height: 14px;
        border-radius: 50%;
        background: linear-gradient(135deg, #667eea, #764ba2);
        animation: typing 1.4s ease-in-out infinite;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
    }
    
    .typing-dot:nth-child(2) { animation-delay: 0.2s; }
    .typing-dot:nth-child(3) { animation-delay: 0.4s; }
    
    /* Message reactions */
    .message-reaction {
        display: inline-block;
        font-size: 28px;
        margin: 8px;
        cursor: pointer;
        transition: all 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55);
        animation: float 3s ease-in-out infinite;
        transform-style: preserve-3d;
    }
    
    .message-reaction:hover {
        transform: perspective(1000px) translateZ(40px) scale(1.5) rotate(20deg);
        animation: spin3D 0.8s ease-in-out;
        filter: drop-shadow(0 0 15px rgba(255, 215, 0, 0.8));
    }
    
    /* Message header with wiggle on hover */
    .message-header {
        font-weight: bold;
        margin-bottom: 1rem;
        font-size: 18px;
        display: flex;
        align-items: center;
        gap: 10px;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        z-index: 1;
    }
    
    .message-header:hover {
        animation: wiggle 0.5s ease-in-out;
    }
    
    /* Message content with smooth reveal */
    .message-content {
        font-size: 17px;
        line-height: 2;
        color: white;
        background-color: rgba(255, 255, 255, 0.15);
        padding: 18px;
        border-radius: 12px;
        backdrop-filter: blur(15px);
        box-shadow: inset 0 2px 8px rgba(0, 0, 0, 0.1);
        z-index: 1;
        animation: fadeIn 0.8s ease-out 0.3s backwards;
    }
    
    /* Sidebar with particles effect */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
        position: relative;
    }
    
    [data-testid="stSidebar"]::before {
        content: '🚀';
        position: absolute;
        font-size: 40px;
        animation: float 3s ease-in-out infinite, rainbow 10s linear infinite;
        top: 5%;
        right: 10%;
    }
    
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
        color: white;
    }
    
    /* Button styling with fun animations */
    .stButton > button {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white !important;
        border: none;
        border-radius: 15px;
        padding: 12px 24px;
        font-weight: bold;
        font-size: 16px;
        transition: all 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55);
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3);
        position: relative;
        overflow: hidden;
        transform-style: preserve-3d;
    }
    
    .stButton > button::before {
        content: '✨';
        position: absolute;
        left: -30px;
        top: 50%;
        transform: translateY(-50%);
        opacity: 0;
        transition: all 0.4s ease;
        font-size: 20px;
    }
    
    .stButton > button:hover {
        transform: perspective(1000px) translateZ(30px) rotateY(5deg) scale(1.1);
        box-shadow: 0 15px 30px rgba(240, 147, 251, 0.5);
        animation: pop3D 0.3s ease-in-out;
    }
    
    .stButton > button:hover::before {
        left: 15px;
        opacity: 1;
        animation: spin3D 1s ease-in-out infinite;
    }
    
    .stButton > button:active {
        transform: perspective(1000px) translateZ(-10px) scale(0.95);
    }
    
    /* Form submit button special styling */
        transform: translateY(-50%);
        opacity: 0;
        transition: all 0.4s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-4px) scale(1.05);
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.3);
        animation: pulse 0.6s ease infinite;
    }
    
    .stButton > button:hover::before {
        left: 10px;
        opacity: 1;
    }
    
    .stButton > button:active {
        transform: scale(0.95);
        animation: bounce 0.3s ease;
    }
    
    /* Form button with special effects */
    .stFormSubmitButton > button {
        background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 15px !important;
        padding: 14px 28px !important;
        font-weight: bold !important;
        font-size: 18px !important;
        transition: all 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55) !important;
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2) !important;
        position: relative !important;
    }
    
    .stFormSubmitButton > button::after {
        content: '🚀';
        position: absolute;
        right: -30px;
        top: 50%;
        transform: translateY(-50%);
        opacity: 0;
        transition: all 0.4s ease;
    }
    
    .stFormSubmitButton > button:hover {
        transform: translateY(-4px) scale(1.08) rotate(-1deg) !important;
        box-shadow: 0 12px 24px rgba(0, 0, 0, 0.3) !important;
        animation: glow 1s ease-in-out infinite !important;
    }
    
    .stFormSubmitButton > button:hover::after {
        right: 15px;
        opacity: 1;
        animation: bounce 0.5s ease infinite;
    }
    
    /* Spinner with rainbow effect */
    .stSpinner > div {
        border-top-color: #f5576c !important;
        animation: rainbow 2s linear infinite;
    }
    
    /* Text Input Styling - Make it visible and attractive */
    .stTextInput > div > div > input {
        background-color: white !important;
        color: #1a1a1a !important;
        border: 3px solid #667eea !important;
        border-radius: 15px !important;
        padding: 15px 20px !important;
        font-size: 16px !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2) !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #f5576c !important;
        box-shadow: 0 6px 20px rgba(245, 87, 108, 0.4) !important;
        transform: translateY(-2px) !important;
        outline: none !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #999 !important;
        font-style: italic !important;
    }
    
    /* Info boxes with slide animation */
    .stAlert {
        border-radius: 15px;
        animation: slideUp 0.6s ease-out;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    
    /* Title with bounce effect */
    h1, h2, h3 {
        color: white;
        text-shadow: 3px 3px 6px rgba(0, 0, 0, 0.4);
        animation: slideUp 0.8s ease-out;
    }
    
    h1:hover, h2:hover {
        animation: bounce 0.5s ease;
    }
    
    /* Welcome box with floating animation */
    .welcome-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem;
        border-radius: 25px;
        text-align: center;
        color: white;
        animation: fadeIn 1s ease-in, float 3s ease-in-out infinite 1s;
        box-shadow: 0 12px 24px rgba(0, 0, 0, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .welcome-box::before {
        content: '🎉';
        position: absolute;
        font-size: 60px;
        top: 20px;
        right: 20px;
        animation: bounce 1s ease-in-out infinite, rainbow 3s linear infinite;
    }
    
    .welcome-box::after {
        content: '🎊';
        position: absolute;
        font-size: 50px;
        bottom: 20px;
        left: 20px;
        animation: wiggle 1s ease-in-out infinite, rainbow 3s linear infinite 1.5s;
    }
    
    /* Info boxes with glow */
    .info-box {
        background: rgba(255, 255, 255, 0.15);
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 1.5rem;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3);
        animation: slideUp 0.6s ease-out, tilt3D 6s ease-in-out infinite;
        transition: all 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55);
        transform-style: preserve-3d;
    }
    
    .info-box:hover {
        transform: perspective(1000px) translateZ(25px) rotateY(5deg) scale(1.05);
        animation: pop3D 0.5s ease-in-out, glow 2s ease-in-out infinite;
        box-shadow: 0 15px 30px rgba(102, 126, 234, 0.4);
    }
    
    /* Emoji animations */
    .emoji-large {
        display: inline-block;
        font-size: 50px;
        animation: bounce 1s ease-in-out infinite, rotate3D 10s linear infinite;
        transform-style: preserve-3d;
        transition: all 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55);
    }
    
    .emoji-large:hover {
        animation: flip3D 1s ease-in-out, pop3D 0.5s ease-in-out;
        transform: scale(1.3);
        filter: drop-shadow(0 0 20px rgba(255, 215, 0, 0.9));
    }
    
    .emoji-float {
        display: inline-block;
        animation: float 2s ease-in-out infinite, tilt3D 4s ease-in-out infinite;
        transform-style: preserve-3d;
    }
    
    .emoji-spin {
        display: inline-block;
        animation: rainbow 3s linear infinite, spin3D 8s linear infinite;
        transform-style: preserve-3d;
    }
    
    /* Progress bar style */
    .stProgress > div > div {
        background: linear-gradient(90deg, #43e97b, #38f9d7, #667eea, #764ba2);
        background-size: 200% 200%;
        animation: rainbow 2s linear infinite;
    }
    
    /* Form container */
    [data-testid="stForm"] {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 1.5rem;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
        animation: slideUp 0.7s ease-out;
    }
    
    /* Hide streamlit branding with style */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 12px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea, #764ba2);
        border-radius: 10px;
        transition: all 0.3s ease;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #f093fb, #f5576c);
        box-shadow: 0 0 10px rgba(255, 255, 255, 0.5);
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
if 'assistant' not in st.session_state:
    st.session_state.assistant = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'initialized' not in st.session_state:
    st.session_state.initialized = False
if 'reaction_counts' not in st.session_state:
    st.session_state.reaction_counts = {}
if 'fun_responses' not in st.session_state:
    st.session_state.fun_responses = [
        "🚀 Let me dive into the DSA universe for you!",
        "🧠 Brain power activating... Beep boop!",
        "🔍 Searching through my magical DSA notes...",
        "💡 Time to sprinkle some knowledge magic!",
        "🎯 Lock and loaded! Finding your answer...",
        "🌟 Consulting the DSA wisdom scrolls...",
        "🎪 Let's make some coding magic happen!",
        "🦾 Flexing my algorithm muscles...",
        "🎨 Painting you a picture of understanding...",
        "🏃 Racing through data structures for you!"
    ]

def initialize_assistant():
    """Initialize the DSA assistant"""
    try:
        load_dotenv()
        with st.spinner("🔄 Initializing DSA Assistant... This may take a moment on first run."):
            st.session_state.assistant = DSAAssistant()
            st.session_state.initialized = True
        st.success("✅ Assistant ready!")
        return True
    except Exception as e:
        st.error(f"❌ Error initializing assistant: {str(e)}")
        st.error("Please ensure all dependencies are installed: pip install -r requirements.txt")
        st.exception(e)  # Show full traceback
        return False

def get_answer(question):
    """Get answer from the assistant"""
    try:
        rag_chain, retriever = st.session_state.assistant.qa_chain
        answer = rag_chain.invoke(question)
        source_docs = retriever.invoke(question)  # Updated method
        return answer, source_docs
    except Exception as e:
        st.error(f"Error getting answer: {str(e)}")
        st.exception(e)  # Show full traceback
        return f"❌ Error: {str(e)}", []

def display_message(role, content):
    """Display a chat message with fun reactions"""
    import html
    import random
    # Properly escape and format content
    content = html.escape(str(content))
    # Replace newlines with proper line breaks
    content = content.replace('\n', '<br>')
    
    # Fun reaction emojis
    reactions = ['💯', '🔥', '⭐', '🎉', '👍', '💪', '🚀', '❤️']
    random_reactions = random.sample(reactions, 4)
    reaction_html = ''.join([f'<span class="message-reaction" title="React!">{emoji}</span>' for emoji in random_reactions])
    
    if role == "user":
        st.markdown(f"""
<div class="chat-message user-message">
<div class="message-header">
<span style="font-size: 24px;">👤</span>
<span>You</span>
</div>
<div class="message-content">{content}</div>
<div style="margin-top: 1rem; text-align: right;">
{reaction_html}
</div>
</div>
""", unsafe_allow_html=True)
    else:
        st.markdown(f"""
<div class="chat-message assistant-message">
<div class="message-header">
<span style="font-size: 24px;">🎓</span>
<span>DSA Assistant</span>
</div>
<div class="message-content">{content}</div>
<div style="margin-top: 1rem; text-align: right;">
{reaction_html}
</div>
</div>
""", unsafe_allow_html=True)

def show_typing_indicator():
    """Display a fun typing indicator"""
    import random
    fun_messages = [
        "🤔 Hmm, let me think about that...",
        "🔍 Searching through DSA notes...",
        "🧠 Processing your question...",
        "💭 Thinking deeply...",
        "🎯 Finding the perfect answer...",
        "✨ Magic in progress...",
        "🚀 Launching answer generator...",
        "🎪 Working my algorithm magic..."
    ]
    st.markdown(f"""
<div class="typing-indicator">
<span style="font-size: 18px; margin-right: 10px;">{random.choice(fun_messages)}</span>
<div class="typing-dot"></div>
<div class="typing-dot"></div>
<div class="typing-dot"></div>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("""
<div style='text-align: center; padding: 1.5rem; background: rgba(255,255,255,0.15); border-radius: 15px; margin-bottom: 1.5rem; animation: slideUp 0.6s ease-out, glow 3s ease-in-out infinite;'>
<h1 style='margin: 0; font-size: 40px;'><span class='emoji-large'>🎓</span></h1>
<h2 style='margin: 10px 0 0 0; font-size: 24px;'>DSA Assistant</h2>
<p style='margin: 5px 0 0 0; font-size: 14px; opacity: 0.9;'><span class='emoji-float'>✨</span> Powered by AI <span class='emoji-float'>✨</span></p>
</div>
""", unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("""
<div class='info-box'>
<h3 style='margin-top: 0; color: #FFD700;'><span class='emoji-float'>📚</span> About</h3>
<p style='color: white;'>Welcome to your personal DSA tutor! Ask me anything about:</p>
<ul style='color: white; line-height: 2; list-style: none; padding-left: 0;'>
<li><span class='emoji-float'>📊</span> Arrays & Linked Lists</li>
<li><span class='emoji-float'>📚</span> Stacks & Queues</li>
<li><span class='emoji-float'>🔍</span> Sorting & Searching</li>
<li><span class='emoji-float'>📈</span> Big O Notation</li>
<li><span class='emoji-float'>🔄</span> Recursion</li>
<li><span class='emoji-float'>🌲</span> Trees & BST</li>
</ul>
</div>
""", unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("""
<div class='info-box'>
<h3 style='margin-top: 0; color: #FFD700;'><span class='emoji-large'>💡</span> Quick Topics</h3>
<p style='color: white; font-size: 15px;'>Click any button below to start learning! <span class='emoji-float'>👇</span></p>
</div>
""", unsafe_allow_html=True)
    
    example_topics = {
        "📊 Arrays": "What is an array and how does it work?",
        "🔗 Linked Lists": "How do I reverse a linked list?",
        "📚 Stacks": "What is a stack and when should I use it?",
        "🚶 Queues": "What's the difference between stack and queue?",
        "🔍 Binary Search": "Explain binary search in simple terms",
        "📈 Big O": "What is Big O notation?",
        "🔄 Recursion": "What is recursion and how does it work?",
        "🌲 Trees": "What is a binary search tree?",
        "🔢 Bubble Sort": "How does bubble sort work?",
        "⚡ Merge Sort": "Explain merge sort step by step",
    }
    
    for topic, question in example_topics.items():
        if st.button(topic, key=topic, use_container_width=True):
            if st.session_state.initialized:
                # Add user message
                st.session_state.chat_history.append(("user", question))
                
                # Show typing indicator
                typing_placeholder = st.empty()
                with typing_placeholder:
                    show_typing_indicator()
                
                # Get assistant response
                answer, sources = get_answer(question)
                typing_placeholder.empty()
                
                # Add assistant message
                st.session_state.chat_history.append(("assistant", answer))
                
                # Rerun to update chat
                st.rerun()
            else:
                st.warning("Please wait for assistant to initialize first!")
    
    st.markdown("---")
    
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()
    
    st.markdown("---")
    st.markdown("""
<div class='info-box'>
<h3 style='margin-top: 0; color: #FFD700;'><span class='emoji-spin'>ℹ️</span> How it works</h3>
<ol style='color: white; line-height: 2.2; font-size: 15px;'>
<li><span class='emoji-float'>✍️</span> Type your DSA question</li>
<li><span class='emoji-float'>🔍</span> AI searches through notes</li>
<li><span class='emoji-float'>💡</span> Get simple explanations</li>
<li><span class='emoji-float'>🎯</span> Learn at your own pace!</li>
</ol>
</div>
""", unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("""
<div class='info-box' style='text-align: center;'>
<p style='color: white; margin: 10px 0; font-size: 16px;'><strong><span class='emoji-large'>⚡</span> Powered by:</strong></p>
<p style='color: #FFD700; margin: 8px 0; font-size: 15px;'><span class='emoji-float'>🚀</span> Groq AI</p>
<p style='color: #FFD700; margin: 8px 0; font-size: 15px;'><span class='emoji-float'>🧠</span> RAG Technology</p>
<p style='color: #FFD700; margin: 8px 0; font-size: 15px;'><span class='emoji-float'>✨</span> Streamlit Magic</p>
</div>
""", unsafe_allow_html=True)

# Main content
st.markdown("""
<div style='text-align: center; padding: 3rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 30px; margin-bottom: 2rem; box-shadow: 0 15px 30px rgba(0,0,0,0.4); animation: slideUp 0.8s ease-out, tilt3D 4s ease-in-out infinite; transform-style: preserve-3d; position: relative; overflow: hidden; transition: all 0.5s ease;' onmouseover='this.style.transform=\"perspective(1000px) translateZ(40px) scale(1.05)\"' onmouseout='this.style.transform=\"\"'>
<h1 style='margin: 0; font-size: 58px; text-shadow: 3px 3px 6px rgba(0,0,0,0.3);'><span class='emoji-large'>🎓</span> DSA Learning Assistant <span class='emoji-large'>✨</span></h1>
<p style='margin: 20px 0 0 0; font-size: 24px; color: white; opacity: 0.98;'><span class='emoji-float'>🚀</span> Your Personal 3D Animated Data Structures & Algorithms Tutor! <span class='emoji-float'>🎯</span></p>
<div style='margin-top: 15px;'>
<span style='font-size: 30px; animation: confetti 2s ease-in-out infinite;'>🎉</span>
<span style='font-size: 30px; animation: confetti 2s ease-in-out infinite 0.3s;'>🎊</span>
<span style='font-size: 30px; animation: confetti 2s ease-in-out infinite 0.6s;'>✨</span>
<span style='font-size: 30px; animation: confetti 2s ease-in-out infinite 0.9s;'>🌟</span>
<span style='font-size: 30px; animation: confetti 2s ease-in-out infinite 1.2s;'>💫</span>
</div>
</div>
""", unsafe_allow_html=True)

# Initialize assistant if not done
if not st.session_state.initialized:
    st.info("👋 Welcome! Initializing your DSA assistant...")
    if initialize_assistant():
        st.success("✅ Assistant ready! Ask me anything about DSA concepts.")
        st.balloons()
    else:
        st.stop()
else:
    # Assistant is already initialized, just show a brief status
    pass

# Chat interface
st.markdown("---")

# Display chat history
chat_container = st.container()
with chat_container:
    if not st.session_state.chat_history:
        st.markdown("""
<div class='welcome-box' style='background: linear-gradient(135deg, rgba(102, 126, 234, 0.4), rgba(245, 87, 108, 0.4)); position: relative;'>
<div style='position: absolute; top: 15px; right: 15px; font-size: 40px; animation: spin3D 5s linear infinite;'>🌟</div>
<div style='position: absolute; top: 15px; left: 15px; font-size: 40px; animation: flip3D 6s linear infinite;'>🎨</div>
<div style='position: absolute; bottom: 15px; right: 15px; font-size: 40px; animation: rotate3D 4s linear infinite;'>🎯</div>
<div style='position: absolute; bottom: 15px; left: 15px; font-size: 40px; animation: wave 1s ease-in-out infinite;'>👋</div>
<h2 style='font-size: 70px; margin-bottom: 25px;'>
<span class='emoji-large' style='animation: pop3D 2s ease-in-out infinite;'>👋</span> 
<span class='emoji-large' style='animation: pop3D 2s ease-in-out infinite 0.3s;'>🎓</span>
<span class='emoji-large' style='animation: pop3D 2s ease-in-out infinite 0.6s;'>💻</span>
</h2>
<h2 style='margin-bottom: 25px; animation: tilt3D 3s ease-in-out infinite; text-shadow: 2px 2px 4px rgba(0,0,0,0.3); font-size: 28px;'>
🎪 Welcome to the DSA Fun Zone! 🎪
</h2>
<p style='font-size: 24px; margin-bottom: 20px; animation: rainbow 5s linear infinite;'>
<span class='emoji-float'>✨</span> I'm your super-fun 3D animated learning buddy! <span class='emoji-float'>✨</span>
</p>
<p style='font-size: 20px; margin-top: 30px; opacity: 0.95; animation: float 3s ease-in-out infinite;'>
<span class='emoji-large' style='animation: wave 1s ease-in-out infinite;'>👇</span> Pick a topic or type your question below! <span class='emoji-large' style='animation: wave 1s ease-in-out infinite;'>👇</span>
</p>
<div style='margin-top: 30px; font-size: 35px;'>
<span style='animation: bounce 1s ease-in-out infinite;'>🚀</span>
<span style='animation: bounce 1s ease-in-out infinite 0.2s;'>💡</span>
<span style='animation: bounce 1s ease-in-out infinite 0.4s;'>🎯</span>
<span style='animation: bounce 1s ease-in-out infinite 0.6s;'>🌈</span>
<span style='animation: bounce 1s ease-in-out infinite 0.8s;'>⭐</span>
</div>
<p style='font-size: 18px; margin-top: 25px; opacity: 0.9;'>
<strong>Pro Tip:</strong> Hover over anything for cool 3D effects! 🎨
</p>
</div>
""", unsafe_allow_html=True)
    else:
        for role, message in st.session_state.chat_history:
            display_message(role, message)

# Input area
st.markdown("""
<div style='padding: 1.5rem; background: linear-gradient(135deg, rgba(139, 92, 246, 0.2), rgba(236, 72, 153, 0.2)); border-radius: 20px; margin: 2rem 0; border: 2px solid rgba(236, 72, 153, 0.4); animation: glow 3s ease-in-out infinite; box-shadow: 0 8px 16px rgba(236, 72, 153, 0.3);'>
<h3 style='margin: 0 0 1rem 0; text-align: center; animation: rainbow 8s linear infinite; font-size: 26px;'><span class='emoji-large'>💬</span> Ask Me Anything About DSA! <span class='emoji-large'>💬</span></h3>
</div>
""", unsafe_allow_html=True)
st.markdown("---")

# Use a form to properly handle submission
with st.form(key="question_form", clear_on_submit=True):
    user_input = st.text_input(
        "Ask your question:",
        placeholder="e.g., What is the time complexity of bubble sort?",
        label_visibility="collapsed"
    )
    submit_button = st.form_submit_button("Ask 💬", use_container_width=True, type="primary")

# Handle question submission
if submit_button and user_input and user_input.strip():
    if st.session_state.initialized:
        # Add user message
        st.session_state.chat_history.append(("user", user_input))
        
        # Show typing indicator
        typing_placeholder = st.empty()
        with typing_placeholder:
            show_typing_indicator()
        
        # Get assistant response
        answer, sources = get_answer(user_input)
        typing_placeholder.empty()
        
        # Add assistant message
        st.session_state.chat_history.append(("assistant", answer))
        
        # Rerun to update chat
        st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 2.5rem; background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); border-radius: 25px; color: white; box-shadow: 0 12px 24px rgba(0,0,0,0.3); animation: slideUp 0.8s ease-out, tilt3D 5s ease-in-out infinite; transform-style: preserve-3d; position: relative;' onmouseover='this.style.transform=\"perspective(1000px) translateZ(30px) rotateY(3deg)\"' onmouseout='this.style.transform=\"\"'>
<div style='font-size: 50px; animation: rotate3D 8s linear infinite;'>💝</div>
<p style='margin: 15px 0; font-size: 22px; animation: rainbow 6s linear infinite;'>
<span class='emoji-large' style='animation: pop3D 2s ease-in-out infinite;'>💡</span> 
<strong>Fun Fact:</strong> I explain everything in simple terms!
</p>
<p style='margin: 15px 0; font-size: 19px; opacity: 0.95; animation: float 3s ease-in-out infinite;'>
If something isn't in my notes, I'll be honest with you! 
<span class='emoji-float' style='animation: wave 1s ease-in-out infinite;'>😊</span>
</p>
<div style='margin: 20px 0; font-size: 35px;'>
<span style='animation: bounce 1.5s ease-in-out infinite;'>🎨</span>
<span style='animation: bounce 1.5s ease-in-out infinite 0.2s;'>🎪</span>
<span style='animation: bounce 1.5s ease-in-out infinite 0.4s;'>🎯</span>
<span style='animation: bounce 1.5s ease-in-out infinite 0.6s;'>🚀</span>
<span style='animation: bounce 1.5s ease-in-out infinite 0.8s;'>🌟</span>
</div>
<p style='margin: 20px 0 0 0; font-size: 24px; font-weight: bold; animation: rainbow 8s linear infinite;'>
<span class='emoji-large'>🌈</span> Keep Learning & Have Fun! <span class='emoji-large'>✨</span>
</p>
<p style='margin: 10px 0 0 0; font-size: 16px; opacity: 0.9;'>
Made with <span style='animation: pulse 1s ease-in-out infinite; color: #ff6b6b;'>❤️</span> and lots of 3D magic!
</p>
</div>
""", unsafe_allow_html=True)
