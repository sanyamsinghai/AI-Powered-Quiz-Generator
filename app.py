import streamlit as st
import json
import re
import time
import logging
from datetime import datetime
from pathlib import Path

# ─── Logger Configuration ──────────────────────────────────────────────────────
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / f"quizcraft_{datetime.now().strftime('%Y%m%d')}.log"

# Create logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create handlers
file_handler = logging.FileHandler(LOG_FILE, mode='a', encoding='utf-8')
console_handler = logging.StreamHandler()

# Set levels
file_handler.setLevel(logging.DEBUG)
console_handler.setLevel(logging.INFO)

# Create formatter
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add handlers
logger.addHandler(file_handler)
logger.addHandler(console_handler)

logger.info("=" * 80)
logger.info("QuizCraft Application Started")
logger.info("=" * 80)

# ─── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="QuizCraft — AI Quiz Generator",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Figtree:wght@300;400;500;600;700;900&display=swap');

:root {
  --bg:        #0c0c0e;
  --bg2:       #111114;
  --bg3:       #18181d;
  --border:    #222228;
  --border2:   #2e2e38;
  --text:      #e2e2ea;
  --muted:     #55556a;
  --accent:    #f5a623;
  --accent2:   #f7c45e;
  --green:     #34d399;
  --red:       #f87171;
  --blue:      #60a5fa;
}

* { box-sizing: border-box; }

html, body, [class*="css"] {
  font-family: 'Figtree', sans-serif;
  background: var(--bg) !important;
  color: var(--text) !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
  background: var(--bg2) !important;
  border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] section { padding-top: 1.5rem !important; }
[data-testid="stSidebar"] * { color: var(--text) !important; }

/* ── Main padding ── */
.main .block-container { padding: 2rem 3rem 3rem !important; max-width: 1100px !important; }

/* ── All inputs ── */
input, textarea,
[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea {
  background: var(--bg3) !important;
  border: 1px solid var(--border2) !important;
  border-radius: 8px !important;
  color: var(--text) !important;
  font-family: 'Figtree', sans-serif !important;
  font-size: 0.95rem !important;
  transition: border-color 0.15s !important;
}
input:focus, textarea:focus {
  border-color: var(--accent) !important;
  box-shadow: 0 0 0 3px rgba(245,166,35,0.12) !important;
}

/* password icon color */
[data-testid="stTextInput"] svg { color: var(--muted) !important; }

/* ── Selectbox ── */
[data-testid="stSelectbox"] > div > div {
  background: var(--bg3) !important;
  border: 1px solid var(--border2) !important;
  border-radius: 8px !important;
  color: var(--text) !important;
}
[data-testid="stSelectbox"] svg { fill: var(--muted) !important; }

/* ── Dropdown list ── */
[data-baseweb="popover"] ul {
  background: var(--bg3) !important;
  border: 1px solid var(--border2) !important;
}
[data-baseweb="popover"] li { color: var(--text) !important; }
[data-baseweb="popover"] li:hover { background: var(--border) !important; }

/* ── Select slider ── */
[data-testid="stSelectSlider"] > div { background: var(--bg3) !important; border-radius: 8px !important; }
[data-testid="stSlider"] > div [data-baseweb="slider"] { background: var(--border2) !important; }

/* ── Primary button ── */
.stButton > button[kind="primary"],
.stButton > button {
  background: var(--accent) !important;
  color: #0c0c0e !important;
  border: none !important;
  border-radius: 8px !important;
  font-family: 'Figtree', sans-serif !important;
  font-weight: 700 !important;
  font-size: 0.95rem !important;
  letter-spacing: 0.02em !important;
  padding: 0.6rem 1.5rem !important;
  transition: all 0.2s ease !important;
  box-shadow: 0 2px 12px rgba(245,166,35,0.25) !important;
}
.stButton > button:hover {
  background: var(--accent2) !important;
  transform: translateY(-1px) !important;
  box-shadow: 0 6px 24px rgba(245,166,35,0.35) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* ── Form submit button ── */
[data-testid="stFormSubmitButton"] > button {
  background: var(--accent) !important;
  color: #0c0c0e !important;
  border: none !important;
  border-radius: 8px !important;
  font-family: 'Figtree', sans-serif !important;
  font-weight: 700 !important;
  font-size: 0.95rem !important;
  width: 100% !important;
  padding: 0.7rem 1.5rem !important;
  transition: all 0.2s !important;
  box-shadow: 0 2px 12px rgba(245,166,35,0.25) !important;
}
[data-testid="stFormSubmitButton"] > button:hover {
  background: var(--accent2) !important;
  transform: translateY(-1px) !important;
}

/* secondary buttons */
[data-testid="stFormSubmitButton"]:nth-child(2) > button,
.secondary-btn button {
  background: var(--bg3) !important;
  color: var(--text) !important;
  border: 1px solid var(--border2) !important;
  box-shadow: none !important;
}

/* ── Radio ── */
[data-testid="stRadio"] > div { gap: 0.5rem !important; }
[data-testid="stRadio"] label {
  background: var(--bg3) !important;
  border: 1px solid var(--border2) !important;
  border-radius: 8px !important;
  padding: 0.75rem 1rem !important;
  transition: all 0.15s !important;
  cursor: pointer !important;
  display: flex !important;
  align-items: center !important;
  gap: 0.5rem !important;
}
[data-testid="stRadio"] label:hover {
  border-color: var(--accent) !important;
  background: rgba(245,166,35,0.06) !important;
}

/* ── Progress bar ── */
[data-testid="stProgressBar"] > div {
  background: var(--border2) !important;
  border-radius: 99px !important;
}
[data-testid="stProgressBar"] > div > div {
  background: linear-gradient(90deg, var(--accent), var(--accent2)) !important;
  border-radius: 99px !important;
  transition: width 0.4s ease !important;
}

/* ── Divider ── */
hr { border-color: var(--border) !important; margin: 1.2rem 0 !important; }

/* ── Spinner ── */
[data-testid="stSpinner"] { color: var(--accent) !important; }

/* ── Alerts ── */
[data-testid="stAlert"] {
  border-radius: 8px !important;
  border: none !important;
  background: var(--bg3) !important;
}

/* ── Custom components ── */
.brand {
  font-family: 'Space Mono', monospace;
  font-size: 0.7rem;
  font-weight: 700;
  letter-spacing: 4px;
  color: var(--accent);
  text-transform: uppercase;
  margin-bottom: 0.4rem;
}

.hero-title {
  font-family: 'Figtree', sans-serif;
  font-size: 2.6rem;
  font-weight: 900;
  color: var(--text);
  line-height: 1.1;
  margin-bottom: 0.5rem;
  letter-spacing: -0.02em;
}

.hero-sub {
  font-size: 1rem;
  color: var(--muted);
  font-weight: 400;
  margin-bottom: 2.5rem;
  max-width: 520px;
}

.stat-row {
  display: flex;
  gap: 1rem;
  margin-bottom: 2.5rem;
  flex-wrap: wrap;
}

.stat-pill {
  background: var(--bg3);
  border: 1px solid var(--border2);
  border-radius: 6px;
  padding: 6px 14px;
  font-size: 0.8rem;
  font-family: 'Space Mono', monospace;
  color: var(--muted);
  letter-spacing: 0.5px;
}

.stat-pill span { color: var(--accent); font-weight: 700; }

.section-eyebrow {
  font-family: 'Space Mono', monospace;
  font-size: 0.65rem;
  font-weight: 700;
  letter-spacing: 3px;
  color: var(--muted);
  text-transform: uppercase;
  margin-bottom: 0.6rem;
}

.q-card {
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 1.4rem 1.6rem 1rem;
  margin-bottom: 0.5rem;
  position: relative;
  transition: border-color 0.2s;
}
.q-card:hover { border-color: var(--border2); }

.q-index {
  font-family: 'Space Mono', monospace;
  font-size: 0.65rem;
  color: var(--accent);
  letter-spacing: 2px;
  text-transform: uppercase;
  margin-bottom: 0.6rem;
}

.q-text {
  font-size: 1.05rem;
  font-weight: 600;
  color: var(--text);
  line-height: 1.5;
  margin-bottom: 1rem;
}

.result-card {
  border-radius: 10px;
  padding: 1.2rem 1.4rem;
  margin-bottom: 0.75rem;
  border: 1px solid;
}
.result-correct {
  background: rgba(52,211,153,0.06);
  border-color: rgba(52,211,153,0.2);
}
.result-wrong {
  background: rgba(248,113,113,0.06);
  border-color: rgba(248,113,113,0.2);
}

.result-status {
  font-family: 'Space Mono', monospace;
  font-size: 0.65rem;
  font-weight: 700;
  letter-spacing: 2px;
  text-transform: uppercase;
  margin-bottom: 0.5rem;
}
.status-correct { color: var(--green); }
.status-wrong   { color: var(--red); }

.result-q   { font-weight: 600; margin-bottom: 0.5rem; font-size: 0.97rem; }
.result-ans { font-size: 0.87rem; margin: 2px 0; }
.result-expl {
  font-size: 0.83rem;
  color: var(--muted);
  margin-top: 0.5rem;
  padding-top: 0.5rem;
  border-top: 1px solid var(--border);
  font-style: italic;
}

.score-box {
  background: var(--bg2);
  border: 1px solid var(--border2);
  border-radius: 16px;
  padding: 2.5rem 2rem;
  text-align: center;
  margin-bottom: 2rem;
  position: relative;
  overflow: hidden;
}
.score-box::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0; height: 3px;
  background: linear-gradient(90deg, var(--accent), var(--accent2));
}

.score-number {
  font-family: 'Space Mono', monospace;
  font-size: 4.5rem;
  font-weight: 700;
  color: var(--accent);
  line-height: 1;
  margin-bottom: 0.25rem;
}
.score-denom {
  color: var(--muted);
  font-size: 1.8rem;
}
.score-pct {
  font-family: 'Figtree', sans-serif;
  font-size: 1rem;
  color: var(--muted);
  margin-top: 0.4rem;
}
.score-badge {
  display: inline-block;
  margin-top: 1rem;
  background: rgba(245,166,35,0.1);
  border: 1px solid rgba(245,166,35,0.3);
  color: var(--accent);
  border-radius: 99px;
  padding: 6px 18px;
  font-family: 'Space Mono', monospace;
  font-size: 0.75rem;
  letter-spacing: 1px;
}

.empty-state {
  text-align: center;
  padding: 5rem 2rem;
  border: 1px dashed var(--border2);
  border-radius: 16px;
  background: var(--bg2);
  margin-top: 1rem;
}
.empty-icon  { font-size: 3rem; margin-bottom: 1rem; }
.empty-title {
  font-family: 'Figtree', sans-serif;
  font-size: 1.2rem;
  font-weight: 700;
  color: var(--muted);
  margin-bottom: 0.4rem;
}
.empty-sub { font-size: 0.88rem; color: var(--border2); }

.tip-box {
  background: var(--bg3);
  border-left: 2px solid var(--accent);
  border-radius: 0 6px 6px 0;
  padding: 0.7rem 1rem;
  font-size: 0.82rem;
  color: var(--muted);
  margin-top: 0.5rem;
  line-height: 1.5;
}

.progress-wrap { margin-bottom: 1.5rem; }
.progress-label {
  display: flex;
  justify-content: space-between;
  font-size: 0.8rem;
  color: var(--muted);
  font-family: 'Space Mono', monospace;
  margin-bottom: 0.4rem;
}

.sidebar-logo {
  font-family: 'Space Mono', monospace;
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--accent);
  letter-spacing: 2px;
  margin-bottom: 1.5rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
</style>
""", unsafe_allow_html=True)


# ─── Configuration ─────────────────────────────────────────────────────────────
DEFAULT_MODEL = "gpt-4o-mini"
DEFAULT_API_BASE = "https://api.openai.com/v1"

PROVIDER_PRESETS = {
    "OpenAI": {
        "base_url": "https://api.openai.com/v1",
        "model": "gpt-4o-mini",
        "auth_type": "bearer",
    },
    "Euron": {
        "base_url": "https://api.euron.one/api/v1/euri",
        "model": "gpt-4.1-nano",
        "auth_type": "bearer",
    },
    "OpenRouter": {
        "base_url": "https://openrouter.ai/api/v1",
        "model": "openai/gpt-4o-mini",
        "auth_type": "bearer",
    },
    "Groq": {
        "base_url": "https://api.groq.com/openai/v1",
        "model": "llama-3.1-8b-instant",
        "auth_type": "bearer",
    },
}

DIFFICULTY_CONFIG = {
    "Easy":   {"emoji": "🟢", "color": "#34d399", "desc": "Fundamentals & basics"},
    "Medium": {"emoji": "🟡", "color": "#fbbf24", "desc": "Applied knowledge"},
    "Hard":   {"emoji": "🔴", "color": "#f87171", "desc": "Deep understanding"},
}


# ─── API Test Function ─────────────────────────────────────────────────────────
def mask_key(api_key):
    """Mask API key for display (show only first and last 4 chars)"""
    if len(api_key) <= 8:
        return "***"
    return f"{api_key[:4]}...{api_key[-4:]}"


def test_api_key(api_key, base_url, model):
    """Test if API key works by making a simple request"""
    try:
        import httpx
        import json as json_lib
        
        masked_key = mask_key(api_key)
        logger.debug(f"Testing API key: {masked_key}")
        logger.debug(f"Base URL: {base_url}")
        logger.debug(f"Model: {model.strip()}")
        
        headers = {
            "Authorization": f"Bearer {api_key.strip()}",
            "Content-Type": "application/json",
        }
        
        payload = {
            "model": model.strip(),
            "messages": [{"role": "user", "content": "Say 'OK'"}],
            "max_tokens": 10,
        }
        
        api_url = base_url.strip().rstrip("/") + "/chat/completions"
        
        logger.info(f"Testing API connection to: {api_url}")
        
        with httpx.Client(timeout=10.0, verify=False) as client:
            response = client.post(api_url, json=payload, headers=headers)
        
        logger.debug(f"API Response status: {response.status_code}")
        
        if response.status_code == 200:
            logger.info("✅ API key validation successful")
            return True, "✅ API key is valid! Your key and base URL are working."
        elif response.status_code == 401:
            resp_data = response.json()
            error_msg = resp_data.get("error", {}).get("message", "Unknown error")
            logger.warning(f"API authentication failed: {error_msg}")
            return False, f"❌ Authentication failed: {error_msg}"
        elif response.status_code == 404:
            logger.warning("API endpoint not found (404)")
            return False, "❌ API endpoint not found. Check base URL."
        else:
            resp_text = response.text[:200]
            logger.warning(f"API returned error {response.status_code}: {resp_text}")
            return False, f"❌ API returned error {response.status_code}."
            
    except Exception as e:
        logger.error(f"API test failed: {type(e).__name__}: {str(e)[:100]}")
        return False, f"❌ Connection failed: {str(e)[:60]}"


# ─── Quiz Generator ────────────────────────────────────────────────────────────
def generate_quiz(topic, difficulty, num_q, api_key, base_url, model, auth_type="bearer"):
    try:
        import json as json_lib
        import httpx
        
        # Validate inputs
        if not api_key or len(api_key.strip()) == 0:
            logger.warning("Generate quiz attempt: API key is empty")
            return None, "API key is empty. Please enter a valid API key."
        if not base_url or len(base_url.strip()) == 0:
            logger.warning("Generate quiz attempt: Base URL is empty")
            return None, "API base URL is required."
        if not model or len(model.strip()) == 0:
            logger.warning("Generate quiz attempt: Model name is empty")
            return None, "Model name is required."
        
        logger.info(f"Generating quiz: topic='{topic}', difficulty='{difficulty}', count={num_q}, model='{model}'")
        
        prompt = f"""You are an expert quiz creator. Generate exactly {num_q} multiple-choice questions about "{topic}" at {difficulty} difficulty.

Rules:
- Each question must have exactly 4 options: A), B), C), D)
- Exactly one option is correct
- Explanations must be concise (1-2 sentences max)
- Questions should match the difficulty: Easy=basic recall, Medium=application, Hard=analysis/edge-cases
- Do NOT include any markdown, code fences, or commentary — output raw JSON only

Output format (strict JSON array):
[
  {{
    "question": "Question text?",
    "options": ["A) ...", "B) ...", "C) ...", "D) ..."],
    "answer": "A) ...",
    "explanation": "Short explanation."
  }}
]"""

        # Build headers with auth
        headers = {
            "Content-Type": "application/json",
        }
        
        if auth_type.lower() == "bearer":
            headers["Authorization"] = f"Bearer {api_key.strip()}"
        else:
            headers["Authorization"] = api_key.strip()
        
        payload = {
            "model": model.strip(),
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.75,
            "max_tokens": 4096,
        }
        
        # Ensure base_url ends with /chat/completions
        api_url = base_url.strip().rstrip("/") + "/chat/completions"
        
        masked_key = mask_key(api_key)
        logger.debug(f"API Request - URL: {api_url}, Model: {model.strip()}, Auth: {auth_type}")
        logger.debug(f"API Request - API Key: {masked_key}, Headers: {{'Authorization': 'Bearer ***', 'Content-Type': 'application/json'}}")
        
        with httpx.Client(timeout=60.0, verify=False) as client:
            response = client.post(api_url, json=payload, headers=headers)
        
        logger.debug(f"API Response status: {response.status_code}")
        
        if response.status_code == 401:
            resp_data = response.json()
            error_msg = resp_data.get("error", {}).get("message", "Unknown error")
            logger.warning(f"Quiz generation failed - Authentication error: {error_msg}")
            return None, "❌ Invalid API key. Please check your key and try again."
        elif response.status_code == 429:
            logger.warning("Quiz generation failed - Rate limit exceeded")
            return None, "❌ Rate limit exceeded. Wait a moment and try again."
        elif response.status_code == 404:
            logger.warning(f"Quiz generation failed - Endpoint not found at {api_url}")
            return None, "❌ API endpoint not found. Check base URL."
        elif response.status_code != 200:
            resp_data = response.json()
            error_msg = json_lib.dumps(resp_data).lower()
            logger.warning(f"Quiz generation failed - API error {response.status_code}: {resp_data}")
            if "model" in error_msg or "not found" in error_msg:
                return None, f"❌ Model '{model}' not found or not available."
            return None, f"❌ API error: {response.status_code}"
        
        resp_json = response.json()
        raw = resp_json["choices"][0]["message"]["content"].strip()
        
        # Strip any accidental markdown fences
        raw = re.sub(r"^```(?:json)?\s*", "", raw)
        raw = re.sub(r"\s*```$", "", raw)
        raw = raw.strip()

        questions = json.loads(raw)
        logger.debug(f"Parsed {len(questions)} questions from API response")

        # Validate structure and normalize whitespace
        for i, q in enumerate(questions):
            assert "question" in q and "options" in q and "answer" in q and "explanation" in q
            assert len(q["options"]) == 4
            # Normalize all strings by stripping whitespace
            q["question"] = q["question"].strip()
            q["options"] = [opt.strip() for opt in q["options"]]
            q["answer"] = q["answer"].strip()
            q["explanation"] = q["explanation"].strip()
            # Verify answer is in options
            assert q["answer"] in q["options"], f"Q{i+1}: Answer '{q['answer']}' not found in options: {q['options']}"
            logger.debug(f"Q{i+1}: Normalized answer = '{q['answer']}'")
        
        logger.info(f"✅ Quiz generated successfully - {len(questions)} questions created")
        return questions, None

    except json.JSONDecodeError as e:
        logger.error(f"JSON Parse Error: {str(e)[:100]}")
        return None, "❌ AI response was malformed. Try again."
    except AssertionError as e:
        logger.error(f"Response validation failed: {str(e)[:100]}")
        return None, "❌ AI response format was unexpected. Try again."
    except Exception as e:
        error_str = str(e).lower()
        logger.error(f"Unexpected Error ({type(e).__name__}): {str(e)[:100]}")
        # Don't expose full error if it contains sensitive info
        if "authorization" in error_str or "bearer" in error_str:
            return None, "❌ Authentication error. Check your API key."
        elif "connection" in error_str or "timeout" in error_str or "certificate" in error_str:
            return None, "❌ Connection failed. Check base URL and internet, then try again."
        return None, f"❌ Error: {str(e)[:80]}"


# ─── Session State Defaults ────────────────────────────────────────────────────
DEFAULTS = {
    "questions": None,
    "answers": {},
    "submitted": False,
    "score": 0,
    "quiz_topic": "",
    "quiz_difficulty": "Medium",
    "quiz_provider": "OpenAI",
    "quiz_count": 0,
}
for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ─── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-logo">⚡ QuizCraft</div>', unsafe_allow_html=True)

    # ── API Provider ──
    st.markdown('<div class="section-eyebrow">API Provider</div>', unsafe_allow_html=True)
    provider = st.selectbox(
        "Provider",
        list(PROVIDER_PRESETS.keys()),
        label_visibility="collapsed",
    )
    
    preset = PROVIDER_PRESETS[provider]
    
    # Show provider-specific help
    if provider == "Euron":
        st.markdown(
            '<div class="tip-box">⚠️ <b>Euron Setup:</b><br/>1. Key must start with <code style="background:#1a1a1e;padding:2px 4px;border-radius:3px">euri-</code><br/>2. Use "Test API Key" button to verify<br/>3. If test fails, generate a new key in your Euron account</div>',
            unsafe_allow_html=True
        )

    # ── API Key ──
    st.markdown('<div class="section-eyebrow" style="margin-top:1rem">API Key</div>', unsafe_allow_html=True)
    api_key = st.text_input(
        "API Key",
        type="password",
        placeholder="sk-... or euri-... or your-api-key",
        label_visibility="collapsed",
    )

    # ── Base URL ──
    st.markdown('<div class="section-eyebrow" style="margin-top:1rem">API Base URL</div>', unsafe_allow_html=True)
    base_url = st.text_input(
        "Base URL",
        value=preset["base_url"],
        placeholder="https://api.example.com/v1",
        label_visibility="collapsed",
    )

    # ── Model ──
    st.markdown('<div class="section-eyebrow" style="margin-top:1rem">Model</div>', unsafe_allow_html=True)
    model = st.text_input(
        "Model",
        value=preset["model"],
        placeholder="gpt-4o-mini",
        label_visibility="collapsed",
    )

    st.divider()
    
    # ── Test API Key ──
    st.markdown('<div class="section-eyebrow">API Diagnostics</div>', unsafe_allow_html=True)
    if st.button("🔍 Test API Key", use_container_width=True, help="Test if your API key works"):
        if not api_key:
            st.error("⚠️ Please enter an API key first.")
        else:
            with st.spinner("Testing API key..."):
                success, message = test_api_key(api_key, base_url, model)
                if success:
                    st.success(message)
                else:
                    st.error(message)
    
    st.divider()

    # ── Quiz Settings ──
    st.markdown('<div class="section-eyebrow">Topic</div>', unsafe_allow_html=True)
    topic = st.text_input(
        "Topic",
        placeholder="e.g. Python, Solar System, WW2…",
        label_visibility="collapsed",
    )

    st.markdown('<div class="section-eyebrow" style="margin-top:1rem">Difficulty</div>', unsafe_allow_html=True)
    difficulty = st.select_slider(
        "Difficulty",
        options=["Easy", "Medium", "Hard"],
        value="Medium",
        label_visibility="collapsed",
    )
    dc = DIFFICULTY_CONFIG[difficulty]
    st.markdown(
        f'<div style="font-size:0.82rem;color:{dc["color"]};font-family:\'Space Mono\',monospace;margin-top:0.2rem">'
        f'{dc["emoji"]} {difficulty} — {dc["desc"]}</div>',
        unsafe_allow_html=True
    )

    st.markdown('<div class="section-eyebrow" style="margin-top:1rem">Questions</div>', unsafe_allow_html=True)
    num_q = st.slider("Questions", 3, 20, 5, label_visibility="collapsed")

    st.divider()
    generate_btn = st.button("⚡ Generate Quiz", use_container_width=True)


# ─── MAIN ─────────────────────────────────────────────────────────────────────
# Header
st.markdown("""
<div class="brand">⚡ QuizCraft AI</div>
<div class="hero-title">Test Your Knowledge.<br>Powered by AI.</div>
<div class="hero-sub">
  Pick your AI provider, enter your API key, add a topic — get a custom quiz in seconds.
  Works with OpenAI, Euron, OpenRouter, Groq, and any OpenAI-compatible API.
</div>
""", unsafe_allow_html=True)


# ─── Generate ─────────────────────────────────────────────────────────────────
if generate_btn:
    errors = []
    if not api_key:
        errors.append("API key is required.")
    if not topic.strip():
        errors.append("Please enter a topic.")
    if not base_url.strip():
        errors.append("API base URL is required.")
    if not model.strip():
        errors.append("Model name is required.")

    if errors:
        for e in errors:
            st.error(f"⚠️ {e}")
    else:
        # Reset state
        st.session_state.questions = None
        st.session_state.answers = {}
        st.session_state.submitted = False

        with st.spinner(f"Crafting {num_q} questions on **{topic.strip()}**…"):
            preset = PROVIDER_PRESETS.get(provider, {})
            auth_type = preset.get("auth_type", "bearer")
            qs, err = generate_quiz(
                topic.strip(), difficulty, num_q,
                api_key, base_url.strip(), model.strip(), auth_type
            )

        if err:
            st.error(err)
        else:
            st.session_state.questions = qs
            st.session_state.quiz_topic = topic.strip()
            st.session_state.quiz_difficulty = difficulty
            st.session_state.quiz_provider = provider
            st.session_state.quiz_count += 1
            st.rerun()


# ─── Quiz in progress ──────────────────────────────────────────────────────────
if st.session_state.questions and not st.session_state.submitted:
    qs = st.session_state.questions
    t  = st.session_state.quiz_topic
    d  = st.session_state.quiz_difficulty
    p  = st.session_state.quiz_provider
    dc = DIFFICULTY_CONFIG[d]

    # Meta row
    st.markdown(
        f'<div class="stat-row">'
        f'<div class="stat-pill">📚 <span>{t}</span></div>'
        f'<div class="stat-pill">{dc["emoji"]} <span>{d}</span></div>'
        f'<div class="stat-pill">❓ <span>{len(qs)} questions</span></div>'
        f'<div class="stat-pill">🔌 <span>{p}</span></div>'
        f'</div>',
        unsafe_allow_html=True
    )

    # Live progress (reads current radio state)
    answered_count = sum(
        1 for i in range(len(qs))
        if st.session_state.get(f"q_{i}") is not None
    )
    pct = answered_count / len(qs)
    st.markdown(
        f'<div class="progress-label"><span>Progress</span><span>{answered_count}/{len(qs)} answered</span></div>',
        unsafe_allow_html=True
    )
    st.progress(pct)
    st.markdown("<br>", unsafe_allow_html=True)

    with st.form("quiz_form", clear_on_submit=False):
        for i, q in enumerate(qs):
            st.markdown(
                f'<div class="q-card">'
                f'<div class="q-index">Question {i+1} of {len(qs)}</div>'
                f'<div class="q-text">{q["question"]}</div>'
                f'</div>',
                unsafe_allow_html=True
            )
            st.radio(
                label=f"answer_{i}",
                options=q["options"],
                key=f"q_{i}",
                index=None,
                label_visibility="collapsed",
            )
            st.markdown("<br>", unsafe_allow_html=True)

        col1, col2 = st.columns([5, 2])
        with col1:
            submitted = st.form_submit_button("✅ Submit Answers", use_container_width=True)
        with col2:
            reset = st.form_submit_button("🔄 New Quiz", use_container_width=True)

    if reset:
        st.session_state.questions = None
        st.session_state.answers = {}
        st.session_state.submitted = False
        st.rerun()

    if submitted:
        # Collect answers
        answers = {i: st.session_state.get(f"q_{i}") for i in range(len(qs))}
        unanswered = [i+1 for i, a in answers.items() if a is None]

        if unanswered:
            q_list = ", ".join(f"Q{n}" for n in unanswered)
            st.warning(f"⚠️ Please answer all questions first. Missing: {q_list}")
        else:
            st.session_state.answers = answers
            st.session_state.submitted = True
            st.session_state.score = sum(
                1 for i, q in enumerate(qs)
                if answers[i].strip() == q["answer"].strip()
            )
            # Log answer details for debugging
            logger.debug(f"Quiz submitted with {len(answers)} answers")
            for i, q in enumerate(qs):
                user_ans = answers[i].strip()
                correct_ans = q["answer"].strip()
                is_correct = user_ans == correct_ans
                logger.debug(f"Q{i+1}: User='{user_ans}' | Correct='{correct_ans}' | Match={is_correct}")
            st.rerun()


# ─── Results ──────────────────────────────────────────────────────────────────
if st.session_state.submitted and st.session_state.questions:
    qs      = st.session_state.questions
    answers = st.session_state.answers
    score   = st.session_state.score
    total   = len(qs)
    pct     = int(score / total * 100)
    t       = st.session_state.quiz_topic
    d       = st.session_state.quiz_difficulty

    if pct >= 90:   grade, msg = "A+", "Outstanding! 🏆"
    elif pct >= 80: grade, msg = "A",  "Excellent work! ⭐"
    elif pct >= 70: grade, msg = "B",  "Great job! 👍"
    elif pct >= 60: grade, msg = "C",  "Good effort! 📖"
    elif pct >= 50: grade, msg = "D",  "Keep practicing! 💪"
    else:           grade, msg = "F",  "More study needed! 📚"

    # Score card
    st.markdown(f"""
<div class="score-box">
  <div class="score-number">{score}<span class="score-denom">/{total}</span></div>
  <div class="score-pct">{pct}% correct</div>
  <div class="score-badge">{grade} — {msg}</div>
</div>
""", unsafe_allow_html=True)

    # Stat pills
    wrong = total - score
    st.markdown(
        f'<div class="stat-row" style="margin-bottom:1.5rem">'
        f'<div class="stat-pill">📚 <span>{t}</span></div>'
        f'<div class="stat-pill">✅ <span>{score} correct</span></div>'
        f'<div class="stat-pill">❌ <span>{wrong} wrong</span></div>'
        f'<div class="stat-pill">📊 <span>{pct}%</span></div>'
        f'</div>',
        unsafe_allow_html=True
    )

    # Answer review
    st.markdown('<div class="section-eyebrow">Answer Review</div>', unsafe_allow_html=True)

    for i, q in enumerate(qs):
        user = answers.get(i)
        correct = q["answer"]
        ok = user == correct

        cls   = "result-correct" if ok else "result-wrong"
        s_cls = "status-correct" if ok else "status-wrong"
        label = "✓ Correct" if ok else "✗ Incorrect"

        user_line = f'<div class="result-ans" style="color:{"#34d399" if ok else "#f87171"}">Your answer: {user}</div>'
        correct_line = "" if ok else f'<div class="result-ans" style="color:#34d399">Correct answer: {correct}</div>'

        st.markdown(f"""
<div class="result-card {cls}">
  <div class="result-status {s_cls}">{label} — Q{i+1}</div>
  <div class="result-q">{q['question']}</div>
  {user_line}
  {correct_line}
  <div class="result-expl">💡 {q['explanation']}</div>
</div>
""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Retry Same Topic", use_container_width=True):
            st.session_state.questions  = None
            st.session_state.answers    = {}
            st.session_state.submitted  = False
            st.rerun()
    with col2:
        if st.button("🆕 New Topic", use_container_width=True):
            st.session_state.questions  = None
            st.session_state.answers    = {}
            st.session_state.submitted  = False
            st.session_state.quiz_topic = ""
            st.rerun()


# ─── Empty State ───────────────────────────────────────────────────────────────
if not st.session_state.questions and not st.session_state.submitted:
    st.markdown("""
<div class="empty-state">
  <div class="empty-icon">⚡</div>
  <div class="empty-title">Ready when you are</div>
  <div class="empty-sub">Select a provider, enter your API key and topic in the sidebar, then hit Generate.</div>
</div>
""", unsafe_allow_html=True)
