import React, { useState } from "react";
import "./ChatWidget.css";

export default function ChatWidget() {
  const [open, setOpen] = useState(false);
  const [msgs, setMsgs] = useState([
    { role: "bot", text: "Hi! Tell me what day you want to book and I’ll suggest open slots." },
  ]);
  const [text, setText] = useState("");

  async function send() {
    const msg = text.trim();
    if (!msg) return;

    setMsgs((m) => [...m, { role: "user", text: msg }]);
    setText("");

    const day = new Date(msg).toISOString();

    const res = await fetch("http://localhost:8000/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: msg }),
    });

    const data = await res.json();
    if (!data.slots || data.slots.length === 0) {
      setMsgs((m) => [
        ...m,
        { role: "bot", text: "I’m booked on that day. Try another date like tomorrow or Friday." },
      ]);
      return;
    }

    const pretty = data.slots.map((s, i) => `${i + 1}. ${new Date(s).toLocaleString()}`).join("\n");
    setMsgs((m) => [
      ...m,
      { role: "bot", text: `Here are open slots:\n${pretty}\nReply with the slot number you want.` },
    ]);
  }

  return (
    <>
      <button className="chat-fab" onClick={() => setOpen(!open)}>
        {open ? "×" : "Book"}
      </button>

      {open && (
        <div className="chat-modal">
          <div className="chat-header">Booking Assistant</div>

          <div className="chat-body">
            {msgs.map((m, i) => (
              <div key={i} className={`bubble ${m.role}`}>
                {m.text}
              </div>
            ))}
          </div>

          <div className="chat-input">
            <input
              value={text}
              onChange={(e) => setText(e.target.value)}
              placeholder="Type a date like 2026-01-12..."
              onKeyDown={(e) => e.key === "Enter" && send()}
            />
            <button onClick={send}>Send</button>
          </div>
        </div>
      )}
    </>
  );
}