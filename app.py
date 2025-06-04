from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv
from flask_cors import CORS
from waitress import serve

load_dotenv()

app = Flask(__name__)
CORS(app, origins=["*"])

API_URL = "https://api.deepseek.com/v1/chat/completions"
API_KEY = os.getenv("DEEPSEEK_API_KEY")


@app.route("/api/chat", methods=["POST"])
def chat():
    try:
        user_msg = request.json.get("message", "")
        if not user_msg:
            return jsonify({"error": "No message provided"}), 400

        payload = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "user", "content": user_msg}
            ]
        }

        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        response = requests.post(API_URL, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()

        reply = data["choices"][0]["message"]["content"]
        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)

