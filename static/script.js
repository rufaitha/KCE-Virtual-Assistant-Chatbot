const form = document.getElementById("chatForm");
const input = document.getElementById("messageInput");
const messages = document.getElementById("messages");

function timeNow(){
  return new Date().toLocaleTimeString([], {hour:"2-digit", minute:"2-digit"});
}

function addMessage(text, who){
  const wrap = document.createElement("div");
  wrap.className = `message ${who}`;
  const avatar = document.createElement("div");
  avatar.className = "mini-avatar";
  avatar.textContent = who === "bot" ? "K" : "You";
  const bubble = document.createElement("div");
  bubble.className = "bubble";
  bubble.innerHTML = text + `<div class="time">${timeNow()}</div>`;
  wrap.appendChild(avatar);
  wrap.appendChild(bubble);
  messages.appendChild(wrap);
  messages.scrollTop = messages.scrollHeight;
}

async function ask(question){
  if(!question) return;
  addMessage(question, "user");
  input.value = "";
  const typing = document.createElement("div");
  typing.className = "message bot";
  typing.id = "typing";
  typing.innerHTML = `<div class="mini-avatar">K</div><div class="bubble">Typing…</div>`;
  messages.appendChild(typing);
  messages.scrollTop = messages.scrollHeight;

  try{
    const res = await fetch("/chat", {
      method:"POST",
      headers:{"Content-Type":"application/json"},
      body:JSON.stringify({message:question})
    });
    const data = await res.json();
    document.getElementById("typing")?.remove();
    addMessage(data.reply, "bot");
  }catch(e){
    document.getElementById("typing")?.remove();
    addMessage("Sorry, I couldn't connect to the chatbot server. Please try again.", "bot");
  }
}

form.addEventListener("submit", e => {
  e.preventDefault();
  ask(input.value.trim());
});

document.querySelectorAll("[data-question]").forEach(btn => {
  btn.addEventListener("click", () => ask(btn.dataset.question));
});
