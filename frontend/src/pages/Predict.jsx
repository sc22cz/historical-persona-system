import { useState } from "react"
import axios from "axios"
import { API, API_KEY } from "../App"

export default function Predict() {
  const [description, setDescription] = useState("")
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)

  const handlePredict = async () => {
    if (!description.trim()) return
    setLoading(true)
    try {
      const res = await axios.post(`${API}/predict/`, {
        description,
        api_key: API_KEY
      })
      setResult(res.data)
    } catch (err) {
      console.error(err)
    }
    setLoading(false)
  }

  return (
    <div>
      <p style={{ color: "#666" }}>Describe yourself. The system will match you to historical figures and predict your likely life trajectory.</p>
      <textarea
        value={description}
        onChange={e => setDescription(e.target.value)}
        placeholder="Describe your behaviours, decisions, and patterns..."
        style={{ width: "100%", height: 150, padding: 12, fontSize: 14, borderRadius: 8, border: "1px solid #ddd", boxSizing: "border-box" }}
      />
      <button
        onClick={handlePredict}
        disabled={loading}
        style={{ marginTop: 12, padding: "10px 24px", background: "#1a1a1a", color: "#fff", border: "none", borderRadius: 8, cursor: "pointer", fontSize: 14 }}
      >
        {loading ? "Analysing..." : "Predict My Future"}
      </button>

      {result && (
        <div style={{ marginTop: 32 }}>
          <h2>Historical Matches</h2>
          {result.matches.map((match, i) => (
            <div key={i} style={{ padding: 12, marginBottom: 8, border: "1px solid #eee", borderRadius: 8, display: "flex", justifyContent: "space-between" }}>
              <strong>{match.name}</strong>
              <span style={{ color: "#666" }}>{(match.score * 100).toFixed(1)}% similar</span>
            </div>
          ))}
          <h2 style={{ marginTop: 32 }}>Your Prediction</h2>
          <div style={{ whiteSpace: "pre-wrap", lineHeight: 1.8, fontSize: 14, color: "#333" }}>
            {result.prediction}
          </div>
        </div>
      )}
    </div>
  )
}