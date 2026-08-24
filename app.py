from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

api_key = os.getenv("GEMINI_API_KEY")

with open("knowledge.txt", "r", encoding="utf-8") as file:
    knowledge = file.read()


@app.route("/")
def home():
    return send_from_directory(".", "index.html")


@app.route("/<path:filename>")
def static_files(filename):
    return send_from_directory(".", filename)


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("message", "")

    prompt = f"""
You are Shalini's portfolio AI assistant.

Answer the question using ONLY the information
in the resume and portfolio below.

If the information is not available, say:
"I don't have that information in Shalini's resume or portfolio."

===== RESUME + PORTFOLIO =====
{knowledge}

===== QUESTION =====
{user_input}
"""

    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.6-flash:generateContent"

    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": api_key
    }

    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ]
    }

    response = requests.post(
        url,
        headers=headers,
        json=payload
    )

    if response.status_code == 200:
        result = response.json()
        answer = result["candidates"][0]["content"]["parts"][0]["text"]
        return jsonify({"answer": answer})

    return jsonify({
        "error": "Gemini API error",
        "details": response.text
    }), response.status_code


if __name__ == "__main__":
    app.run(debug=True)