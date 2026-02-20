# 🧠 AI-Powered Quiz Generator

A Generative AI web app built with Python and Streamlit that creates customized MCQ quizzes on any topic in seconds — powered by OpenAI's GPT model.

---

## 🚀 Live Demo

> Hosted on **Streamlit Cloud** (Free)  
> `https://sanyamsinghai-quiz-generator.streamlit.app`

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| Language | Python 3.10+ |
| UI Framework | Streamlit |
| AI Model | OpenAI GPT-4o-mini (via API) |
| Hosting | Streamlit Cloud (Free) |
| Key Storage | User-provided (no backend needed) |

---

## ✨ Features

- 🎯 **Any Topic** — Enter any subject (History, Python, Biology, etc.)
- 🎚️ **Difficulty Levels** — Easy / Medium / Hard
- 🔢 **Custom Question Count** — 1 to 20 questions per session
- ✅ **Instant Results** — Score, correct answers, and explanations shown after submission
- 🔑 **User API Key** — User provides their own OpenAI key → zero cost for you
- 🔄 **Regenerate** — Generate a fresh quiz on the same topic anytime
- 📋 **Clean UI** — Radio buttons for each MCQ, progress indicator, submit button

---

## 📁 Project Structure

```
ai-quiz-generator/
├── app.py               # Main Streamlit app
├── quiz_generator.py    # OpenAI API call + prompt logic
├── requirements.txt     # Python dependencies
└── README.md
```

---

## 🔧 How to Run Locally

```bash
# Clone the repo
git clone https://github.com/sanyamsinghai/ai-quiz-generator.git
cd ai-quiz-generator

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

> You'll be asked to enter your OpenAI API key inside the app.

---

## 📦 requirements.txt

```
streamlit>=1.35.0
openai>=1.30.0
```

---

## 🧩 Core Implementation

### `quiz_generator.py` — Prompt + API Call
```python
import openai
import json

def generate_quiz(topic: str, difficulty: str, num_questions: int, api_key: str) -> list:
    client = openai.OpenAI(api_key=api_key)

    prompt = f"""
    Generate {num_questions} multiple choice questions about "{topic}".
    Difficulty: {difficulty}.
    
    Return ONLY a valid JSON array in this exact format:
    [
      {{
        "question": "Question text here?",
        "options": ["A) option1", "B) option2", "C) option3", "D) option4"],
        "answer": "A) option1",
        "explanation": "Brief explanation of why this is correct."
      }}
    ]
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    raw = response.choices[0].message.content
    return json.loads(raw)
```

### `app.py` — Streamlit UI
```python
import streamlit as st
from quiz_generator import generate_quiz

st.title("🧠 AI Quiz Generator")
st.caption("Generate MCQ quizzes on any topic using OpenAI")

# Sidebar — settings
with st.sidebar:
    api_key = st.text_input("🔑 OpenAI API Key", type="password")
    topic = st.text_input("📚 Topic", placeholder="e.g. Python, World War II")
    difficulty = st.selectbox("🎚️ Difficulty", ["Easy", "Medium", "Hard"])
    num_q = st.slider("🔢 Number of Questions", 1, 20, 5)
    generate = st.button("Generate Quiz")

# Generate quiz
if generate:
    if not api_key or not topic:
        st.warning("Please enter your API key and a topic.")
    else:
        with st.spinner("Generating your quiz..."):
            questions = generate_quiz(topic, difficulty, num_q, api_key)
            st.session_state["questions"] = questions
            st.session_state["submitted"] = False
            st.session_state["answers"] = {}

# Display quiz
if "questions" in st.session_state and not st.session_state.get("submitted"):
    questions = st.session_state["questions"]
    with st.form("quiz_form"):
        for i, q in enumerate(questions):
            st.markdown(f"**Q{i+1}. {q['question']}**")
            st.session_state["answers"][i] = st.radio(
                label="",
                options=q["options"],
                key=f"q_{i}",
                index=None
            )
        submitted = st.form_submit_button("✅ Submit Quiz")
        if submitted:
            st.session_state["submitted"] = True
            st.rerun()

# Show results
if st.session_state.get("submitted"):
    questions = st.session_state["questions"]
    answers = st.session_state["answers"]
    score = 0

    st.subheader("📊 Results")
    for i, q in enumerate(questions):
        user_ans = answers.get(i)
        correct = q["answer"]
        is_correct = user_ans == correct
        if is_correct:
            score += 1
        status = "✅" if is_correct else "❌"
        st.markdown(f"{status} **Q{i+1}:** {q['question']}")
        st.markdown(f"- Your answer: `{user_ans}`")
        if not is_correct:
            st.markdown(f"- Correct answer: `{correct}`")
        st.caption(f"💡 {q['explanation']}")
        st.divider()

    st.success(f"🎯 Your Score: **{score}/{len(questions)}**")
    if st.button("🔄 Try Again"):
        del st.session_state["questions"]
        st.rerun()
```

---

## 🌐 Deploy on Streamlit Cloud (Free)

1. Push all files to a **public GitHub repo**
2. Go to [streamlit.io/cloud](https://streamlit.io/cloud) → Sign in with GitHub
3. Click **New App** → Select your repo and `app.py`
4. Click **Deploy** — live in ~2 minutes at:  
   `https://your-username-your-repo.streamlit.app`

> ✅ **100% Free** — Streamlit Cloud hosts public apps for free. No credit card needed.

---

## 🔑 About the API Key

- Users enter their own OpenAI API key inside the sidebar
- The key is **never stored** — it exists only in the current session
- This keeps your hosting cost at **zero**
- Users can get a free-tier key at [platform.openai.com](https://platform.openai.com)

---

## 🔮 Future Improvements

- [ ] Timer per question
- [ ] Topic suggestions / presets
- [ ] Download quiz as PDF
- [ ] Leaderboard (store scores with username)
- [ ] Support for image-based questions

---

## 👤 Author

**Sanyam Singhai**  
B.Tech CSE | SVVV Indore  
GitHub: [@sanyamsinghai](https://github.com/sanyamsinghai)
