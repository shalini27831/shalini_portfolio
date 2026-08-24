import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("API key not found")
    exit()

# Load resume + portfolio knowledge
with open("knowledge.txt", "r", encoding="utf-8") as file:
    knowledge = file.read()

print("API key found!")
print("🤖 Shalini's Portfolio Chatbot")
print("Ask questions about Shalini's resume and portfolio.")
print("Type 'exit' to stop.\n")

url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.6-flash:generateContent"

headers = {
    "Content-Type": "application/json",
    "x-goog-api-key": api_key
}

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("Goodbye!")
        break

    prompt = f"""
You are Shalini's portfolio assistant.

Answer the user's question using ONLY the information
provided in the resume and portfolio below.

If the answer is not available in the information,
say: "I don't have that information in Shalini's resume or portfolio."

===== KNOWLEDGE =====
{knowledge}

===== USER QUESTION =====
{user_input}
"""

    data = {
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
        json=data
    )

    if response.status_code == 200:
        result = response.json()
        answer = result["candidates"][0]["content"]["parts"][0]["text"]
        print("\nBot:", answer)
        print()
    else:
        print("Error:", response.status_code)
        print(response.text)