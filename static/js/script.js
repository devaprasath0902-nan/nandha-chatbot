// Nandha Arts and Science College — Admission Chatbot frontend logic

const chatThread = document.getElementById("chat-thread");
const composer = document.getElementById("composer");
const input = document.getElementById("message-input");
const typingRow = document.getElementById("typing-row");
const topicTabsEl = document.getElementById("topic-tabs");

function timeNow() {
  return new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
}

function stampCode(intent) {
  // short reference code reminiscent of an office stamp / ticket number
  const map = {
    courses_offered: "CRS",
    eligibility_criteria: "ELG",
    fee_structure: "FEE",
    scholarship: "SCH",
    admission_process: "APP",
    important_dates: "DTE",
    required_documents: "DOC",
    hostel_facility: "HST",
    placement_info: "PLC",
    greeting: "HLO",
    goodbye: "BYE",
    thanks: "THX",
    fallback: "N/A",
  };
  return map[intent] || "INF";
}

function appendMessage(role, text, meta) {
  const row = document.createElement("div");
  row.className = `msg-row ${role}`;

  if (role === "bot") {
    const stamp = document.createElement("div");
    stamp.className = "stamp-badge";
    stamp.textContent = meta && meta.intent ? stampCode(meta.intent) : "INF";
    row.appendChild(stamp);
  }

  const col = document.createElement("div");

  const bubble = document.createElement("div");
  bubble.className = "bubble";
  bubble.textContent = text;
  col.appendChild(bubble);

  const metaEl = document.createElement("div");
  metaEl.className = "msg-meta";
  metaEl.textContent = role === "bot"
    ? `${timeNow()} · ref ${stampCode(meta && meta.intent)}-${Math.floor(1000 + Math.random() * 9000)}`
    : timeNow();
  col.appendChild(metaEl);

  row.appendChild(col);
  chatThread.appendChild(row);
  chatThread.scrollTop = chatThread.scrollHeight;
}

async function sendMessage(text) {
  if (!text.trim()) return;
  appendMessage("user", text);
  input.value = "";
  typingRow.hidden = false;
  chatThread.scrollTop = chatThread.scrollHeight;

  try {
    const res = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: text }),
    });
    const data = await res.json();
    typingRow.hidden = true;
    appendMessage("bot", data.response, { intent: data.intent });
  } catch (err) {
    typingRow.hidden = true;
    appendMessage("bot", "Sorry, I'm having trouble connecting right now. Please try again in a moment.", { intent: "fallback" });
  }
}

composer.addEventListener("submit", (e) => {
  e.preventDefault();
  sendMessage(input.value);
});

async function loadTopics() {
  try {
    const res = await fetch("/api/quick-topics");
    const topics = await res.json();
    topicTabsEl.innerHTML = "";
    topics.forEach((t) => {
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "topic-tab";
      btn.textContent = t.label;
      btn.addEventListener("click", () => sendMessage(t.message));
      topicTabsEl.appendChild(btn);
    });
  } catch (err) {
    topicTabsEl.innerHTML = "<p style='font-size:12px;color:#5B5749;'>Topics unavailable.</p>";
  }
}

// initial greeting + topics
window.addEventListener("DOMContentLoaded", () => {
  loadTopics();
  appendMessage(
    "bot",
    "Hello! Welcome to the Nandha Arts and Science College Admission Enquiry Desk. I can help with courses, fees, eligibility, scholarships, hostel, placements, documents, and important dates. What would you like to know?",
    { intent: "greeting" }
  );
  input.focus();
});
