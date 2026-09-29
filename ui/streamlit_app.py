import os
from datetime import datetime

import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

BACKEND_URL = os.getenv('BACKEND_URL', 'http://localhost:8000').rstrip('/')

st.set_page_config(page_title='Agentic Chatbot', layout='centered')

# ---------- Styling ----------
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

:root {
    --bg: #07080f;
    --glass: rgba(255, 255, 255, 0.055);
    --glass-2: rgba(255, 255, 255, 0.09);
    --border: rgba(255, 255, 255, 0.10);
    --text: #eef0f8;
    --muted: #9198b0;
    --a1: #8b5cf6;
    --a2: #38bdf8;
    --a3: #f472b6;
    --grad: linear-gradient(135deg, var(--a1), var(--a2));
}

html, body, [class*="css"], .stApp { font-family: 'Plus Jakarta Sans', sans-serif; }

/* Aurora background */
.stApp {
    background:
        radial-gradient(700px 450px at 12% 8%,  rgba(139, 92, 246, 0.28), transparent 65%),
        radial-gradient(650px 450px at 92% 18%, rgba(56, 189, 248, 0.20), transparent 65%),
        radial-gradient(700px 500px at 60% 105%, rgba(244, 114, 182, 0.16), transparent 65%),
        var(--bg);
    background-attachment: fixed;
    color: var(--text);
}

header[data-testid="stHeader"],
[data-testid="stBottom"],
[data-testid="stBottom"] > div { background: transparent !important; }
.block-container { padding-top: 2.2rem; max-width: 780px; }

/* Top brand bar */
.brand { display: flex; align-items: center; gap: 12px; margin-bottom: 0.2rem; }
.logo {
    width: 40px; height: 40px; border-radius: 12px;
    background: var(--grad);
    display: grid; place-items: center;
    font-weight: 800; color: #fff; font-size: 1.1rem;
    box-shadow: 0 6px 24px rgba(139, 92, 246, 0.55);
}
.brand h1 {
    margin: 0; padding: 0; font-size: 1.25rem; font-weight: 700;
    letter-spacing: -0.01em; color: var(--text);
}
.brand small { color: var(--muted); font-size: 0.75rem; display: block; margin-top: 2px; }

/* Hero */
.hero { padding: 3.2rem 0 1.6rem; }
.hero .hi {
    font-size: 2.9rem; line-height: 1.1; font-weight: 800; letter-spacing: -0.03em; margin: 0;
    background: linear-gradient(120deg, #fff 20%, #c4b5fd 55%, #7dd3fc 90%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.hero .sub { color: var(--muted); margin-top: 0.7rem; font-size: 1.02rem; }

/* Sidebar */
[data-testid="stSidebar"] {
    background: rgba(255, 255, 255, 0.04) !important;
    backdrop-filter: blur(28px) saturate(160%);
    -webkit-backdrop-filter: blur(28px) saturate(160%);
    border-right: 1px solid var(--border);
}
[data-testid="stSidebar"] h3 {
    font-size: 0.68rem !important; font-weight: 600 !important;
    text-transform: uppercase; letter-spacing: 0.14em; color: var(--muted);
}
[data-testid="stCode"], [data-testid="stSidebar"] pre {
    background: rgba(0, 0, 0, 0.35) !important;
    border: 1px solid var(--border); border-radius: 10px;
}
.pill {
    display: inline-flex; align-items: center; gap: 8px;
    padding: 5px 12px; border-radius: 999px; margin: 0.5rem 0 1.5rem;
    background: rgba(52, 211, 153, 0.10);
    border: 1px solid rgba(52, 211, 153, 0.30);
    font-size: 0.75rem; color: #6ee7b7;
}
.pill i {
    width: 7px; height: 7px; border-radius: 50%; background: #34d399;
    box-shadow: 0 0 0 0 rgba(52, 211, 153, 0.7); animation: pulse 2s infinite;
}
@keyframes pulse {
    0%   { box-shadow: 0 0 0 0 rgba(52, 211, 153, 0.6); }
    70%  { box-shadow: 0 0 0 8px rgba(52, 211, 153, 0); }
    100% { box-shadow: 0 0 0 0 rgba(52, 211, 153, 0); }
}
.tool {
    display: flex; align-items: center; gap: 12px;
    padding: 0.7rem 0.85rem; margin-bottom: 0.5rem;
    background: var(--glass); border: 1px solid var(--border); border-radius: 12px;
    font-size: 0.86rem; font-weight: 500;
}
.tool b {
    width: 30px; height: 30px; border-radius: 9px; display: grid; place-items: center;
    font-size: 0.8rem; color: #fff;
}
.tool span { display: block; color: var(--muted); font-size: 0.7rem; font-weight: 400; }

/* Chat bubbles */
[data-testid="stChatMessage"] {
    background: var(--glass);
    backdrop-filter: blur(16px) saturate(170%);
    -webkit-backdrop-filter: blur(16px) saturate(170%);
    border: 1px solid var(--border);
    border-radius: 18px 18px 18px 6px;
    padding: 0.95rem 1.2rem;
    margin-bottom: 0.9rem;
    max-width: 88%;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.25), inset 0 1px 0 rgba(255, 255, 255, 0.07);
    animation: rise 0.4s ease both;
}
@keyframes rise { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: none; } }

[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
    flex-direction: row-reverse;
    margin-left: auto;
    text-align: left;
    background: linear-gradient(135deg, rgba(139, 92, 246, 0.30), rgba(56, 189, 248, 0.16));
    border-color: rgba(139, 92, 246, 0.35);
    border-radius: 18px 18px 6px 18px;
}
[data-testid="stChatMessageAvatarUser"],
[data-testid="stChatMessageAvatarAssistant"] {
    background: var(--grad) !important; color: #fff !important; border-radius: 10px !important;
}
[data-testid="stChatMessageAvatarUser"] { background: linear-gradient(135deg, var(--a3), var(--a1)) !important; }
[data-testid="stChatMessage"] p, [data-testid="stChatMessage"] li {
    color: var(--text); font-size: 0.96rem; line-height: 1.7;
}

/* Input */
[data-testid="stChatInput"], [data-testid="stChatInput"] > div {
    background: rgba(255, 255, 255, 0.07) !important;
    border-radius: 18px !important;
}
[data-testid="stChatInput"] {
    border: 1px solid var(--border) !important;
    backdrop-filter: blur(24px); -webkit-backdrop-filter: blur(24px);
    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.4);
    transition: all 0.25s ease;
}
[data-testid="stChatInput"]:focus-within {
    border-color: rgba(139, 92, 246, 0.8) !important;
    box-shadow: 0 0 0 4px rgba(139, 92, 246, 0.18), 0 12px 40px rgba(0, 0, 0, 0.4);
}
[data-testid="stChatInput"] textarea { background: transparent !important; color: var(--text) !important; }
[data-testid="stChatInput"] textarea::placeholder { color: var(--muted); }
[data-testid="stChatInput"] button { background: var(--grad) !important; border-radius: 12px !important; }
[data-testid="stChatInput"] button svg { color: #fff !important; fill: #fff !important; }

/* Buttons / suggestion cards */
.stButton > button {
    background: var(--glass); color: var(--text);
    border: 1px solid var(--border); border-radius: 14px;
    font-size: 0.86rem; font-weight: 500; padding: 0.95rem 1rem; min-height: 4.2rem;
    backdrop-filter: blur(14px);
    transition: all 0.25s ease;
}
.stButton > button:hover {
    transform: translateY(-3px);
    background: var(--glass-2);
    border-color: rgba(139, 92, 246, 0.65);
    box-shadow: 0 12px 30px rgba(139, 92, 246, 0.25);
    color: #fff;
}
[data-testid="stSidebar"] .stButton > button { min-height: 2.6rem; padding: 0.5rem 1rem; }

/* Tool chips in chat */
.chip {
    display: inline-block; margin: 10px 6px 0 0; padding: 3px 11px;
    font-size: 0.72rem; font-weight: 500; color: #c4b5fd;
    background: rgba(139, 92, 246, 0.14); border: 1px solid rgba(139, 92, 246, 0.35);
    border-radius: 999px;
}

[data-testid="stAlert"] {
    background: rgba(244, 63, 94, 0.10); border: 1px solid rgba(244, 63, 94, 0.35);
    border-radius: 14px;
}
::-webkit-scrollbar { width: 8px; }
::-webkit-scrollbar-thumb { background: rgba(255, 255, 255, 0.14); border-radius: 8px; }
</style>
""",
    unsafe_allow_html=True,
)

# ---------- Header ----------
st.markdown(
    '<div class="brand"><div class="logo">A</div>'
    '<div><h1>Agentic Chatbot</h1>'
    '<small>Streamlit  ›  FastAPI  ›  LangGraph  ›  Tools</small></div></div>',
    unsafe_allow_html=True,
)

# ---------- Sidebar ----------
with st.sidebar:
    st.subheader('Backend')
    st.code(BACKEND_URL)
    st.markdown('<div class="pill"><i></i>Agent online</div>', unsafe_allow_html=True)

    st.subheader('Tools')
    st.markdown(
        '<div class="tool"><b style="background:linear-gradient(135deg,#8b5cf6,#6366f1)">∑</b>'
        '<div>Calculator<span>Solve expressions</span></div></div>'
        '<div class="tool"><b style="background:linear-gradient(135deg,#38bdf8,#0ea5e9)">◷</b>'
        '<div>Current time<span>Date and clock</span></div></div>'
        '<div class="tool"><b style="background:linear-gradient(135deg,#f472b6,#ec4899)">☁</b>'
        '<div>Weather<span>Live conditions</span></div></div>',
        unsafe_allow_html=True,
    )
    st.write('')
    if st.button('Clear conversation', use_container_width=True):
        st.session_state.messages = []
        st.rerun()

if 'messages' not in st.session_state:
    st.session_state.messages = []

# ---------- Empty state ----------
if not st.session_state.messages:
    hour = datetime.now().hour
    greeting = 'Good morning' if hour < 12 else 'Good afternoon' if hour < 17 else 'Good evening'
    st.markdown(
        f'<div class="hero"><p class="hi">{greeting}.<br>What shall we solve?</p>'
        '<p class="sub">Ask anything. The agent picks the right tool for you.</p></div>',
        unsafe_allow_html=True,
    )
    suggestions = [
        'What is 245 * 18 + 99?',
        'What time is it now?',
        'What is the weather in Indore?',
    ]
    cols = st.columns(len(suggestions))
    for col, text in zip(cols, suggestions):
        if col.button(text, key=text, use_container_width=True):
            st.session_state.pending = text
            st.rerun()


def render_tools(tools):
    if tools:
        st.markdown(
            ''.join(f'<span class="chip">{t}</span>' for t in tools),
            unsafe_allow_html=True,
        )


# ---------- History ----------
for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.markdown(message['content'])
        render_tools(message.get('tools'))

# ---------- Input ----------
prompt = st.chat_input('Message the agent...') or st.session_state.pop('pending', None)

if prompt:
    with st.chat_message('user'):
        st.markdown(prompt)

    history = [
        {'role': m['role'], 'content': m['content']}
        for m in st.session_state.messages
    ]
    st.session_state.messages.append({'role': 'user', 'content': prompt})

    with st.chat_message('assistant'):
        with st.spinner('Thinking...'):
            try:
                response = requests.post(
                    f'{BACKEND_URL}/chat',
                    json={'message': prompt, 'history': history},
                    timeout=120,
                )
                response.raise_for_status()
                data = response.json()
                answer = data['answer']
                tool_calls = data.get('tool_calls', [])

                st.markdown(answer)
                render_tools(tool_calls)

                st.session_state.messages.append(
                    {'role': 'assistant', 'content': answer, 'tools': tool_calls}
                )
            except requests.RequestException as exc:
                st.error(f'Backend connection failed: {exc}')
            except Exception as exc:
                st.error(f'Unexpected error: {exc}')