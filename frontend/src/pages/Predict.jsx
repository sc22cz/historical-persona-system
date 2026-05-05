import { useState, useEffect } from "react"
import axios from "axios"
import { API } from "../App"

const S = {
  desc: { fontSize: 13, color: "#888", marginBottom: 20, lineHeight: 1.7 },
  saved: { padding: "10px 14px", background: "#f8f8f8", border: "1px solid #e5e5e5", borderRadius: 6, fontSize: 13, color: "#555", marginBottom: 20, display: "flex", justifyContent: "space-between", alignItems: "center" },
  matchCard: { border: "1px solid #e5e5e5", borderRadius: 8, padding: "10px 14px", marginBottom: 8, display: "flex", justifyContent: "space-between", alignItems: "center" },
  name: { fontSize: 14, fontWeight: 600, color: "#111" },
  score: { fontSize: 12, color: "#888" },
  prediction: { whiteSpace: "pre-wrap", lineHeight: 1.9, fontSize: 14, color: "#111", borderLeft: "2px solid #111", paddingLeft: 16, marginTop: 8 },
  err: { padding: "10px 14px", background: "#fafafa", border: "1px solid #e5e5e5", borderRadius: 6, fontSize: 13, color: "#dc2626", marginTop: 16 },
}

export default function Predict() {
  const [description, setDescription] = useState("")
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState("")
  const [savedProfile, setSavedProfile] = useState(null)
  const [usingSaved, setUsingSaved] = useState(false)

  useEffect(() => {
    const raw = localStorage.getItem("hps_profile")
    if (raw) {
      try {
        const p = JSON.parse(raw)
        setSavedProfile(p)
        setDescription(p.description || "")
        setUsingSaved(true)
      } catch {}
    }
  }, [])

  const handlePredict = async () => {
    if (!description.trim()) return
    setLoading(true)
    setError("")
    setResult(null)
    try {
      const res = await axios.post(`${API}/predict/`, { description })
      setResult(res.data)
    } catch (err) {
      setError(err.response?.data?.detail || "Failed. Please try again.")
    }
    setLoading(false)
  }

  const clearSaved = () => {
    setUsingSaved(false)
    setSavedProfile(null)
    setDescription("")
  }

  return (
    <div>
      <h2 style={{ marginBottom: 6 }}>What Would They Tell Me?</h2>
      <p style={S.desc}>
        Describe your decisions, instincts, and patterns. Historical figures who share your behavioural DNA will channel their lived experience to tell you what you need to hear — not what you want to hear.
      </p>

      {savedProfile && usingSaved && (
        <div style={S.saved}>
          <span>Using your saved profile from Match</span>
          <button className="secondary" style={{ fontSize: 12, padding: "4px 10px" }} onClick={clearSaved}>Clear</button>
        </div>
      )}

      <span style={{ fontSize: 12, fontWeight: 600, color: "#888", textTransform: "uppercase", letterSpacing: 1, marginBottom: 6, display: "block" }}>Your description</span>
      <textarea
        value={description}
        onChange={e => { setDescription(e.target.value); setUsingSaved(false) }}
        placeholder="Describe your behaviours, decisions, and patterns…"
        style={{ width: "100%", height: 150, marginBottom: 12 }}
      />
      <button className="primary" onClick={handlePredict} disabled={loading}>
        {loading ? "Channelling…" : "Find My Historical Mirrors"}
      </button>

      {error && <div style={S.err}>{error}</div>}

      {loading && (
        <div style={{ marginTop: 32 }}>
          <div style={{ fontSize: 13, color: "#888", marginBottom: 16 }}>Channelling historical figures…</div>
          {[1,2,3].map(i => (
            <div key={i} style={{ border: "1px solid #e5e5e5", borderRadius: 8, padding: "10px 14px", marginBottom: 8, display: "flex", justifyContent: "space-between" }}>
              <div className="skeleton" style={{ height: 14, width: "35%", borderRadius: 4 }} />
              <div className="skeleton" style={{ height: 12, width: "18%", borderRadius: 4 }} />
            </div>
          ))}
        </div>
      )}

      {result && (
        <div style={{ marginTop: 40 }}>
          <h2 style={{ marginBottom: 16 }}>Your Historical Counterparts</h2>
          {result.matches.map((match, i) => (
            <div key={i} className={`card-hover fade-up fade-up-delay-${i + 1}`} style={S.matchCard}>
              <span style={S.name}>{match.name}</span>
              <span style={S.score}>{(match.score * 100).toFixed(1)}% similar</span>
            </div>
          ))}

          <h2 style={{ marginTop: 32, marginBottom: 12 }}>Their Message to You</h2>
          <div className="fade-up" style={S.prediction}>{result.prediction}</div>
        </div>
      )}
    </div>
  )
}
