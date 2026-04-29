import { useState } from "react"
import axios from "axios"
import { API, API_KEY } from "../App"

export default function Analyze() {
  const [name, setName] = useState("")
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)

  const handleAnalyze = async () => {
    if (!name.trim()) return
    setLoading(true)
    try {
      const res = await axios.post(`${API}/analyze/`, {
        name,
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
      <p style={{ color: "#666" }}>Enter any person's name. The system will fetch their Wikipedia page and build a behavioural profile.</p>
      <div style={{ display: "flex", gap: 12 }}>
        <input
          value={name}
          onChange={e => setName(e.target.value)}
          placeholder="e.g. Cao Cao, Zhang Juzheng, Alan Turing"
          style={{ flex: 1, padding: 10, fontSize: 14, borderRadius: 8, border: "1px solid #ddd" }}
        />
        <button
          onClick={handleAnalyze}
          disabled={loading}
          style={{ padding: "10px 20px", background: "#1a1a1a", color: "#fff", border: "none", borderRadius: 8, cursor: "pointer" }}
        >
          {loading ? "Analysing..." : "Analyse"}
        </button>
      </div>

      {result && (
        <div style={{ marginTop: 24 }}>
          <h2>{result.name}</h2>
          <h3>Behavioural Vector</h3>
          {["Oppression", "Group", "Principle", "Trust", "Change", "Emotion", "Motivation", "Mission", "Injustice", "Expression"].map((dim, i) => (
            <div key={i} style={{ marginBottom: 8 }}>
              <div style={{ display: "flex", justifyContent: "space-between", fontSize: 13 }}>
                <span>{dim}</span>
                <span style={{ color: "#666" }}>{result.profile.vector[i].toFixed(2)}</span>
              </div>
              <div style={{ background: "#f5f5f5", borderRadius: 4, height: 6, marginTop: 4 }}>
                <div style={{ width: `${result.profile.vector[i] * 100}%`, background: "#6366f1", height: "100%", borderRadius: 4 }} />
              </div>
            </div>
          ))}

          <h3 style={{ marginTop: 24 }}>Closest Matches</h3>
          {result.matches.map((match, i) => (
            <div key={i} style={{ padding: 16, marginBottom: 12, border: "1px solid #eee", borderRadius: 8 }}>
              <div style={{ display: "flex", justifyContent: "space-between" }}>
                <strong>{match.name}</strong>
                <span style={{ color: "#666" }}>{match.era > 0 ? match.era : `${Math.abs(match.era)} BC`}</span>
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