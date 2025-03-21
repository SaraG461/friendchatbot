    const mbti = localStorage.getItem("mbti");

    const descriptions = {
        ISTJ: "Responsible, serious, and traditional. Loves structure and rules.",
        ISFJ: "Kind, quiet, and dependable. Enjoys helping others.",
        INFJ: "Insightful, idealistic, and compassionate. Seeks meaning in everything.",
        INTJ: "Strategic, logical, and forward-thinking. Loves complex ideas.",
        ISTP: "Analytical, practical, and reserved. Enjoys hands-on work.",
        ISFP: "Gentle, sensitive, and artistic. Values beauty and freedom.",
        INFP: "Idealistic, loyal, and thoughtful. Driven by strong values.",
        INTP: "Intellectual, inventive, and curious. Loves abstract thinking.",
        ESTP: "Energetic, action-oriented, and bold. Lives in the moment.",
        ESFP: "Outgoing, friendly, and spontaneous. Loves fun and people.",
        ENFP: "Enthusiastic, creative, and people-centered. Full of ideas.",
        ENTP: "Quick-witted, resourceful, and inventive. Loves challenges.",
        ESTJ: "Organized, practical, and driven. Natural leader.",
        ESFJ: "Warm, organized, and conscientious. Values harmony.",
        ENFJ: "Charismatic, empathetic, and inspiring. Seeks to uplift others.",
        ENTJ: "Confident, strategic, and assertive. Born to lead.",
    };

    document.querySelector(".mbti").textContent = "Your MBTI Type: " + mbti;
    document.querySelector(".description").textContent = descriptions[mbti] || "Description not found.";

    document.getElementById("startBtn").addEventListener("click", () => {
        window.location.href = "chatbot.html";
    });

