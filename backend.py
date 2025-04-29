from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "")
    if not user_message:
        return jsonify({"error": "Empty message"}), 400

    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "Ты дружелюбный советник для людей 40+. Они стесняются начинать общаться поэтому ты всегда задаешь им наводящие вопросы"},
            {"role": "user", "content": user_message}
        ],
        "stream": False
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}"
    }

    response = requests.post("https://api.deepseek.com/chat/completions", json=payload, headers=headers)
    result = response.json()
    reply = result.get("choices", [{}])[0].get("message", {}).get("content", "Нет ответа.")
    return jsonify({"reply": reply})
