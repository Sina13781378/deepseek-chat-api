from flask import Flask, request, jsonify
from flask_cors import CORS
from waitress import serve
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# بارگذاری کلید Gemini از فایل .env
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

# بارگذاری مدل
model = genai.GenerativeModel("gemini-1.5-flash")

# خواندن محتوای فایل متنی
def load_flat_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except Exception as e:
        return f"خطا در خواندن فایل: {str(e)}"

@app.route("/api/chat", methods=["POST"])
def chat():
    try:
        user_msg = request.json.get("message", "")
        if not user_msg:
            return jsonify({"error": "No message provided"}), 400

        # خواندن داده‌ها از فایل فلت
        flat_data = load_flat_file("Sefareshat Khareji.txt")

        prompt = f"""
        اطلاعات سفارشات خارجی شرکت در ادامه آمده است:

        {flat_data}

        لطفاً فقط بر اساس اطلاعات بالا به این پرسش پاسخ بده:
        {user_msg}
        """

        response = model.generate_content(prompt)
        return jsonify({"reply": response.text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
