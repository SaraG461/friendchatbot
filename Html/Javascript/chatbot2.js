"use strict";

const inputEl = document.getElementById('userInput');
const btnEl = document.querySelector('.submit-btn');
const personalityEl = document.getElementById('personality');

// DOM elements for both responses
const personalityResponse = document.getElementById("personalityResponse");
const pureResponse = document.getElementById("pureResponse");

btnEl.addEventListener('click', async () => {
    const userMessage = inputEl.value.trim();
    const selectedPersonality = personalityEl.value;

    if (!userMessage || !selectedPersonality) {
        alert("Please enter a message and select a personality type.");
        return;
    }

    // Temporary loading text
    personalityResponse.innerText = "Thinking...";
    pureResponse.innerText = "Thinking...";

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
        personalityResponse.innerText = data.personality_response;
        pureResponse.innerText = data.pure_response;

    } catch (error) {
        console.error("Error:", error);
        personalityResponse.innerText = "Error contacting server.";
        pureResponse.innerText = "Error contacting server.";
    }

    inputEl.value = '';
});
