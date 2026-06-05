"""
Pywiki AI Personal Assistant — Streamlit Edition

Setup & run (requires uv — https://docs.astral.sh/uv/):
    uv sync
    uv run streamlit run main.py
"""

import streamlit as st
import datetime
import time
import webbrowser
import requests

# ── Optional imports (graceful degradation) ──────────────────────────────────
try:
    import pyttsx3
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False

try:
    import speech_recognition as sr
    STT_AVAILABLE = True
except ImportError:
    STT_AVAILABLE = False

try:
    import wikipedia
    WIKI_AVAILABLE = True
except ImportError:
    WIKI_AVAILABLE = False

try:
    import wolframalpha
    WOLFRAM_AVAILABLE = True
except ImportError:
    WOLFRAM_AVAILABLE = False

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Pywiki — AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=Space+Mono:wght@400;700&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background: #0d0f14;
    color: #e8eaf0;
}

[data-testid="stSidebar"] {
    background: #13161e !important;
    border-right: 1px solid #1e2230;
}
[data-testid="stSidebar"] .stMarkdown h1,
[data-testid="stSidebar"] .stMarkdown h2,
[data-testid="stSidebar"] .stMarkdown h3 {
    color: #e8eaf0;
}

.brand-header {
    font-family: 'Space Mono', monospace;
    font-size: 1.6rem;
    font-weight: 700;
    letter-spacing: -0.03em;
    background: linear-gradient(135deg, #6c8ef5 0%, #a78bfa 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.2rem;
}
.brand-sub {
    font-size: 0.75rem;
    color: #5a6080;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    font-weight: 500;
}

.chat-container {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    padding: 1rem 0;
}
.msg-user {
    align-self: flex-end;
    background: #1e2547;
    border: 1px solid #2a3260;
    color: #c5cefc;
    border-radius: 18px 18px 4px 18px;
    padding: 0.75rem 1.1rem;
    max-width: 70%;
    font-size: 0.92rem;
    line-height: 1.6;
}
.msg-pywiki {
    align-self: flex-start;
    background: #161921;
    border: 1px solid #1e2230;
    color: #c8cdd8;
    border-radius: 4px 18px 18px 18px;
    padding: 0.75rem 1.1rem;
    max-width: 72%;
    font-size: 0.92rem;
    line-height: 1.6;
}
.msg-label {
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 0.3rem;
    opacity: 0.5;
}
.msg-user .msg-label  { color: #6c8ef5; }
.msg-pywiki .msg-label { color: #a78bfa; }

.metric-tile {
    background: #161921;
    border: 1px solid #1e2230;
    border-radius: 12px;
    padding: 1rem 1.25rem;
    text-align: center;
}
.metric-tile .val {
    font-family: 'Space Mono', monospace;
    font-size: 1.4rem;
    font-weight: 700;
    color: #a78bfa;
}
.metric-tile .lbl {
    font-size: 0.72rem;
    color: #5a6080;
    text-transform: uppercase;
    letter-spacing: 0.09em;
    margin-top: 0.2rem;
}

.badge {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 99px;
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.06em;
}
.badge-on  { background: #0d2e1a; color: #4ade80; border: 1px solid #166534; }
.badge-off { background: #2b1111; color: #f87171; border: 1px solid #7f1d1d; }

.stTextInput input {
    background: #161921 !important;
    border: 1px solid #1e2230 !important;
    border-radius: 10px !important;
    color: #e8eaf0 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.93rem !important;
    padding: 0.65rem 1rem !important;
}
.stTextInput input:focus {
    border-color: #6c8ef5 !important;
    box-shadow: 0 0 0 2px rgba(108,142,245,0.15) !important;
}

.stButton > button {
    background: #1a1f30 !important;
    border: 1px solid #2a3260 !important;
    color: #6c8ef5 !important;
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    font-size: 0.88rem !important;
    transition: all 0.18s ease !important;
}
.stButton > button:hover {
    background: #20284a !important;
    border-color: #6c8ef5 !important;
    color: #a5b8ff !important;
}

.stSelectbox div[data-baseweb="select"] > div {
    background: #161921 !important;
    border-color: #1e2230 !important;
    color: #e8eaf0 !important;
}
.stTextArea textarea {
    background: #161921 !important;
    border-color: #1e2230 !important;
    color: #e8eaf0 !important;
    font-family: 'DM Sans', sans-serif !important;
}

.section-title {
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #3a4060;
    margin: 1.5rem 0 0.6rem;
}

#MainMenu { visibility: hidden; }
footer    { visibility: hidden; }
header    { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# ── Session state ─────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "query_count" not in st.session_state:
    st.session_state.query_count = 0


# ── Helpers ───────────────────────────────────────────────────────────────────

def speak(text: str) -> None:
    """TTS — no-op if pyttsx3 unavailable."""
    if TTS_AVAILABLE and st.session_state.get("tts_enabled", False):
        try:
            engine = pyttsx3.init()
            engine.say(text)
            engine.runAndWait()
        except Exception:
            pass


def add_message(role: str, content: str) -> None:
    st.session_state.messages.append({"role": role, "content": content, "ts": datetime.datetime.now()})
    st.session_state.query_count += 1
    speak(content)


def get_greeting() -> str:
    hour = datetime.datetime.now().hour
    if hour < 12:
        return "Good morning"
    elif hour < 18:
        return "Good afternoon"
    return "Good evening"


def get_weather(city: str, api_key: str) -> str:
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    try:
        resp = requests.get(base_url, params={"q": city, "appid": api_key}, timeout=8)
        data = resp.json()
        if data.get("cod") == 200:
            main   = data["main"]
            desc   = data["weather"][0]["description"].capitalize()
            temp_c = round(main["temp"] - 273.15, 1)
            humid  = main["humidity"]
            return (f"**{city.title()}** — {desc}\n\n"
                    f"🌡 Temperature: **{temp_c} °C**\n\n"
                    f"💧 Humidity: **{humid}%**")
        return f"City **{city}** not found. Please check the spelling."
    except Exception as e:
        return f"Weather service error: {e}"


def process_command(cmd: str, weather_api_key: str = "") -> str:
    """Route a command string to the appropriate handler."""
    cmd_l = cmd.lower().strip()

    # ── Greetings ──
    if any(w in cmd_l for w in ["hello", "hi ", "hey", "good morning", "good afternoon", "good evening"]):
        return f"{get_greeting()}! How can I help you today?"

    # ── Identity ──
    if any(p in cmd_l for p in ["who are you", "what can you do", "your name"]):
        return (
            "I'm **Pywiki**, your AI personal assistant.\n\n"
            "I can help you with:\n"
            "- 🔍 Wikipedia searches\n"
            "- 🌤 Weather forecasts\n"
            "- 🧮 Computational & geographical questions\n"
            "- 🌐 Opening websites (YouTube, Google, Gmail, StackOverflow)\n"
            "- 🕐 Current time & date\n"
            "- 📰 News headlines"
        )

    if any(p in cmd_l for p in ["who made you", "who created you", "who built you"]):
        return "I was built by **Tesimune**. 🛠️"

    # ── Time / Date ──
    if "time" in cmd_l and "weather" not in cmd_l:
        now = datetime.datetime.now()
        return f"🕐 Current time: **{now.strftime('%H:%M:%S')}**"

    if "date" in cmd_l:
        now = datetime.datetime.now()
        return f"📅 Today is **{now.strftime('%A, %d %B %Y')}**"

    # ── Wikipedia ──
    if "wikipedia" in cmd_l or cmd_l.startswith("wiki "):
        if not WIKI_AVAILABLE:
            return "Wikipedia module not installed. Run `uv add wikipedia`."
        query = cmd_l.replace("wikipedia", "").replace("wiki", "").strip()
        if not query:
            return "Please specify a topic to search Wikipedia."
        try:
            result = wikipedia.summary(query, sentences=4)
            return f"📖 **Wikipedia — {query.title()}**\n\n{result}"
        except wikipedia.exceptions.DisambiguationError as e:
            opts = ", ".join(e.options[:5])
            return f"Ambiguous query. Did you mean: {opts}?"
        except Exception as ex:
            return f"Wikipedia error: {ex}"

    # ── Weather ──
    if "weather" in cmd_l:
        for prep in ["weather in ", "weather for ", "weather at ", "weather "]:
            if prep in cmd_l:
                city = cmd_l.split(prep, 1)[1].strip()
                if city:
                    if not weather_api_key:
                        return "⚠️ Add your OpenWeatherMap API key in the sidebar to use this feature."
                    return get_weather(city, weather_api_key)
        return "Please specify a city, e.g. *weather in Lagos*."

    # ── Wolfram Alpha ──
    if cmd_l.startswith("ask ") or cmd_l.startswith("calculate ") or cmd_l.startswith("compute "):
        if not WOLFRAM_AVAILABLE:
            return "Wolfram Alpha module not installed. Run `uv add wolframalpha`."
        app_id = st.session_state.get("wolfram_key", "")
        if not app_id:
            return "⚠️ Add your Wolfram Alpha App ID in the sidebar."
        question = cmd_l.replace("ask", "").replace("calculate", "").replace("compute", "").strip()
        try:
            client = wolframalpha.Client(app_id)
            res    = client.query(question)
            answer = next(res.results).text
            return f"🧮 **{question.capitalize()}**\n\n{answer}"
        except Exception as ex:
            return f"Wolfram Alpha error: {ex}"

    # ── Open websites ──
    site_map = {
        "youtube":       ("https://www.youtube.com",   "▶️ Opening YouTube…"),
        "google":        ("https://www.google.com",    "🔍 Opening Google…"),
        "gmail":         ("https://mail.google.com",   "📧 Opening Gmail…"),
        "stackoverflow": ("https://stackoverflow.com", "💻 Opening Stack Overflow…"),
        "github":        ("https://www.github.com",    "🐙 Opening GitHub…"),
        "news":          ("https://timesofindia.indiatimes.com/home/headlines",
                          "📰 Opening Times of India headlines…"),
    }
    for key, (url, msg) in site_map.items():
        if f"open {key}" in cmd_l or (key == "news" and "news" in cmd_l):
            webbrowser.open_new_tab(url)
            return msg

    # ── Generic search ──
    if cmd_l.startswith("search "):
        query = cmd.split("search ", 1)[1].strip()
        url   = f"https://www.google.com/search?q={requests.utils.quote(query)}"
        webbrowser.open_new_tab(url)
        return f"🔍 Searching Google for **{query}**…"

    # ── Goodbye ──
    if any(w in cmd_l for w in ["bye", "goodbye", "stop", "shut down", "exit"]):
        return "Goodbye! 👋 It was a pleasure assisting you."

    # ── Fallback ──
    return (
        "I'm not sure how to handle that yet. Try:\n"
        "- `wikipedia <topic>` — search Wikipedia\n"
        "- `weather in <city>` — current weather\n"
        "- `ask <question>` — computational answers\n"
        "- `open youtube` / `open google` / `open gmail`\n"
        "- `time` or `date`"
    )


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="brand-header">PYWIKI</div>', unsafe_allow_html=True)
    st.markdown('<div class="brand-sub">AI Personal Assistant v2.0</div>', unsafe_allow_html=True)
    st.markdown("---")

    st.markdown('<div class="section-title">Module Status</div>', unsafe_allow_html=True)
    for label, available in [
        ("Speech Recognition", STT_AVAILABLE),
        ("Text-to-Speech",     TTS_AVAILABLE),
        ("Wikipedia",          WIKI_AVAILABLE),
        ("Wolfram Alpha",      WOLFRAM_AVAILABLE),
    ]:
        badge = "badge-on" if available else "badge-off"
        txt   = "Active" if available else "Inactive"
        st.markdown(
            f'<div style="display:flex;justify-content:space-between;align-items:center;'
            f'margin-bottom:6px;font-size:0.82rem;color:#8890a8;">'
            f'{label} <span class="badge {badge}">{txt}</span></div>',
            unsafe_allow_html=True,
        )

    st.markdown('<div class="section-title">Settings</div>', unsafe_allow_html=True)
    tts_on = st.toggle("Enable voice output (TTS)", value=True, disabled=not TTS_AVAILABLE)
    st.session_state["tts_enabled"] = tts_on

    st.markdown('<div class="section-title">API Keys</div>', unsafe_allow_html=True)
    weather_key = st.text_input("OpenWeatherMap key", type="password",
                                placeholder="Paste API key…",
                                help="Free key at openweathermap.org")
    wolfram_key = st.text_input("Wolfram Alpha App ID", type="password",
                                placeholder="Paste App ID…",
                                help="Free ID at wolframalpha.com/developers")
    st.session_state["wolfram_key"] = wolfram_key

    st.markdown("---")
    if st.button("🗑️  Clear conversation"):
        st.session_state.messages = []
        st.session_state.query_count = 0
        st.rerun()

    st.markdown('<div class="section-title">Quick Commands</div>', unsafe_allow_html=True)
    for c in ["wikipedia Python", "weather in Lagos", "open youtube",
              "open github", "ask what is pi", "time", "date", "news"]:
        st.markdown(
            f'<div style="font-family:\'Space Mono\',monospace;font-size:0.7rem;'
            f'color:#4a5280;padding:2px 0;">{c}</div>',
            unsafe_allow_html=True,
        )

# ── Main area ─────────────────────────────────────────────────────────────────
col_title, col_metrics = st.columns([3, 2])

with col_title:
    now = datetime.datetime.now()
    st.markdown(
        f'<div style="padding:1.5rem 0 0.5rem;">'
        f'<span style="font-family:\'Space Mono\',monospace;font-size:0.7rem;'
        f'color:#3a4060;letter-spacing:0.12em;">PYWIKI ASSISTANT</span>'
        f'<h1 style="color:#e8eaf0;font-size:1.8rem;font-weight:600;'
        f'margin:0.3rem 0 0.2rem;letter-spacing:-0.03em;">Hello — {get_greeting()}</h1>'
        f'<p style="color:#5a6080;font-size:0.85rem;margin:0;">'
        f'{now.strftime("%A, %d %B %Y  ·  %H:%M")}</p>'
        f'</div>',
        unsafe_allow_html=True,
    )

with col_metrics:
    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown(
            f'<div class="metric-tile"><div class="val">'
            f'{len(st.session_state.messages)}</div>'
            f'<div class="lbl">Messages</div></div>',
            unsafe_allow_html=True,
        )
    with m2:
        active = sum([STT_AVAILABLE, TTS_AVAILABLE, WIKI_AVAILABLE, WOLFRAM_AVAILABLE])
        st.markdown(
            f'<div class="metric-tile"><div class="val">{active}/4</div>'
            f'<div class="lbl">Modules</div></div>',
            unsafe_allow_html=True,
        )
    with m3:
        st.markdown(
            f'<div class="metric-tile"><div class="val">'
            f'{st.session_state.query_count}</div>'
            f'<div class="lbl">Queries</div></div>',
            unsafe_allow_html=True,
        )

st.markdown("---")

# ── Chat history ──────────────────────────────────────────────────────────────
with st.container():
    if not st.session_state.messages:
        st.markdown(
            '<div style="text-align:center;padding:3rem 0;color:#2a3060;">'
            '<div style="font-size:2.5rem;margin-bottom:1rem;">🤖</div>'
            '<div style="font-family:\'Space Mono\',monospace;font-size:0.8rem;'
            'letter-spacing:0.12em;">TYPE A COMMAND BELOW TO BEGIN</div>'
            '</div>',
            unsafe_allow_html=True,
        )
    else:
        html_parts = ['<div class="chat-container">']
        for msg in st.session_state.messages:
            role    = msg["role"]
            content = msg["content"]
            ts      = msg["ts"].strftime("%H:%M")
            if role == "user":
                html_parts.append(
                    f'<div style="display:flex;flex-direction:column;align-items:flex-end;">'
                    f'<div class="msg-user"><div class="msg-label">You · {ts}</div>{content}</div>'
                    f'</div>'
                )
            else:
                html_parts.append(
                    f'<div style="display:flex;flex-direction:column;align-items:flex-start;">'
                    f'<div class="msg-pywiki"><div class="msg-label">Pywiki · {ts}</div>{content}</div>'
                    f'</div>'
                )
        html_parts.append("</div>")
        st.markdown("\n".join(html_parts), unsafe_allow_html=True)

st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

# ── Input row ─────────────────────────────────────────────────────────────────
col_input, col_send, col_mic = st.columns([6, 1, 1])

with col_input:
    user_input = st.text_input(
        label="command",
        label_visibility="collapsed",
        placeholder="Type a command, e.g. 'weather in Abuja' or 'wikipedia quantum computing'…",
        key="chat_input",
    )

with col_send:
    send_clicked = st.button("Send ↗", use_container_width=True)

with col_mic:
    mic_clicked = st.button("🎙 Mic", use_container_width=True, disabled=not STT_AVAILABLE)

# ── Voice input ───────────────────────────────────────────────────────────────
if mic_clicked and STT_AVAILABLE:
    with st.spinner("Listening… speak now"):
        try:
            r = sr.Recognizer()
            with sr.Microphone() as source:
                audio = r.listen(source, timeout=6)
            spoken = r.recognize_google(audio, language="en-ng")
            add_message("user", spoken)
            reply = process_command(spoken, weather_key)
            add_message("assistant", reply)
            st.rerun()
        except sr.WaitTimeoutError:
            st.warning("No speech detected. Please try again.")
        except sr.UnknownValueError:
            st.warning("Could not understand audio. Please speak clearly.")
        except Exception as e:
            st.error(f"Microphone error: {e}")

# ── Text submit ───────────────────────────────────────────────────────────────
if (send_clicked or (user_input and st.session_state.get("_last_input") != user_input)) and user_input.strip():
    st.session_state["_last_input"] = user_input
    add_message("user", user_input.strip())
    with st.spinner("Thinking…"):
        reply = process_command(user_input.strip(), weather_key)
    add_message("assistant", reply)
    st.rerun()

# ── Quick-action chips ────────────────────────────────────────────────────────
st.markdown("<div style='height:0.75rem'></div>", unsafe_allow_html=True)
st.markdown(
    '<div style="font-size:0.7rem;color:#3a4060;letter-spacing:0.1em;'
    'text-transform:uppercase;margin-bottom:0.5rem;">Try these</div>',
    unsafe_allow_html=True,
)
chip_cols = st.columns(5)
chips = ["time", "date", "open youtube", "wikipedia AI", "open github"]
for i, chip in enumerate(chips):
    with chip_cols[i]:
        if st.button(chip, key=f"chip_{i}", use_container_width=True):
            add_message("user", chip)
            reply = process_command(chip, weather_key)
            add_message("assistant", reply)
            st.rerun()

