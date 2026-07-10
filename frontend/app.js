/**
 * English Seekho — Frontend App
 * Handles: chat UI, API calls, quiz modal, score/progress tracking
 * No paid dependencies — vanilla JS only.
 */

// ---------------------------------------------------------------------------
// Config
// ---------------------------------------------------------------------------
const API_BASE = "http://localhost:5000";

// ---------------------------------------------------------------------------
// State (in-memory; persisted to localStorage where available)
// ---------------------------------------------------------------------------
const state = {
  score: 0,
  completedTopics: new Set(),
  currentLesson: null,
  quiz: {
    active: false,
    questions: [],
    currentIndex: 0,
    correctCount: 0,
    lessonKey: null,
  },
};

// ---------------------------------------------------------------------------
// localStorage helpers (gracefully degrade if unavailable)
// ---------------------------------------------------------------------------
function saveState() {
  try {
    localStorage.setItem(
      "englishSeekho",
      JSON.stringify({
        score: state.score,
        completedTopics: [...state.completedTopics],
      })
    );
  } catch (_) {}
}

function loadState() {
  try {
    const raw = localStorage.getItem("englishSeekho");
    if (!raw) return;
    const saved = JSON.parse(raw);
    state.score = saved.score || 0;
    state.completedTopics = new Set(saved.completedTopics || []);
  } catch (_) {}
}

// ---------------------------------------------------------------------------
// DOM refs
// ---------------------------------------------------------------------------
const chatMessages = document.getElementById("chatMessages");
const userInput    = document.getElementById("userInput");
const sendBtn      = document.getElementById("sendBtn");
const scoreDisplay = document.getElementById("scoreDisplay");
const levelDisplay = document.getElementById("levelDisplay");
const progressBar  = document.getElementById("progressBar");
const progressLabel= document.getElementById("progressLabel");
const quizModal    = document.getElementById("quizModal");
const quizTitle    = document.getElementById("quizTitle");
const quizBody     = document.getElementById("quizBody");
const quizNextBtn  = document.getElementById("quizNextBtn");
const quizFinishBtn= document.getElementById("quizFinishBtn");

const TOTAL_TOPICS = 9;

// ---------------------------------------------------------------------------
// Scoring & Level
// ---------------------------------------------------------------------------
function getLevel(score) {
  if (score < 50)  return "Beginner";
  if (score < 150) return "Explorer";
  if (score < 300) return "Learner";
  if (score < 500) return "Speaker";
  return "Scholar";
}

function addScore(points) {
  state.score += points;
  scoreDisplay.textContent = state.score;
  levelDisplay.textContent = getLevel(state.score);
  saveState();
}

function markTopicDone(topicKey) {
  if (!topicKey || state.completedTopics.has(topicKey)) return;
  state.completedTopics.add(topicKey);
  const btn = document.querySelector(`.topic-btn[data-topic="${topicKey}"]`);
  if (btn) btn.classList.add("completed");
  updateProgress();
  saveState();
}

function updateProgress() {
  const done = state.completedTopics.size;
  const pct  = Math.round((done / TOTAL_TOPICS) * 100);
  progressBar.style.width  = `${pct}%`;
  progressLabel.textContent = `${done} / ${TOTAL_TOPICS} topics completed`;
}

function resetProgress() {
  state.score = 0;
  state.completedTopics.clear();
  scoreDisplay.textContent = "0";
  levelDisplay.textContent = "Beginner";
  document.querySelectorAll(".topic-btn.completed").forEach(b => b.classList.remove("completed", "active"));
  updateProgress();
  saveState();
}

// ---------------------------------------------------------------------------
// Simple Markdown → HTML converter (for lesson content)
// ---------------------------------------------------------------------------
function renderMarkdown(text) {
  // Tables
  text = text.replace(/\|(.+)\|\n\|[-| ]+\|\n((?:\|.+\|\n?)+)/g, (_, header, rows) => {
    const ths = header.split("|").filter(c => c.trim()).map(c => `<th>${c.trim()}</th>`).join("");
    const trs = rows.trim().split("\n").map(row => {
      const tds = row.split("|").filter(c => c.trim()).map(c => `<td>${c.trim()}</td>`).join("");
      return `<tr>${tds}</tr>`;
    }).join("");
    return `<table><thead><tr>${ths}</tr></thead><tbody>${trs}</tbody></table>`;
  });

  // Bold (**text**)
  text = text.replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>");

  // Italic (*text*)
  text = text.replace(/\*(.+?)\*/g, "<em>$1</em>");

  // Inline code
  text = text.replace(/`(.+?)`/g, "<code>$1</code>");

  // Unordered list lines starting with -
  text = text.replace(/^- (.+)$/gm, "<li>$1</li>");
  text = text.replace(/(<li>.*<\/li>\n?)+/g, m => `<ul>${m}</ul>`);

  // Line breaks → <br> (but don't double-break after block elements)
  text = text.replace(/\n{2,}/g, "<br><br>");
  text = text.replace(/\n/g, "<br>");

  return `<div class="rendered-md">${text}</div>`;
}

// ---------------------------------------------------------------------------
// Chat message rendering
// ---------------------------------------------------------------------------
function scrollToBottom() {
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

function addMessage(role, html, extraClass = "") {
  const row    = document.createElement("div");
  row.className = `message-row ${role}`;

  const avatar = document.createElement("div");
  avatar.className = "msg-avatar";
  avatar.textContent = role === "bot" ? "🎓" : "🧑";

  const bubble = document.createElement("div");
  bubble.className = `msg-bubble ${extraClass}`;
  bubble.innerHTML  = html;

  row.appendChild(avatar);
  row.appendChild(bubble);
  chatMessages.appendChild(row);
  scrollToBottom();
  return bubble;
}

function showTyping() {
  const row    = document.createElement("div");
  row.className = "message-row bot";
  row.id        = "typingRow";

  const avatar = document.createElement("div");
  avatar.className = "msg-avatar";
  avatar.textContent = "🎓";

  const bubble = document.createElement("div");
  bubble.className = "msg-bubble";
  bubble.innerHTML  = `<div class="typing-indicator"><span></span><span></span><span></span></div>`;

  row.appendChild(avatar);
  row.appendChild(bubble);
  chatMessages.appendChild(row);
  scrollToBottom();
}

function removeTyping() {
  const row = document.getElementById("typingRow");
  if (row) row.remove();
}

// ---------------------------------------------------------------------------
// Response rendering
// ---------------------------------------------------------------------------
function renderResponse(data) {
  switch (data.type) {

    case "text":
    case "help":
      addMessage("bot", renderMarkdown(data.text));
      break;

    case "lesson": {
      state.currentLesson = data.lesson_key;
      markTopicDone(data.lesson_key);

      const html = `
        <div class="lesson-card">
          <div class="lesson-header">
            <span class="lesson-title">📖 ${data.title}</span>
            <span class="lesson-badge badge-${data.level}">${data.level}</span>
          </div>
          <div class="lesson-content">${renderMarkdown(data.content)}</div>
          <button class="quiz-prompt-btn" data-lesson="${data.lesson_key}">
            📝 Take Quiz on This Topic
          </button>
        </div>
      `;
      const bubble = addMessage("bot", html);

      // Attach quiz button handler
      bubble.querySelector(".quiz-prompt-btn").addEventListener("click", e => {
        openQuiz(e.target.dataset.lesson);
      });
      break;
    }

    case "lesson_list": {
      const chips = data.lessons.map(l => `
        <button class="lesson-chip" data-lesson="${l.key}">
          <span class="chip-title">${l.title}</span>
          <span class="chip-level">${l.level}</span>
        </button>
      `).join("");

      const html = `
        <div>
          <p style="margin-bottom:10px;">${data.text}</p>
          <div class="lesson-list-grid">${chips}</div>
        </div>
      `;
      const bubble = addMessage("bot", html);
      bubble.querySelectorAll(".lesson-chip").forEach(btn => {
        btn.addEventListener("click", () => fetchLesson(btn.dataset.lesson));
      });
      break;
    }

    case "quiz":
      openQuiz(data.lesson_key, data);
      break;

    case "error":
      addMessage("bot", `<span style="color:#dc2626">⚠️ ${data.text || "Something went wrong."}</span>`);
      break;

    default:
      addMessage("bot", `<em>Unknown response type: ${data.type}</em>`);
  }
}

// ---------------------------------------------------------------------------
// API calls
// ---------------------------------------------------------------------------
async function sendToBot(message) {
  if (!message.trim()) return;

  addMessage("user", escapeHtml(message));
  userInput.value = "";
  sendBtn.disabled = true;
  showTyping();

  try {
    const res = await fetch(`${API_BASE}/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        message,
        context: { current_lesson: state.currentLesson },
      }),
    });

    if (!res.ok) throw new Error(`Server error: ${res.status}`);
    const data = await res.json();
    removeTyping();
    renderResponse(data);
  } catch (err) {
    removeTyping();
    addMessage("bot", `
      <span style="color:#dc2626">
        ⚠️ Could not connect to the server.<br>
        <small>Make sure the backend is running: <code>python app.py</code></small>
      </span>
    `);
    console.error(err);
  } finally {
    sendBtn.disabled = false;
    userInput.focus();
  }
}

async function fetchLesson(lessonKey) {
  showTyping();
  try {
    const res  = await fetch(`${API_BASE}/lesson/${lessonKey}`);
    const data = await res.json();
    removeTyping();
    renderResponse(data);
  } catch {
    removeTyping();
    addMessage("bot", "⚠️ Could not load lesson. Is the server running?");
  }
}

// ---------------------------------------------------------------------------
// Quiz Modal
// ---------------------------------------------------------------------------
async function openQuiz(lessonKey, dataIn = null) {
  let data = dataIn;
  if (!data) {
    try {
      const res = await fetch(`${API_BASE}/quiz/${lessonKey || "greetings"}`);
      data = await res.json();
    } catch {
      addMessage("bot", "⚠️ Could not load quiz. Is the server running?");
      return;
    }
  }

  state.quiz.active       = true;
  state.quiz.questions    = data.questions;
  state.quiz.currentIndex = 0;
  state.quiz.correctCount = 0;
  state.quiz.lessonKey    = data.lesson_key;

  quizTitle.textContent = `📝 Quiz: ${data.title}`;
  quizModal.hidden = false;
  renderQuizQuestion();
}

function renderQuizQuestion() {
  const { questions, currentIndex } = state.quiz;
  const q = questions[currentIndex];
  const total = questions.length;

  quizNextBtn.hidden   = true;
  quizFinishBtn.hidden = true;

  quizBody.innerHTML = `
    <div class="quiz-progress-text">Question ${currentIndex + 1} of ${total}</div>
    <div class="quiz-question-text">${escapeHtml(q.question)}</div>
    <div class="quiz-options" id="quizOptions">
      ${q.options.map((opt, i) => `
        <button class="quiz-option" data-index="${i}" data-value="${escapeHtml(opt)}">
          ${escapeHtml(opt)}
        </button>
      `).join("")}
    </div>
    <div class="quiz-explanation" id="quizExplain" hidden></div>
  `;

  document.querySelectorAll(".quiz-option").forEach(btn => {
    btn.addEventListener("click", handleQuizAnswer);
  });
}

function handleQuizAnswer(e) {
  const selected  = e.currentTarget.dataset.value;
  const q         = state.quiz.questions[state.quiz.currentIndex];
  const isCorrect = selected === q.answer;
  const explain   = document.getElementById("quizExplain");

  document.querySelectorAll(".quiz-option").forEach(btn => {
    btn.disabled = true;
    if (btn.dataset.value === q.answer)   btn.classList.add("correct");
    if (btn === e.currentTarget && !isCorrect) btn.classList.add("wrong");
  });

  if (isCorrect) {
    state.quiz.correctCount++;
    explain.textContent = `✅ Correct! ${q.explanation}`;
  } else {
    explain.textContent = `❌ The correct answer is: "${q.answer}". ${q.explanation}`;
  }
  explain.hidden = false;

  const isLast = state.quiz.currentIndex >= state.quiz.questions.length - 1;
  if (isLast) {
    quizFinishBtn.hidden = false;
  } else {
    quizNextBtn.hidden = false;
  }
}

function advanceQuiz() {
  state.quiz.currentIndex++;
  renderQuizQuestion();
}

function finishQuiz() {
  const { correctCount, questions, lessonKey } = state.quiz;
  const total   = questions.length;
  const pct     = Math.round((correctCount / total) * 100);
  const points  = correctCount * 10;

  addScore(points);
  if (correctCount === total) markTopicDone(lessonKey);

  let trophy = "🥉", msg = "Keep practising!";
  if (pct === 100) { trophy = "🏆"; msg = "Perfect score! Excellent work! शाबाश!"; }
  else if (pct >= 70) { trophy = "🥈"; msg = "Well done! Keep it up!"; }
  else if (pct >= 50) { trophy = "🥉"; msg = "Good effort! Try again soon!"; }

  quizNextBtn.hidden   = true;
  quizFinishBtn.hidden = true;

  quizBody.innerHTML = `
    <div class="quiz-result">
      <div class="trophy">${trophy}</div>
      <h3>${msg}</h3>
      <div class="result-score">${correctCount} <span>/ ${total} correct</span></div>
      <p>${pct}% accuracy</p>
      <div class="points-earned">+${points} points earned! 🌟</div>
    </div>
  `;

  // close button becomes "Done"
  document.getElementById("closeQuiz").textContent = "Done ✓";

  // Post summary to chat
  addMessage("bot", `
    <strong>Quiz completed! 🎉</strong><br>
    You scored <strong>${correctCount}/${total}</strong> (${pct}%) and earned <strong>+${points} points</strong>!
    ${pct === 100 ? "<br>🏆 Perfect score! शाबाश!" : ""}
  `);

  state.quiz.active = false;
}

function closeQuiz() {
  quizModal.hidden = true;
  document.getElementById("closeQuiz").textContent = "✕";
  state.quiz.active = false;
  userInput.focus();
}

// ---------------------------------------------------------------------------
// Utility
// ---------------------------------------------------------------------------
function escapeHtml(str) {
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

// ---------------------------------------------------------------------------
// Event listeners
// ---------------------------------------------------------------------------
sendBtn.addEventListener("click", () => sendToBot(userInput.value.trim()));

userInput.addEventListener("keydown", e => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    sendToBot(userInput.value.trim());
  }
});

// Sidebar topic buttons
document.querySelectorAll(".topic-btn").forEach(btn => {
  btn.addEventListener("click", () => {
    document.querySelectorAll(".topic-btn").forEach(b => b.classList.remove("active"));
    btn.classList.add("active");
    fetchLesson(btn.dataset.topic);
  });
});

// Quick action buttons
document.getElementById("quickQuiz").addEventListener("click", () => {
  openQuiz(state.currentLesson || "greetings");
});

document.getElementById("quickHelp").addEventListener("click", () => {
  sendToBot("help");
});

document.getElementById("resetProgress").addEventListener("click", () => {
  if (confirm("Reset all progress and score to zero?")) {
    resetProgress();
    addMessage("bot", "🔄 Progress reset! Let's start fresh. Type <strong>lessons</strong> to begin.");
  }
});

// Quiz modal controls
quizNextBtn.addEventListener("click", advanceQuiz);
quizFinishBtn.addEventListener("click", finishQuiz);
document.getElementById("closeQuiz").addEventListener("click", closeQuiz);
quizModal.addEventListener("click", e => {
  if (e.target === quizModal) closeQuiz();
});

// ---------------------------------------------------------------------------
// Boot
// ---------------------------------------------------------------------------
function boot() {
  loadState();
  scoreDisplay.textContent = state.score;
  levelDisplay.textContent = getLevel(state.score);
  updateProgress();

  // Restore completed topic badges
  state.completedTopics.forEach(key => {
    const btn = document.querySelector(`.topic-btn[data-topic="${key}"]`);
    if (btn) btn.classList.add("completed");
  });

  // Welcome message
  addMessage("bot", renderMarkdown(
    `**Namaste! 🙏 Welcome to English Seekho!**\n\n` +
    `I am your English learning assistant. I can help you:\n` +
    `- 📚 Learn **9 topics** — greetings, alphabet, numbers, colors & more\n` +
    `- 📝 Take **quizzes** to test your knowledge\n` +
    `- 🌟 Earn **points** and level up!\n\n` +
    `**Where would you like to start?**\n` +
    `👉 Click a topic in the sidebar, or type *alphabet*, *greetings*, *help*, etc.`
  ));

  userInput.focus();
}

boot();
