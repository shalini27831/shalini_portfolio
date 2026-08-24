import streamlit as st
import os
import requests
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="Shalini G | AI Portfolio",
    page_icon="🤖",
    layout="wide"
)

# Load portfolio knowledge
with open("knowledge.txt", "r", encoding="utf-8") as file:
    knowledge = file.read()

# ---------- PORTFOLIO ----------

st.title("Shalini G")
st.subheader("AI / ML Developer | Python | RAG")

st.write(
    "Welcome to my portfolio. Explore my skills, projects, "
    "experience and resume."
)

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.header("👩 About Me")
    st.write(
        "I am Shalini G, passionate about Artificial Intelligence, "
        "Machine Learning, Python and RAG applications."
    )

with col2:
    st.header("🛠️ Skills")
    st.write(
        "Python • Machine Learning • Artificial Intelligence • "
        "RAG • Gemini API • HTML • CSS • JavaScript"
    )

st.divider()

st.header("💼 Projects")
st.write(
    "My projects and portfolio work are available in my "
    "portfolio and resume."
)

st.divider()

st.header("📄 Resume")

with open("Shalini_G_Resume.pdf", "rb") as pdf_file:
    st.download_button(
        label="Download Resume",
        data=pdf_file,
        file_name="Shalini_G_Resume.pdf",
        mime="application/pdf"
    )

st.divider()

# ---------- RAG CHATBOT ----------

st.header("🤖 Ask Shalini")

st.write(
    "Ask questions about my skills, projects, education, "
    "experience and portfolio."
)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

user_input = st.chat_input("Ask something about Shalini...")

if user_input:

    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.write(user_input)

    api_key = os.getenv("GEMINI_API_KEY")

    prompt = f"""
You are Shalini's AI portfolio assistant.

Answer using ONLY the information in the resume
and portfolio knowledge below.

If the information is not available, say:
"I don't have that information in Shalini's resume or portfolio."

===== KNOWLEDGE =====
{knowledge}

===== QUESTION =====
{user_input}
"""

    url = (
        "https://generativelanguage.googleapis.com/"
        "v1beta/models/gemini-3.6-flash:generateContent"
    )

    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": api_key
    }

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

    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            response = requests.post(
                url,
                headers=headers,
                json=data
            )

            if response.status_code == 200:

                result = response.json()

                answer = (
                    result["candidates"][0]
                    ["content"]["parts"][0]["text"]
                )

                st.write(answer)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })

            else:
                st.error(
                    f"Gemini API error: {response.status_code}"
                )