from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv
from flask_cors import CORS
from waitress import serve

load_dotenv()
app = Flask(__name__)
CORS(app, origins=["https://commercial-documents-analysis.ir"])

API_URL = "https://api.deepseek.com/v1/chat/completions"
API_KEY = os.getenv("DEEPSEEK_API_KEY")

@app.route("/api/chat", methods=["POST"])
def chat():
    user_msg = request.json.get("message", "")
    payload = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": user_msg}]
    }
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(API_URL, json=payload, headers=headers)
        reply = response.json()['choices'][0]['message']['content']
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

