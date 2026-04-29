import { useState, useEffect } from "react"
import axios from "axios"
import { Radar, RadarChart, PolarGrid, PolarAngleAxis, ResponsiveContainer } from "recharts"
import { API } from "../App"

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
    } catch (err) {
      console.error(err)
    }
    setLoading(false)
  }

  useEffect(() => {
    handleFetch()
  }, [])

  const radarData = result ? Object.entries(result.dimension_averages).map(([key, val]) => ({
    dimension: key.replace(/_/g, " "),
    value: val || 0
  })) : []

  return (
    <div>
      <p style={{ color: "#666" }}>Global distribution of behavioural patterns across historical figures.</p>

      <div style={{ display: "flex", gap: 12, marginBottom: 24 }}>
        <select
          value={era}
          onChange={e => setEra(e.target.value)}
          style={{ flex: 1, padding: 10, fontSize: 14, borderRadius: 8, border: "1px solid #ddd" }}
        >
          <option value="">All eras</option>
          <option value="ancient">Ancient (before 1800)</option>
          <option value="modern">Modern (after 1800)</option>
        </select>
        <button
          onClick={handleFetch}
          disabled={loading}
          style={{ padding: "10px 20px", background: "#1a1a1a", color: "#fff", border: "none", borderRadius: 8, cursor: "pointer" }}
        >
          {loading ? "Loading..." : "Filter"}
        </button>
      </div>

      {result && (
        <div>
          <p style={{ fontSize: 14, color: "#666" }}>Total figures: <strong>{result.total_figures}</strong></p>

          <ResponsiveContainer width="100%" height={350}>
            <RadarChart data={radarData}>
              <PolarGrid />
              <PolarAngleAxis dataKey="dimension" tick={{ fontSize: 10 }} />
              <Radar dataKey="value" stroke="#6366f1" fill="#6366f1" fillOpacity={0.4} />
            </RadarChart>
          </ResponsiveContainer>

          <h2 style={{ marginTop: 24 }}>Insights</h2>
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: 12 }}>
            <div style={{ padding: 16, border: "1px solid #eee", borderRadius: 8, textAlign: "center" }}>
              <div style={{ fontSize: 28, fontWeight: 500 }}>{result.insights.high_mission_driven}</div>
              <div style={{ fontSize: 12, color: "#666", marginTop: 4 }}>Mission-driven</div>
            </div>
            <div style={{ padding: 16, border: "1px solid #eee", borderRadius: 8, textAlign: "center" }}>
              <div style={{ fontSize: 28, fontWeight: 500 }}>{result.insights.high_change_oriented}</div>
              <div style={{ fontSize: 12, color: "#666", marginTop: 4 }}>Change-oriented</div>
            </div>
            <div style={{ padding: 16, border: "1px solid #eee", borderRadius: 8, textAlign: "center" }}>
              <div style={{ fontSize: 28, fontWeight: 500 }}>{result.insights.lone_wolves}</div>
              <div style={{ fontSize: 12, color: "#666", marginTop: 4 }}>Lone wolves</div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}