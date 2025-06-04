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

        # بررسی وجود کلیدها
        if "choices" not in data or not data["choices"]:
            return jsonify({"error": "Invalid API response format (no choices)"}), 500

        print("DeepSeek Response JSON:", data)

        print("✅ Full Response:", data)  # لاگ گرفتن کامل
        reply = data.get("choices", [{}])[0].get("message", {}).get("content", "")
        if not reply:
            return jsonify({"error": "❌ Unexpected format. No reply found."}), 500
        return jsonify({"reply": reply})

        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
