# ⚡ QuizCraft AI — Multi-Provider Quiz Generator

A production-ready AI quiz app built with Python + Streamlit. Generate customized MCQ quizzes on any topic using your own API key from any provider.

---

## 🚀 Live Demo
`https://sanyamsinghai-quizcraft.streamlit.app`

---

## ✨ Features

| Feature | Detail |
|---------|--------|
| **Any Topic** | Python, History, Biology, anything |
| **Difficulty Levels** | Easy / Medium / Hard |
| **Custom Question Count** | 3–20 per quiz |
| **Multi-Provider** | OpenAI, OpenRouter, Euron, Groq, or any custom endpoint |
| **Instant Scoring** | Score, grade, correct answers + explanations |
| **Progress Tracker** | Live progress bar while answering |
| **Zero Cost** | User brings their own key — you pay nothing |

---

## 🔌 Supported API Providers

| Provider | Key Prefix | Free Tier |
|----------|-----------|-----------|
| OpenAI | `sk-...` | Limited |
| OpenRouter | `sk-or-v1-...` | ✅ Many free models |
| Euron | `eu-...` | ✅ |
| Groq | `gsk_...` | ✅ Very fast |
| Custom / Other | any | Depends |

---

## 📁 Project Structure

```
quizcraft/
├── app.py                  # Full Streamlit app (UI + logic)
├── requirements.txt        # Dependencies
├── .streamlit/
│   └── config.toml         # Theme config
└── README.md
```

---

## 🔧 Run Locally

```bash
git clone https://github.com/sanyamsinghai/quizcraft.git
cd quizcraft
pip install -r requirements.txt
streamlit run app.py
```

---

## 🌐 Deploy Free on Streamlit Cloud

1. Push to a **public GitHub repo**
2. Go to [streamlit.io/cloud](https://streamlit.io/cloud) → Sign in with GitHub
3. Click **New App** → select repo → set `app.py` as main file
4. Click **Deploy** → live in ~2 minutes

---

## 🔑 API Key Info

- Keys are entered by the user inside the app
- Keys are **never stored** — session only
- You pay zero for hosting
- Users can use the free tier of any supported provider

---

## 👤 Author

**Sanyam Singhai** · B.Tech CSE · SVVV Indore  
GitHub: [@sanyamsinghai](https://github.com/sanyamsinghai)
