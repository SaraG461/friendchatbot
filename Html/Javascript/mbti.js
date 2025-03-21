document.querySelector("form").addEventListener("submit", function (e) {
    e.preventDefault();

    const formData = new FormData(this);
    const answers = {};

    for (let [key, value] of formData.entries()) {
        answers[key] = value;
    }

    
    let E = 0, I = 0, S = 0, N = 0, T = 0, F = 0, J = 0, P = 0;

    const questionMap = {
        E: [57, 64],
        I: [57, 64],
        S: [58, 59, 65],
        N: [58, 59, 65],
        T: [53, 54, 60, 61, 66, 67, 68],
        F: [53, 54, 60, 61, 66, 67, 68],
        J: [55, 56, 62, 63, 69, 70],
        P: [55, 56, 62, 63, 69, 70],
    };

   
    for (let q = 53; q <= 70; q++) {
        const val = answers[`q${q}`];
        if (!val) continue;

        const numVal = parseInt(val);
        if ([57, 64].includes(q)) (numVal === 1 ? E++ : I++);
        if ([58, 59, 65].includes(q)) (numVal === 1 ? S++ : N++);
        if ([53, 54, 60, 61, 66, 67, 68].includes(q)) (numVal === 1 ? T++ : F++);
        if ([55, 56, 62, 63, 69, 70].includes(q)) (numVal === 1 ? J++ : P++);
    }

    const mbti =
        (E >= I ? "E" : "I") +
        (S >= N ? "S" : "N") +
        (T >= F ? "T" : "F") +
        (J >= P ? "J" : "P");

   
    localStorage.setItem("mbti", mbti);
    window.location.href = "mbtiResult.html";
});

