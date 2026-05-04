import { useState, useEffect } from "react"
import axios from "axios"
import { API } from "../App"

const S = {
  desc: { fontSize: 13, color: "#888", marginBottom: 20, lineHeight: 1.7 },
  row: { display: "flex", gap: 10, marginBottom: 12 },
  label: { fontSize: 12, fontWeight: 600, color: "#888", textTransform: "uppercase", letterSpacing: 1, marginBottom: 6, display: "block" },
  saved: { padding: "10px 14px", background: "#f8f8f8", border: "1px solid #e5e5e5", borderRadius: 6, fontSize: 13, color: "#555", marginBottom: 16, display: "flex", justifyContent: "space-between", alignItems: "center" },
  meta: { fontSize: 12, color: "#888", padding: "8px 12px", background: "#f8f8f8", border: "1px solid #e5e5e5", borderRadius: 6, marginBottom: 16 },
  body: { whiteSpace: "pre-wrap", lineHeight: 1.9, fontSize: 14, color: "#111", borderLeft: "2px solid #111", paddingLeft: 16, marginTop: 8 },
  err: { padding: "10px 14px", background: "#fafafa", border: "1px solid #e5e5e5", borderRadius: 6, fontSize: 13, color: "#dc2626", marginBottom: 16 },
}

export default function Reconstruct() {
  const [figureName, setFigureName] = useState("")
  const [userDesc, setUserDesc] = useState("")
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState("")
  const [step, setStep] = useState("idle")
  const [savedProfile, setSavedProfile] = useState(null)
  const [useProfile, setUseProfile] = useState(true)

  useEffect(() => {
    const raw = localStorage.getItem("hps_profile")
    if (raw) {
      try { setSavedProfile(JSON.parse(raw)) } catch {}
    }
  }, [])

  const handleReconstruct = async () => {
    if (!figureName.trim()) return
    setLoading(true)
    setError("")
    setResult(null)

    let user_vector = null

    if (savedProfile && useProfile) {
      user_vector = savedProfile.vector
    } else if (userDesc.trim()) {
      setStep("extracting")
      try {
        const matchRes = await axios.post(`${API}/match/`, { description: userDesc.trim(), top_k: 1 })
        user_vector = matchRes.data.user_profile.vector
      } catch {}
    }

    setStep("reconstructing")
    try {
      const res = await axios.post(`${API}/reconstruct/`, { name: figureName.trim(), user_vector })
      setResult(res.data)
    } catch (err) {
      setError(err.response?.data?.detail || "Reconstruction failed. Check the name is a valid Wikipedia entry.")
    }

    setStep("idle")
    setLoading(false)
  }

  const stepLabel = step === "extracting" ? "Extracting your profile…" : "Reconstructing…"

  return (
    <div>
      <h2 style={{ marginBottom: 6 }}>Reconstruct a Historical Figure</h2>
      <p style={S.desc}>
        Enter a historical figure. The system fills their missing behavioural dimensions using similar modern figures — or your own profile if you've completed a Match.
      </p>

      <span style={S.label}>Historical figure</span>
      <div style={S.row}>
        <input
          value={figureName}
          onChange={e => setFigureName(e.target.value)}
          onKeyDown={e => e.key === "Enter" && handleReconstruct()}
          placeholder="e.g. Hammurabi, Qin Shi Huang, Boudicca"
          style={{ flex: 1 }}
        />
        <button className="primary" onClick={handleReconstruct} disabled={loading} style={{ whiteSpace: "nowrap" }}>
          {loading ? stepLabel : "Reconstruct"}
        </button>
      </div>

      {savedProfile ? (
        <div style={S.saved}>
          <span>{useProfile ? "Using your saved profile to fill missing dimensions" : "Not using saved profile"}</span>
          <button className="secondary" style={{ fontSize: 12, padding: "4px 10px" }} onClick={() => setUseProfile(u => !u)}>
            {useProfile ? "Don't use" : "Use profile"}
          </button>
        </div>
      ) : (
        <div>
          <span style={S.label}>Your description <span style={{ fontWeight: 400, textTransform: "none", letterSpacing: 0, color: "#aaa" }}>(optional)</span></span>
          <textarea
            value={userDesc}
            onChange={e => setUserDesc(e.target.value)}
            placeholder="Describe yourself — used to fill the figure's missing dimensions if you share similar traits."
            style={{ width: "100%", height: 100, marginBottom: 16 }}
          />
        </div>
      )}

      {error && <div style={S.err}>{error}</div>}

      {result && (
        <div style={{ marginTop: 8 }}>
          <h2 style={{ marginBottom: 4 }}>{result.name}</h2>
          <div style={{ fontSize: 12, color: "#888", marginBottom: 12 }}>
            {result.era < 0 ? `${Math.abs(result.era)} BC` : `${result.era} AD`}
          </div>
          {result.similar_figure && result.similar_figure !== "unknown" && (
            <div style={S.meta}>
              Missing dimensions filled from: <strong>{result.similar_figure}</strong>
              {result.user_vector_used && <span style={{ marginLeft: 8, color: "#555" }}>· your profile was used</span>}
            </div>
          )}
          <div style={S.body}>{result.reconstruction}</div>
        </div>
      )}
    </div>
  )
}
