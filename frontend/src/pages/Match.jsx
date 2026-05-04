import { useState } from "react"
import axios from "axios"
import { Radar, RadarChart, PolarGrid, PolarAngleAxis, ResponsiveContainer } from "recharts"
import { API } from "../App"

const DIMS = ["Oppression", "Group", "Principle", "Trust", "Change", "Emotion", "Motivation", "Mission", "Injustice", "Expression"]

const S = {
  label: { fontSize: 12, fontWeight: 600, color: "#888", textTransform: "uppercase", letterSpacing: 1, marginBottom: 6, display: "block" },
  desc: { fontSize: 13, color: "#888", marginBottom: 24, lineHeight: 1.7 },
  card: { border: "1px solid #e5e5e5", borderRadius: 8, padding: 16, marginBottom: 10 },
  row: { display: "flex", justifyContent: "space-between", alignItems: "center" },
  name: { fontSize: 15, fontWeight: 600, color: "#111" },
  era: { fontSize: 12, color: "#888" },
  bar: { background: "#f0f0f0", borderRadius: 3, height: 5, marginTop: 10 },
  fill: (pct) => ({ width: `${pct}%`, background: "#111", height: "100%", borderRadius: 3 }),
  sim: { fontSize: 12, color: "#888", marginTop: 6 },
  saved: { padding: "10px 14px", background: "#f8f8f8", border: "1px solid #e5e5e5", borderRadius: 6, fontSize: 13, color: "#555", marginTop: 24 },
  err: { padding: "10px 14px", background: "#fafafa", border: "1px solid #e5e5e5", borderRadius: 6, fontSize: 13, color: "#dc2626", marginTop: 16 },
}

export default function Match() {
  const [description, setDescription] = useState("")
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState("")

  const handleMatch = async () => {
    if (!description.trim()) return
    setLoading(true)
    setError("")
    setResult(null)
    try {
      const res = await axios.post(`${API}/match/`, { description, top_k: 5 })
      if (!res.data.matches?.length) {
        setError("No matches found. Go to Figures and add historical figures to the database first.")
      } else {
        setResult(res.data)
        localStorage.setItem("hps_profile", JSON.stringify({
          vector: res.data.user_profile.vector,
          description,
          timestamp: Date.now()
        }))
      }
    } catch (err) {
      setError(err.response?.data?.detail || "Analysis failed. Please try again.")
    }
    setLoading(false)
  }

  const radarData = result ? DIMS.map((dim, i) => ({ dimension: dim, value: result.user_profile.vector[i] })) : []

  return (
    <div>
      <h2 style={{ marginBottom: 6 }}>Find Your Historical Mirror</h2>
      <p style={S.desc}>Describe your decisions, instincts, and patterns. The system builds your 10-dimensional behavioural profile and matches you to historical figures in the database.</p>

      <span style={S.label}>Your description</span>
      <textarea
        value={description}
        onChange={e => setDescription(e.target.value)}
        placeholder="e.g. I act on instinct rather than planning. I resist authority when I believe it's unjust, but I need people around me. I'm driven by a sense of larger purpose..."
        style={{ width: "100%", height: 140, marginBottom: 12 }}
      />
      <button className="primary" onClick={handleMatch} disabled={loading}>
        {loading ? "Analysing…" : "Find My Historical Mirror"}
      </button>

      {error && <div style={S.err}>{error}</div>}

      {result && (
        <div style={{ marginTop: 40 }}>
          <h2 style={{ marginBottom: 20 }}>Your Behavioural Profile</h2>
          <ResponsiveContainer width="100%" height={280}>
            <RadarChart data={radarData}>
              <PolarGrid stroke="#e5e5e5" />
              <PolarAngleAxis dataKey="dimension" tick={{ fontSize: 11, fill: "#888" }} />
              <Radar dataKey="value" stroke="#111" fill="#111" fillOpacity={0.15} strokeWidth={1.5} />
            </RadarChart>
          </ResponsiveContainer>

          <h2 style={{ marginTop: 32, marginBottom: 16 }}>Historical Matches</h2>
          {result.matches.map((m, i) => (
            <div key={i} style={S.card}>
              <div style={S.row}>
                <span style={S.name}>{m.name}</span>
                <span style={S.era}>{m.era < 0 ? `${Math.abs(m.era)} BC` : `${m.era} AD`}</span>
              </div>
              <div style={S.bar}><div style={S.fill(m.score * 100)} /></div>
              <div style={S.sim}>{(m.score * 100).toFixed(1)}% behavioural similarity</div>
            </div>
          ))}

          <div style={S.saved}>
            Profile saved — you can now use it in <strong>Predict</strong> and <strong>Reconstruct</strong> without re-entering your description.
          </div>
        </div>
      )}
    </div>
  )
}
