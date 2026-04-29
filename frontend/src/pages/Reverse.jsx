import { useState } from "react"
import axios from "axios"
import { API } from "../App"

export default function Reverse() {
  const [name, setName] = useState("")
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)

  const handleSearch = async () => {
    if (!name.trim()) return
    setLoading(true)
    try {
      const res = await axios.get(`${API}/reverse/${encodeURIComponent(name)}?top_k=5`)
      setResult(res.data)
    } catch (err) {
      console.error(err)
    }
    setLoading(false)
  }

  return (
    <div>
      <p style={{ color: "#666" }}>Enter a historical figure to find their cross-civilisation equivalents.</p>
      <div style={{ display: "flex", gap: 12 }}>
        <input
          value={name}
          onChange={e => setName(e.target.value)}
          placeholder="e.g. Napoleon Bonaparte"
          style={{ flex: 1, padding: 10, fontSize: 14, borderRadius: 8, border: "1px solid #ddd" }}
        />
        <button
          onClick={handleSearch}
          disabled={loading}
          style={{ padding: "10px 20px", background: "#1a1a1a", color: "#fff", border: "none", borderRadius: 8, cursor: "pointer" }}
        >
          {loading ? "Searching..." : "Search"}
        </button>
      </div>

      {result && (
        <div style={{ marginTop: 24 }}>
          <h2>Similar to {result.query}</h2>
          {result.matches.map((match, i) => (
            <div key={i} style={{ padding: 16, marginBottom: 12, border: "1px solid #eee", borderRadius: 8 }}>
              <div style={{ display: "flex", justifyContent: "space-between" }}>
                <strong>{match.name}</strong>
                <span style={{ color: "#666" }}>{match.era > 0 ? match.era : `${Math.abs(match.era)} BC`}</span>
              </div>
              <div style={{ marginTop: 8, background: "#f5f5f5", borderRadius: 4, height: 8 }}>
                <div style={{ width: `${match.score * 100}%`, background: "#6366f1", height: "100%", borderRadius: 4 }} />
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