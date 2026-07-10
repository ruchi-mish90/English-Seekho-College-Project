"""
English Learning Chatbot — Flask Backend
Free, offline NLP using NLTK. No paid APIs required.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from nlp_engine import process_message, list_all_lessons, get_quiz, LESSONS

app = Flask(__name__)
CORS(app)  # Allow frontend (any origin) to call backend


@app.route("/", methods=["GET"])
def health():
    return jsonify({"status": "ok", "message": "English Learning Chatbot API is running!"})


@app.route("/chat", methods=["POST"])
def chat():
    """
    POST /chat
    Body: { "message": "...", "context": { "current_lesson": "..." } }
    Returns: response payload from nlp_engine.process_message()
    """
    data = request.get_json(silent=True) or {}
    user_message = data.get("message", "").strip()
    context = data.get("context", {})

    if not user_message:
        return jsonify({"type": "error", "text": "Please send a message!"}), 400

    response = process_message(user_message, context)
    return jsonify(response)


@app.route("/lessons", methods=["GET"])
def lessons():
    """GET /lessons — returns list of all available lessons."""
    return jsonify(list_all_lessons())


@app.route("/lesson/<lesson_key>", methods=["GET"])
def lesson(lesson_key):
    """GET /lesson/<key> — returns full lesson content."""
    if lesson_key not in LESSONS:
        return jsonify({"error": "Lesson not found"}), 404
    l = LESSONS[lesson_key]
    return jsonify({
        "type": "lesson",
        "title": l["title"],
        "level": l["level"],
        "content": l["content"],
        "lesson_key": lesson_key,
    })


@app.route("/quiz/<lesson_key>", methods=["GET"])
def quiz(lesson_key):
    """GET /quiz/<key> — returns quiz for a lesson."""
    return jsonify(get_quiz(lesson_key))


if __name__ == "__main__":
    print("\n🎓 English Learning Chatbot Backend")
    print("   Running on http://localhost:5000")
    print("   Press Ctrl+C to stop\n")
    app.run(debug=False, port=5000, host="0.0.0.0")
