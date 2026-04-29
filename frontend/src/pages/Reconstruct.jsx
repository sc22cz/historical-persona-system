import { useState } from "react"
import axios from "axios"
import { API, API_KEY } from "../App"

export default function Reconstruct() {
  const [name, setName] = useState("")
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)

  const handleReconstruct = async () => {
    if (!name.trim()) return
    setLoading(true)
    try {
      const res = await axios.post(`${API}/reconstruct/`, {
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
      <p style={{ color: "#666" }}>Enter a historical figure. The system will reconstruct their missing behavioural history based on similar modern figures.</p>
      <div style={{ display: "flex", gap: 12 }}>
        <input
          value={name}
          onChange={e => setName(e.target.value)}
          placeholder="e.g. Hammurabi, Qin Shi Huang"
          style={{ flex: 1, padding: 10, fontSize: 14, borderRadius: 8, border: "1px solid #ddd" }}
        />
        <button
          onClick={handleReconstruct}
          disabled={loading}
          style={{ padding: "10px 20px", background: "#1a1a1a", color: "#fff", border: "none", borderRadius: 8, cursor: "pointer" }}
        >
          {loading ? "Reconstructing..." : "Reconstruct"}
        </button>
      </div>

      {result && (
        <div style={{ marginTop: 32 }}>
          <h2>{result.name}</h2>
          {result.similar_figure && (
            <p style={{ color: "#666", fontSize: 14 }}>Profile imputed from: <strong>{result.similar_figure}</strong></p>
          )}
          <div style={{ whiteSpace: "pre-wrap", lineHeight: 1.8, fontSize: 14, color: "#333", marginTop: 16 }}>
            {result.reconstruction}
          </div>
        </div>
      )}
    </div>
  )
}