"""
Nandha Arts and Science College - Admission Chatbot (Flask Backend)
Run: python3 app.py
Then open http://127.0.0.1:5000 in your browser.
"""
import os
import sqlite3
import uuid
from datetime import datetime

from flask import Flask, render_template, request, jsonify, session

from chatbot.nlp_engine import ChatBot

BASE_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(BASE_DIR, "database", "admission.db")

app = Flask(__name__)
app.secret_key = "college-admission-chatbot-secret-key"  # replace in production

bot = ChatBot()


def log_chat(session_id, user_message, intent, confidence, bot_response):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        """INSERT INTO chat_logs (session_id, user_message, detected_intent, confidence, bot_response, timestamp)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (session_id, user_message, intent, confidence, bot_response, datetime.now().isoformat()),
    )
    conn.commit()
    conn.close()


@app.route("/")
def index():
    if "session_id" not in session:
        session["session_id"] = str(uuid.uuid4())
    return render_template("index.html")


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json(force=True)
    user_message = (data.get("message") or "").strip()

    if not user_message:
        return jsonify({"response": "Please type a question so I can help you.", "intent": "empty", "confidence": 0}), 200

    result = bot.get_response(user_message)
    session_id = session.get("session_id", "anonymous")
    log_chat(session_id, user_message, result["intent"], result["confidence"], result["response"])

    return jsonify(result)


@app.route("/api/quick-topics")
def quick_topics():
    """Suggested quick-reply chips shown in the UI."""
    topics = [
        {"label": "Courses Offered", "message": "What courses do you offer?"},
        {"label": "Fee Structure", "message": "What is the fee structure?"},
        {"label": "Eligibility", "message": "What is the eligibility criteria?"},
        {"label": "Scholarships", "message": "Are there any scholarships?"},
        {"label": "Important Dates", "message": "What are the important dates?"},
        {"label": "Required Documents", "message": "What documents are required?"},
        {"label": "Hostel Facility", "message": "Is hostel facility available?"},
        {"label": "Placements", "message": "What about placements?"},
    ]
    return jsonify(topics)


@app.route("/api/stats")
def stats():
    """Simple admin-style stats endpoint: total queries + top intents."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) AS total FROM chat_logs")
    total = cur.fetchone()["total"]
    cur.execute(
        "SELECT detected_intent, COUNT(*) AS c FROM chat_logs GROUP BY detected_intent ORDER BY c DESC LIMIT 5"
    )
    top_intents = [dict(row) for row in cur.fetchall()]
    conn.close()
    return jsonify({"total_queries": total, "top_intents": top_intents})


if __name__ == "__main__":
    if not os.path.exists(DB_PATH):
        from database.db_setup import create_and_seed
        create_and_seed()
    app.run(debug=False, host="0.0.0.0", port=5000)
