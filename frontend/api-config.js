"use strict";

/**
 * The API is served by the same Vercel deployment under /api.
 * Using a relative URL keeps the app working on localhost and production.
 */
const API_BASE = "/api";

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
