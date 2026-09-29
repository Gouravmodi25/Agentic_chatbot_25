import html
import json
import os
import time

import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

BACKEND_URL = os.getenv('BACKEND_URL', 'http://localhost:8000').rstrip('/')

TOOLS = {
    'calculator': '🧮',
    'current time': '🕒',
    'weather': '⛅',
}

SUGGESTIONS = [
    ('🧮', 'Calculate (245 * 18) + 99 / 3'),
    ('🕒', 'What time is it right now?'),
    ('⛅', "What's the weather in Indore?"),
    ('✨', 'Use two tools: weather in Delhi and the current time'),
]

st.set_page_config(
    page_title='Agentic Chatbot',
    page_icon='🤖',
    layout='centered',
)


# ---------- helpers ----------
def hex_to_rgb(value: str) -> str:
    value = value.lstrip('#')
    return ', '.join(str(int(value[i:i + 2], 16)) for i in (0, 2, 4))


def check_backend() -> bool:
    for path in ('/health', '/docs'):
        try:
            if requests.get(f'{BACKEND_URL}{path}', timeout=3).status_code == 200:
                return True
        except requests.RequestException:
            continue
    return False


def tool_pills(tool_calls) -> str:
    pills = ''.join(
        f'<span class="pill">🛠 {html.escape(str(t))}</span>' for t in tool_calls
    )
    return f'<div class="pill-row">{pills}</div>'


def render_message(message: dict) -> None:
    with st.chat_message(message['role']):
        st.markdown(message['content'])
        if message.get('tool_calls'):
            st.markdown(tool_pills(message['tool_calls']), unsafe_allow_html=True)


def typewriter(placeholder, text: str) -> None:
    words = text.split(' ')
    shown = ''
    for i, word in enumerate(words):
        shown += word + ' '
        if i % 2 == 0:
            placeholder.markdown(shown + '▌')
            time.sleep(0.02)
    placeholder.markdown(text)


# ---------- state ----------
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'backend_ok' not in st.session_state:
    st.session_state.backend_ok = None

# ---------- sidebar ----------
with st.sidebar:
    st.subheader('Control panel')

    accent = st.color_picker('Accent color', '#7c9cff')
    animate = st.toggle('Typing animation', value=True)
    show_tools = st.toggle('Show tools used', value=True)

    st.markdown('**Backend**')
    st.code(BACKEND_URL)

    if st.button('Test connection', use_container_width=True):
        with st.spinner('Pinging backend...'):
            st.session_state.backend_ok = check_backend()

    status = st.session_state.backend_ok
    if status is True:
        st.markdown('<span class="status ok">● Online</span>', unsafe_allow_html=True)
    elif status is False:
        st.markdown('<span class="status bad">● Unreachable</span>', unsafe_allow_html=True)

    st.markdown('**Available tools**')
    st.markdown(
        '<div class="pill-row">'
        + ''.join(f'<span class="pill">{icon} {name}</span>' for name, icon in TOOLS.items())
        + '</div>',
        unsafe_allow_html=True,
    )

    st.metric('Messages', len(st.session_state.messages))

    col_a, col_b = st.columns(2)
    with col_a:
        if st.button('Clear chat', use_container_width=True):
            st.session_state.messages = []
            st.rerun()
    with col_b:
        st.download_button(
            'Export',
            data=json.dumps(st.session_state.messages, indent=2, ensure_ascii=False),
            file_name='chat.json',
            mime='application/json',
            use_container_width=True,
            disabled=not st.session_state.messages,
        )

# ---------- glassmorphism theme ----------
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

:root {
    --accent: __ACCENT__;
    --accent-rgb: __ACCENT_RGB__;
    --glass: rgba(255, 255, 255, 0.08);
    --glass-strong: rgba(255, 255, 255, 0.14);
    --glass-border: rgba(255, 255, 255, 0.22);
    --text: #eef1ff;
    --muted: rgba(238, 241, 255, 0.65);
}

html, body, [class*="css"], .stApp {
    font-family: 'Plus Jakarta Sans', system-ui, sans-serif;
    color: var(--text);
}

/* Background: deep gradient + blurred colour orbs the glass can blur */
.stApp {
    background:
        radial-gradient(circle at 12% 18%, rgba(var(--accent-rgb), 0.55) 0, transparent 38%),
        radial-gradient(circle at 88% 12%, rgba(255, 105, 180, 0.35) 0, transparent 34%),
        radial-gradient(circle at 75% 88%, rgba(64, 224, 208, 0.32) 0, transparent 36%),
        radial-gradient(circle at 10% 90%, rgba(150, 90, 255, 0.35) 0, transparent 34%),
        linear-gradient(135deg, #0b1020 0%, #141a36 50%, #0d1226 100%);
    background-attachment: fixed;
}

header[data-testid="stHeader"] { background: transparent; }
[data-testid="stBottom"], [data-testid="stBottom"] > div { background: transparent; }
.block-container { padding-top: 2.2rem; padding-bottom: 6rem; }

/* Title */
h1 { font-weight: 700; letter-spacing: -0.02em; color: var(--text); }
[data-testid="stCaptionContainer"] p { color: var(--muted); }

/* Sidebar */
[data-testid="stSidebar"] {
    background: var(--glass);
    backdrop-filter: blur(24px) saturate(160%);
    -webkit-backdrop-filter: blur(24px) saturate(160%);
    border-right: 1px solid var(--glass-border);
}
[data-testid="stSidebar"] * { color: var(--text); }

/* Chat bubbles */
[data-testid="stChatMessage"] {
    background: var(--glass);
    backdrop-filter: blur(18px) saturate(150%);
    -webkit-backdrop-filter: blur(18px) saturate(150%);
    border: 1px solid var(--glass-border);
    border-radius: 20px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.9rem;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.28), inset 0 1px 0 rgba(255, 255, 255, 0.18);
}
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
    background: rgba(var(--accent-rgb), 0.18);
    border-color: rgba(var(--accent-rgb), 0.45);
}
[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] li { color: var(--text); line-height: 1.6; }
[data-testid="stChatMessage"] code {
    background: rgba(0, 0, 0, 0.35);
    border-radius: 6px;
}

/* Chat input */
[data-testid="stChatInput"] {
    background: var(--glass-strong);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid var(--glass-border);
    border-radius: 999px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
}
[data-testid="stChatInput"]:focus-within {
    border-color: rgba(var(--accent-rgb), 0.9);
    box-shadow: 0 0 0 3px rgba(var(--accent-rgb), 0.28), 0 8px 32px rgba(0, 0, 0, 0.3);
}
[data-testid="stChatInput"] textarea { color: var(--text); background: transparent; }
[data-testid="stChatInput"] textarea::placeholder { color: var(--muted); }
[data-testid="stChatInput"] button { background: var(--accent); color: #0b1020; border-radius: 999px; }

/* Buttons (sidebar + suggestion chips) */
.stButton > button, .stDownloadButton > button {
    background: var(--glass);
    color: var(--text);
    border: 1px solid var(--glass-border);
    border-radius: 14px;
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    transition: transform 0.15s ease, background 0.15s ease, border-color 0.15s ease;
}
.stButton > button:hover, .stDownloadButton > button:hover {
    background: rgba(var(--accent-rgb), 0.28);
    border-color: rgba(var(--accent-rgb), 0.8);
    color: #fff;
    transform: translateY(-2px);
}
.stButton > button:focus-visible, .stDownloadButton > button:focus-visible {
    outline: 2px solid var(--accent);
    outline-offset: 2px;
}
.stButton > button:active { transform: translateY(0); }

/* Hero card shown before the first message */
.hero {
    background: var(--glass);
    backdrop-filter: blur(22px) saturate(160%);
    -webkit-backdrop-filter: blur(22px) saturate(160%);
    border: 1px solid var(--glass-border);
    border-radius: 24px;
    padding: 1.6rem 1.8rem;
    margin: 0.5rem 0 1.2rem;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.2);
}
.hero h3 { margin: 0 0 0.3rem; font-weight: 700; }
.hero p { margin: 0; color: var(--muted); }

/* Tool pills + status */
.pill-row { display: flex; flex-wrap: wrap; gap: 0.4rem; margin-top: 0.5rem; }
.pill {
    background: rgba(var(--accent-rgb), 0.2);
    border: 1px solid rgba(var(--accent-rgb), 0.5);
    border-radius: 999px;
    padding: 0.18rem 0.7rem;
    font-size: 0.8rem;
    color: var(--text);
}
.status { font-size: 0.85rem; font-weight: 600; }
.status.ok { color: #6ee7a8; }
.status.bad { color: #ff8a8a; }

/* Alerts, code, metrics */
[data-testid="stAlert"] {
    background: rgba(255, 90, 90, 0.16);
    border: 1px solid rgba(255, 120, 120, 0.45);
    border-radius: 16px;
    backdrop-filter: blur(14px);
}
[data-testid="stSidebar"] pre, [data-testid="stCode"] {
    background: rgba(0, 0, 0, 0.3) !important;
    border-radius: 12px;
}
[data-testid="stMetric"] {
    background: var(--glass);
    border: 1px solid var(--glass-border);
    border-radius: 16px;
    padding: 0.6rem 0.9rem;
}

/* Scrollbar */
::-webkit-scrollbar { width: 8px; }
::-webkit-scrollbar-thumb { background: rgba(255, 255, 255, 0.25); border-radius: 8px; }

@media (prefers-reduced-motion: reduce) {
    * { transition: none !important; }
}
</style>
"""
st.markdown(
    CSS.replace('__ACCENT__', accent).replace('__ACCENT_RGB__', hex_to_rgb(accent)),
    unsafe_allow_html=True,
)

# ---------- header ----------
st.title('🤖 Agentic Chatbot')
st.caption('Streamlit UI → FastAPI → LangGraph Agent → Tools → Response')

# ---------- input (chat box or a clicked suggestion) ----------
typed = st.chat_input('Ask something...')
prompt = typed or st.session_state.pop('pending', None)

# ---------- empty state with clickable suggestions ----------
if not st.session_state.messages and not prompt:
    st.markdown(
        '<div class="hero"><h3>What can I help with?</h3>'
        '<p>Pick a starter below or type your own question. '
        'The agent decides which tools to use.</p></div>',
        unsafe_allow_html=True,
    )
    cols = st.columns(2)
    for i, (icon, text) in enumerate(SUGGESTIONS):
        with cols[i % 2]:
            if st.button(f'{icon}  {text}', key=f'sugg_{i}', use_container_width=True):
                st.session_state.pending = text
                st.rerun()

# ---------- history ----------
for message in st.session_state.messages:
    render_message(message)

# ---------- handle new prompt ----------
if prompt:
    with st.chat_message('user'):
        st.markdown(prompt)

    history = [
        {'role': m['role'], 'content': m['content']}
        for m in st.session_state.messages
    ]
    st.session_state.messages.append({'role': 'user', 'content': prompt})

    with st.chat_message('assistant'):
        try:
            with st.spinner('Agent is thinking...'):
                response = requests.post(
                    f'{BACKEND_URL}/chat',
                    json={'message': prompt, 'history': history},
                    timeout=120,
                )
                response.raise_for_status()
                data = response.json()

            answer = data['answer']
            tool_calls = data.get('tool_calls', [])

            if animate:
                typewriter(st.empty(), answer)
            else:
                st.markdown(answer)

            if tool_calls and show_tools:
                st.markdown(tool_pills(tool_calls), unsafe_allow_html=True)

            st.session_state.messages.append(
                {'role': 'assistant', 'content': answer, 'tool_calls': tool_calls}
            )
        except requests.RequestException as exc:
            st.error(f'Backend connection failed: {exc}')
        except Exception as exc:
            st.error(f'Unexpected error: {exc}')