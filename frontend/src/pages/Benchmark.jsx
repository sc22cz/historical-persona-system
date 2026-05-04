import { useState, useEffect } from "react"
import axios from "axios"
import { Radar, RadarChart, PolarGrid, PolarAngleAxis, ResponsiveContainer } from "recharts"
import { API } from "../App"

const S = {
  desc: { fontSize: 13, color: "#888", marginBottom: 20, lineHeight: 1.7 },
  row: { display: "flex", gap: 10, marginBottom: 24 },
  stat: { flex: 1, padding: 16, border: "1px solid #e5e5e5", borderRadius: 8, textAlign: "center" },
  statNum: { fontSize: 28, fontWeight: 600, color: "#111" },
  statLabel: { fontSize: 12, color: "#888", marginTop: 4 },
}

export default function Benchmark() {
  const [result, setResult] = useState(null)
  const [era, setEra] = useState("")
  const [loading, setLoading] = useState(false)

  const handleFetch = async () => {
    setLoading(true)
    try {
      const url = era ? `${API}/benchmark/?era=${era}` : `${API}/benchmark/`
      const res = await axios.get(url)
      setResult(res.data)
    } catch {}
    setLoading(false)
  }

  useEffect(() => { handleFetch() }, [])

  const radarData = result
    ? Object.entries(result.dimension_averages).map(([key, val]) => ({
        dimension: key.replace(/_/g, " "),
        value: val || 0,
      }))
    : []

  return (
    <div>
      <h2 style={{ marginBottom: 6 }}>Behavioural Benchmark</h2>
      <p style={S.desc}>Global distribution of behavioural patterns across all historical figures in the database.</p>

      <div style={S.row}>
        <select value={era} onChange={e => setEra(e.target.value)} style={{ flex: 1 }}>
          <option value="">All eras</option>
          <option value="ancient">Ancient (before 1800)</option>
          <option value="modern">Modern (after 1800)</option>
        </select>
        <button className="primary" onClick={handleFetch} disabled={loading}>
          {loading ? "Loading…" : "Apply"}
        </button>
      </div>

      {result && (
        <div>
          <p style={{ fontSize: 13, color: "#888", marginBottom: 20 }}>
            {result.total_figures} figures analysed
          </p>

          <ResponsiveContainer width="100%" height={320}>
            <RadarChart data={radarData}>
              <PolarGrid stroke="#e5e5e5" />
              <PolarAngleAxis dataKey="dimension" tick={{ fontSize: 11, fill: "#888" }} />
              <Radar dataKey="value" stroke="#111" fill="#111" fillOpacity={0.12} strokeWidth={1.5} />
            </RadarChart>
          </ResponsiveContainer>

          <h2 style={{ marginTop: 32, marginBottom: 16 }}>Insights</h2>
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: 12 }}>
            <div style={S.stat}>
              <div style={S.statNum}>{result.insights.high_mission_driven}</div>
              <div style={S.statLabel}>Mission-driven</div>
            </div>
            <div style={S.stat}>
              <div style={S.statNum}>{result.insights.high_change_oriented}</div>
              <div style={S.statLabel}>Change-oriented</div>
            </div>
            <div style={S.stat}>
              <div style={S.statNum}>{result.insights.lone_wolves}</div>
              <div style={S.statLabel}>Lone wolves</div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
