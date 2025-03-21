"use strict";

const inputEl = document.querySelector('.input-chat');
const btnEl = document.querySelector('.bxs-paper-plane');
const cardBodyEl = document.querySelector('.card-body');

function manageChat() {
    const userMessage = inputEl.value.trim();
    if (!userMessage) return;
    inputEl.value = '';

    cardBodyEl.appendChild(messageEl(userMessage, "user"));

    
    cardBodyEl.scrollTop = cardBodyEl.scrollHeight;

   
    setTimeout(() => {
        cardBodyEl.appendChild(messageEl("Writing....", "chat-bot"));
        cardBodyEl.scrollTop = cardBodyEl.scrollHeight;
    }, 600);
}

function messageEl(message, className) {
    const chatEl = document.createElement('div');
    chatEl.classList.add('chat', className);
    const chatContent =
        className === "chat-bot"
            ? `<span class='user-icon'><i class='bx bxs-heart'></i></span><p>${message}</p>`
            : `<span class='user-icon'><i class='bx bx-user'></i></span><p>${message}</p>`;
    chatEl.innerHTML = chatContent;
    return chatEl;
}

btnEl.addEventListener('click', manageChat);
