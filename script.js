const chatButton = document.getElementById("chatButton");
const chatWindow = document.getElementById("chatWindow");
const closeChat = document.getElementById("closeChat");
const sendMessage = document.getElementById("sendMessage");
const chatInput = document.getElementById("chatInput");
const chatMessages = document.getElementById("chatMessages");

chatButton.addEventListener("click", () => {
  chatWindow.style.display = "flex";
  chatInput.focus();
});

closeChat.addEventListener("click", () => {
  chatWindow.style.display = "none";
});

async function sendChatMessage() {
  const message = chatInput.value.trim();

  if (!message) return;

  chatMessages.innerHTML += `
    <div class="user-message">${message}</div>
  `;

  chatInput.value = "";

  chatMessages.innerHTML += `
    <div class="bot-message" id="typing">Thinking...</div>
  `;

  try {
    const response = await fetch("/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        message: message
      })
    });

    const data = await response.json();

    document.getElementById("typing").remove();

    if (data.answer) {
      chatMessages.innerHTML += `
        <div class="bot-message">${data.answer}</div>
      `;
    } else {
      chatMessages.innerHTML += `
        <div class="bot-message">Sorry, something went wrong.</div>
      `;
    }

  } catch (error) {
    document.getElementById("typing").remove();

    chatMessages.innerHTML += `
      <div class="bot-message">
        Unable to connect to the chatbot.
      </div>
    `;

    console.error(error);
  }

  chatMessages.scrollTop = chatMessages.scrollHeight;
}

sendMessage.addEventListener("click", sendChatMessage);

chatInput.addEventListener("keypress", (event) => {
  if (event.key === "Enter") {
    sendChatMessage();
  }
});
