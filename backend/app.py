"""
English Learning Chatbot — Flask Backend
Free, offline NLP using NLTK. No paid APIs required.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from nlp_engine import process_message, list_all_lessons, get_quiz, LESSONS

app = Flask(__name__)
CORS(app)


def route_paths(path):
    """Return both local and Vercel API paths for one endpoint."""
    return [path, f"/api{path}"]


@app.route(route_paths("/"), methods=["GET"])
def health():
    return jsonify({"status": "ok", "message": "English Learning Chatbot API is running!"})


@app.route(route_paths("/chat"), methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    user_message = data.get("message", "").strip()
    context = data.get("context", {})

    if not user_message:
        return jsonify({"type": "error", "text": "Please send a message!"}), 400

    return jsonify(process_message(user_message, context))


@app.route(route_paths("/lessons"), methods=["GET"])
def lessons():
    return jsonify(list_all_lessons())


@app.route(route_paths("/lesson/<lesson_key>"), methods=["GET"])
def lesson(lesson_key):
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


@app.route(route_paths("/quiz/<lesson_key>"), methods=["GET"])
def quiz(lesson_key):
    return jsonify(get_quiz(lesson_key))


if __name__ == "__main__":
    app.run(debug=False, port=5000, host="0.0.0.0")
