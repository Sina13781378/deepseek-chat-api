from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
from flask_cors import CORS
from waitress import serve
import google.generativeai as genai
import pandas as pd

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")

# Load Excel data once at startup
try:
    df = pd.read_excel("Sefareshat Khareji.xlsx")
    excel_context = df.to_string(index=False)
except Exception as e:
    excel_context = "Failed to load Excel data: " + str(e)

@app.route("/api/chat", methods=["POST"])
def chat():
    try:
        user_msg = request.json.get("message", "")
        if not user_msg:
            return jsonify({"error": "No message provided"}), 400

        full_prompt = (
            "You are an assistant that answers questions based on this dataset:\n"
            + excel_context +
            "\n\nUser question: " + user_msg
        )

        response = model.generate_content(full_prompt)
        return jsonify({"reply": response.text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
