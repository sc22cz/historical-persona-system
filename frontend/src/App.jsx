import { useState } from "react"
import axios from "axios"

const API = "http://127.0.0.1:8000"
const API_KEY = "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"

export default function App() {
  const [description, setDescription] = useState("")
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)

  const handleMatch = async () => {
    if (!description.trim()) return
    setLoading(true)
    try {
      const res = await axios.post(`${API}/match/`, {
        description,
        api_key: API_KEY,
        top_k: 3
      })
      setResult(res.data)
    } catch (err) {
      console.error(err)
    }
    setLoading(false)
  }

  return (
    <div style={{ maxWidth: 600, margin: "60px auto", padding: "0 20px", fontFamily: "sans-serif" }}>
      <h1>Historical Persona Match</h1>
      <p style={{ color: "#666" }}>Describe yourself or someone you know. The system will find your historical mirror.</p>
      
      <textarea
        value={description}
        onChange={e => setDescription(e.target.value)}
        placeholder="Describe behaviours, decisions, and patterns..."
        style={{ width: "100%", height: 150, padding: 12, fontSize: 14, borderRadius: 8, border: "1px solid #ddd", boxSizing: "border-box" }}
      />
      
      <button
        onClick={handleMatch}
        disabled={loading}
        style={{ marginTop: 12, padding: "10px 24px", background: "#1a1a1a", color: "#fff", border: "none", borderRadius: 8, cursor: "pointer", fontSize: 14 }}
      >
        {loading ? "Analysing..." : "Find My Historical Mirror"}
      </button>

      {result && (
        <div style={{ marginTop: 32 }}>
          <h2>Your Matches</h2>
          {result.matches.map((match, i) => (
            <div key={i} style={{ padding: 16, marginBottom: 12, border: "1px solid #eee", borderRadius: 8 }}>
              <div style={{ display: "flex", justifyContent: "space-between" }}>
                <strong>{match.name}</strong>
                <span style={{ color: "#666" }}>{match.era > 0 ? match.era : `${Math.abs(match.era)} BC`}</span>
              </div>
              <div style={{ marginTop: 8, background: "#f5f5f5", borderRadius: 4, height: 8 }}>
                <div style={{ width: `${match.score * 100}%`, background: "#1a1a1a", height: "100%", borderRadius: 4 }} />
              </div>
              <div style={{ marginTop: 4, fontSize: 12, color: "#666" }}>
                Similarity: {(match.score * 100).toFixed(1)}%
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}