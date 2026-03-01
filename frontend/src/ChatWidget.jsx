import React, { useState } from "react";
import "./ChatWidget.css";

export default function ChatWidget() {
  const [text, setText] = useState("");
  const [msgs, setMsgs] = useState([
    {
        role: "assistant",
        text: "Hi! Enter a date (YYYY-MM-DD) and I'll show available slots."
      }
  ]);

  const send = async () => {
    const msg = text.trim();
    if (!msg) return;

    setMsgs((m) => [...m, { role: "user", text: msg }]);
    setText("");

    const res = await fetch("http://localhost:8000/availability", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ day_iso: msg }),
    });

    const data = await res.json();

    if (data.slots) {
      setMsgs((m) => [
        ...m,
        { role: "assistant", text: data.slots.join("\n") },
      ]);
    }
  };

  return (
    <div className="chat-container">
      <div className="chat-messages">
        {msgs.map((m, i) => (
          <div key={i} className={`message ${m.role}`}>
            {m.text}
          </div>
        ))}
      </div>

      <div className="chat-input">
        <input
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Enter date like 2026-03-05"
        />
        <button onClick={send}>Send</button>
      </div>
    </div>
  );
}