# 🎓 English Seekho — NLP Chatbot for English Learning in Rural Schools

> AI & AIML · Education – Language Learning**
> An NLP-powered chatbot that helps students in rural schools learn English — completely free, no internet required after setup, no paid APIs.

---

## 📸 Features

| Feature | Description |
|---------|-------------|
| 💬 **Chat Interface** | Natural language input — type in English or Hindi words |
| 📚 **9 Lessons** | Greetings, Alphabet, Numbers, Colors, Days, Animals, Sentences, Present Tense, Vocabulary |
| 📝 **Interactive Quiz** | Multiple-choice questions with instant feedback and explanations |
| 🌟 **Scoring System** | Points, levels (Beginner → Scholar), progress tracking |
| 📊 **Progress Bar** | Visual tracker for completed topics |
| 🔁 **Persistent Score** | Score saved in browser localStorage |
| 🌐 **Bilingual Hints** | Hindi translations included in lesson content |
| 📱 **Responsive** | Works on desktop and mobile screens |

---

## 🛠️ Tech Stack (100% Free)

| Layer | Technology | Cost |
|-------|-----------|------|
| Frontend | HTML5 + CSS3 + Vanilla JS | Free |
| Backend | Python 3 + Flask | Free |
| NLP | NLTK (regex intent matching + tokenization) | Free |
| Persistence | Browser localStorage | Free |
| Server | `python app.py` (localhost) | Free |

**No cloud APIs. No subscriptions. Works offline once installed.**

---

## 📁 Project Structure

```
english-bot/
├── backend/
│   ├── app.py              # Flask REST API server
│   ├── nlp_engine.py       # NLP: intent detection, lesson data, quiz logic
│   └── requirements.txt    # Python dependencies
├── frontend/
│   ├── index.html          # Main UI
│   ├── style.css           # Full styling
│   └── app.js              # Chat logic, quiz engine, score tracking
├── start.sh                # Linux/Mac one-command startup
├── start.bat               # Windows one-command startup
└── README.md               # This file
```

---

## 🚀 Setup & Run

### Prerequisites
- Python 3.8+ (free: https://www.python.org/downloads/)
- A modern web browser (Chrome, Firefox, Edge)

---

### Option A — One Command (Linux / Mac)

```bash
chmod +x start.sh
./start.sh
```

Then open **http://localhost:5000** in your browser... wait, the frontend is a static HTML file:

Open `frontend/index.html` directly in your browser **after** starting the backend.

---

### Option B — Manual Setup

**Step 1: Install Python dependencies**
```bash
cd backend
pip install -r requirements.txt
```

**Step 2: Download NLTK data** (one-time, needs internet)
```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet'); nltk.download('punkt_tab')"
```

**Step 3: Start the backend server**
```bash
python app.py
```
You should see:
```
🎓 English Learning Chatbot Backend
   Running on http://localhost:5000
```

**Step 4: Open the frontend**

Open `frontend/index.html` in your browser.
*(Double-click the file, or drag it into Chrome/Firefox)*

---

### Option C — Windows

Double-click `start.bat`

---

## 🎓 How to Use

| You type... | Bot does... |
|-------------|-------------|
| `hello` / `namaste` | Greets you |
| `alphabet` | Opens Alphabet lesson |
| `greetings` | Opens Greetings lesson |
| `numbers` | Opens Numbers lesson |
| `colors` | Opens Colors lesson |
| `days` | Opens Days of the Week lesson |
| `animals` | Opens Animals lesson |
| `sentences` | Opens Sentences lesson |
| `present tense` / `tense` | Opens Present Tense lesson |
| `vocabulary` / `word` | Opens Vocabulary lesson |
| `lessons` / `all topics` | Lists every lesson |
| `quiz` | Starts a quiz on the current topic |
| `help` | Shows all commands |
| `bye` | Says goodbye |

You can also **click topics in the sidebar** and use the **"Take Quiz" button** after each lesson.

---

## 📡 API Endpoints

The backend exposes a simple REST API:

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Health check |
| `POST` | `/chat` | Main chat endpoint |
| `GET` | `/lessons` | List all lessons |
| `GET` | `/lesson/<key>` | Get a specific lesson |
| `GET` | `/quiz/<key>` | Get quiz for a lesson |

**POST /chat example:**
```json
// Request
{ "message": "teach me alphabet", "context": { "current_lesson": null } }

// Response
{
  "type": "lesson",
  "title": "The English Alphabet",
  "level": "Beginner",
  "content": "...",
  "lesson_key": "alphabet"
}
```

---

## ⚠️ Known Limitations

- **No real-time speech input** — text only (a future enhancement could add Web Speech API)
- **No automated tests** — the NLP is tested with manual assertions in `nlp_engine.py`
- **Single-user** — no multi-student backend; each browser has its own localStorage score
- **NLTK data needs internet once** — after the initial `nltk.download()` calls, it works fully offline
- **NLP is rule-based** — uses regex patterns + NLTK tokenization, not a neural model
- **English only** — Hindi translations are embedded in lesson text, but the bot understands English input only

---

## 🔮 Possible Extensions

- Add speech-to-text using the free **Web Speech API** (browser built-in)
- Add more lessons: past tense, articles, prepositions, story reading
- Integrate a lightweight local model (Ollama + llama3) for open-ended QA
- Add a teacher dashboard to track class-level progress (requires a backend DB like SQLite)
- Export student scores to CSV for teacher review

---

## 📜 License

MIT — free to use, modify, and distribute.
