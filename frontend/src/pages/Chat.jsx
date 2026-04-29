import { useState } from "react"
import axios from "axios"
import { API, API_KEY } from "../App"

export default function Chat() {
  const [name, setName] = useState("")
  const [message, setMessage] = useState("")
  const [history, setHistory] = useState([])
  const [loading, setLoading] = useState(false)

  const handleSend = async () => {
    if (!name.trim() || !message.trim()) return
    setLoading(true)
    const userMessage = message
    setMessage("")
    setHistory(h => [...h, { role: "user", text: userMessage }])
    try {
      const res = await axios.post(`${API}/chat/`, {
        name,
        message: userMessage,
        api_key: API_KEY
      })
      setHistory(h => [...h, { role: "figure", text: res.data.response, figure: res.data.figure }])
    } catch (err) {
      console.error(err)
    }
    setLoading(false)
  }

  return (
    <div>
      <p style={{ color: "#666" }}>Enter a historical figure's name and start a conversation.</p>
      <input
        value={name}
        onChange={e => setName(e.target.value)}
        placeholder="e.g. Napoleon Bonaparte"
        style={{ width: "100%", padding: 10, fontSize: 14, borderRadius: 8, border: "1px solid #ddd", boxSizing: "border-box", marginBottom: 16 }}
      />

      <div style={{ minHeight: 300, border: "1px solid #eee", borderRadius: 8, padding: 16, marginBottom: 16, background: "#fafafa" }}>
        {history.length === 0 && (
          <p style={{ color: "#ccc", textAlign: "center", marginTop: 100 }}>Your conversation will appear here</p>
        )}
        {history.map((msg, i) => (
          <div key={i} style={{ marginBottom: 16, textAlign: msg.role === "user" ? "right" : "left" }}>
            <div style={{
              display: "inline-block",
              maxWidth: "80%",
              padding: "10px 14px",
              borderRadius: 8,
              background: msg.role === "user" ? "#1a1a1a" : "#fff",
              color: msg.role === "user" ? "#fff" : "#1a1a1a",
              border: msg.role === "figure" ? "1px solid #eee" : "none",
              fontSize: 14,
              lineHeight: 1.6,
              textAlign: "left"
            }}>
              {msg.role === "figure" && <div style={{ fontSize: 11, color: "#999", marginBottom: 4 }}>{msg.figure}</div>}
              {msg.text}
            </div>
          </div>
        ))}
      </div>

      <div style={{ display: "flex", gap: 12 }}>
        <input
          value={message}
          onChange={e => setMessage(e.target.value)}
          onKeyDown={e => e.key === "Enter" && handleSend()}
          placeholder="Ask a question..."
          style={{ flex: 1, padding: 10, fontSize: 14, borderRadius: 8, border: "1px solid #ddd" }}
        />
        <button
          onClick={handleSend}
          disabled={loading}
          style={{ padding: "10px 20px", background: "#1a1a1a", color: "#fff", border: "none", borderRadius: 8, cursor: "pointer" }}
        >
          {loading ? "..." : "Send"}
        </button>
      </div>
    </div>
  )
}