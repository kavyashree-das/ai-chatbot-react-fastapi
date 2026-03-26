import { useState, useRef, useEffect } from "react";
import "./chat.css";
import ReactMarkDdown from "react-markdown";

function App() {
  const [message, setMessage] = useState("");
  const [chat, setChat] = useState([]);
  const [loading, setLoading] = useState(false);

  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [chat]);

  const sendMessage = async () => {
    if (!message.trim()) return;

    const userMsg = { role: "user", text: message };

    setChat((prev) => [...prev, userMsg]);
    setMessage("");
    setLoading(true);

    try {
      const res = await fetch("http://127.0.0.1:8000/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ message }),
      });

      const data = await res.json();

      const aiMsg = { role: "ai", text: data.response };

      setChat((prev) => [...prev, aiMsg]);
    } catch (err) {
      setChat((prev) => [
        ...prev,
        { role: "ai", text: "Server error." },
      ]);
    }

    setLoading(false);
  };

  return (
    <div className="container">
      <div className="chat-container">
        <h1 className="title">AI Assistant</h1>

        <div className="messages">
          {chat.map((msg, i) => (
            <div
              key={i}
              className={
                msg.role === "user" ? "message user" : "message ai"
              }
            >
              <ReactMarkDdown
              components={{
                  p: ({children }) => <p style={{ marginBottom: "10px" }} >{children} </p>
                  }}>
              {msg.text}
              </ReactMarkDdown>
            </div>
          ))}

          {loading && <div className="message ai">Thinking...</div>}

          <div ref={bottomRef}></div>
        </div>

        <div className="input-area">
          <input
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder="Ask anything..."
          />

          <button onClick={sendMessage}>Send</button>
        </div>
      </div>
    </div>
  );
}

export default App;