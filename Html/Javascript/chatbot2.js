"use strict";

const inputEl = document.getElementById('userInput');
const btnEl = document.querySelector('.submit-btn');
const responseEl = document.getElementById('chatbotResponse');
const personalityEl = document.getElementById('personality');

btnEl.addEventListener('click', async () => {
    const userMessage = inputEl.value.trim();
    const selectedPersonality = personalityEl.value;

    if (!userMessage || !selectedPersonality) {
        alert("Please enter a message and select a personality type.");
        return;
    }

    responseEl.innerHTML = `<strong>You:</strong> ${userMessage}<br><em>Chatbot is thinking...</em>`;

    try {
        const res = await fetch("http://127.0.0.1:5000/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                message: userMessage,
                personality: selectedPersonality
            })
        });

        const data = await res.json();
        responseEl.innerHTML = `<strong>Chatbot:</strong> ${data.response}`;

    } catch (error) {
        console.error("Error:", error);
        responseEl.innerHTML = `<strong>Error:</strong> Failed to connect to chatbot server. Is Python running?`;
    }

    inputEl.value = '';
});
