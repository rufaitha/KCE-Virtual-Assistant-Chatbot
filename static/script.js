const form = document.getElementById("chatForm");
const input = document.getElementById("messageInput");
const messages = document.getElementById("messages");


// ===============================
// CURRENT TIME
// ===============================

function timeNow() {
    return new Date().toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit"
    });
}


// ===============================
// ADD MESSAGE
// ===============================

function addMessage(text, who) {

    const wrap = document.createElement("div");
    wrap.className = `message ${who}`;

    const avatar = document.createElement("div");
    avatar.className = "mini-avatar";
    avatar.textContent = who === "bot" ? "K" : "You";

    const bubble = document.createElement("div");
    bubble.className = "bubble";

    // Bot responses can contain HTML such as <b>, <ul>, <a>
    bubble.innerHTML =
        text +
        `<div class="time">${timeNow()}</div>`;

    wrap.appendChild(avatar);
    wrap.appendChild(bubble);

    messages.appendChild(wrap);

    // Automatically scroll to newest message
    messages.scrollTop = messages.scrollHeight;
}


// ===============================
// TYPING INDICATOR
// ===============================

function showTyping() {

    const typing = document.createElement("div");

    typing.className = "message bot";
    typing.id = "typing";

    typing.innerHTML = `
        <div class="mini-avatar">K</div>
        <div class="bubble">
            <span>Typing...</span>
        </div>
    `;

    messages.appendChild(typing);

    messages.scrollTop = messages.scrollHeight;
}


// ===============================
// REMOVE TYPING INDICATOR
// ===============================

function removeTyping() {

    const typing = document.getElementById("typing");

    if (typing) {
        typing.remove();
    }
}


// ===============================
// ASK CHATBOT
// ===============================

async function ask(question) {

    question = question.trim();

    // Don't send empty messages
    if (!question) {
        return;
    }

    // Show user's message
    addMessage(question, "user");

    // Clear input
    input.value = "";

    // Disable input while waiting
    input.disabled = true;

    showTyping();

    try {

        const response = await fetch("/chat", {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                message: question
            })
        });


        // Check server response
        if (!response.ok) {
            throw new Error("Server error");
        }


        const data = await response.json();

        removeTyping();


        // Display chatbot response
        if (data.reply) {

            addMessage(data.reply, "bot");

        } else {

            addMessage(
                "Sorry, I couldn't find an answer. Please try asking another question about KCE.",
                "bot"
            );

        }

    } catch (error) {

        removeTyping();

        addMessage(
            "Sorry, I couldn't connect to the KCE chatbot server. Please try again.",
            "bot"
        );

        console.error("Chatbot error:", error);

    } finally {

        // Enable input again
        input.disabled = false;

        input.focus();
    }
}


// ===============================
// FORM SUBMIT
// ===============================

form.addEventListener("submit", function (event) {

    event.preventDefault();

    ask(input.value);

});


// ===============================
// QUICK QUESTION BUTTONS
// ===============================

document.querySelectorAll("[data-question]").forEach(function (button) {

    button.addEventListener("click", function () {

        const question = button.dataset.question;

        if (question) {
            ask(question);
        }

    });

});


// ===============================
// ENTER KEY
// ===============================

input.addEventListener("keydown", function (event) {

    if (event.key === "Enter") {

        event.preventDefault();

        form.requestSubmit();

    }

});


// ===============================
// INITIAL FOCUS
// ===============================

window.addEventListener("load", function () {

    input.focus();

});
