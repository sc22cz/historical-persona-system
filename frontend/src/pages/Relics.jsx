import { useState } from "react"
import axios from "axios"
import { API, API_KEY } from "../App"

export default function Relics() {
  const [description, setDescription] = useState("")
  const [material, setMaterial] = useState("")
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)

  const handleMatch = async () => {
    if (!description.trim()) return
    setLoading(true)
    try {
      const res = await axios.post(`${API}/relics/match/`, {
        description,
        material,
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
      <p style={{ color: "#666" }}>Describe a relic or artefact. The system will match it to historical figures with similar behavioural profiles.</p>
      
      <input
        value={material}
        onChange={e => setMaterial(e.target.value)}
        placeholder="Material (e.g. bronze, jade, iron)"
        style={{ width: "100%", padding: 10, fontSize: 14, borderRadius: 8, border: "1px solid #ddd", boxSizing: "border-box", marginBottom: 12 }}
      />
      <textarea
        value={description}
        onChange={e => setDescription(e.target.value)}
        placeholder="Describe the relic (e.g. a heavy bronze sword with military engravings...)"
        style={{ width: "100%", height: 120, padding: 12, fontSize: 14, borderRadius: 8, border: "1px solid #ddd", boxSizing: "border-box" }}
      />
      <button
        onClick={handleMatch}
        disabled={loading}
        style={{ marginTop: 12, padding: "10px 24px", background: "#1a1a1a", color: "#fff", border: "none", borderRadius: 8, cursor: "pointer", fontSize: 14 }}
      >
        {loading ? "Analysing..." : "Match Relic"}
      </button>

      {result && (
        <div style={{ marginTop: 32 }}>
          <h2>Relic Analysis</h2>
          <p style={{ fontSize: 14, color: "#555", lineHeight: 1.6 }}>{result.relic_profile.reasoning}</p>
          <h2 style={{ marginTop: 24 }}>Closest Historical Matches</h2>
          {result.matches.map((match, i) => (
            <div key={i} style={{ padding: 16, marginBottom: 12, border: "1px solid #eee", borderRadius: 8 }}>
              <div style={{ display: "flex", justifyContent: "space-between" }}>
                <strong>{match.name}</strong>
                <span style={{ color: "#666" }}>{match.era > 0 ? match.era : `${Math.abs(match.era)} BC`}</span>
              </div>
              <div style={{ marginTop: 8, background: "#f5f5f5", borderRadius: 4, height: 6 }}>
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