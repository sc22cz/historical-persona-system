import { useState, useEffect, useRef } from "react"
import axios from "axios"
import { API } from "../App"

const PERIOD_COLORS = {
  "Ancient": "#111",
  "Medieval": "#555",
  "Early Modern": "#888",
  "Modern": "#aaa",
  "Contemporary": "#ccc",
  "": "#bbb",
}

function getColor(period) {
  for (const key of Object.keys(PERIOD_COLORS)) {
    if (period?.includes(key)) return PERIOD_COLORS[key]
  }
  return "#888"
}

const S = {
  desc: { fontSize: 13, color: "#888", marginBottom: 20, lineHeight: 1.7 },
  legend: { display: "flex", gap: 16, flexWrap: "wrap", marginBottom: 20 },
  legendItem: { display: "flex", alignItems: "center", gap: 6, fontSize: 12, color: "#555" },
  dot: (color) => ({ width: 10, height: 10, borderRadius: "50%", background: color, flexShrink: 0 }),
  tooltip: { position: "fixed", background: "#111", color: "#fff", padding: "6px 10px", borderRadius: 6, fontSize: 12, pointerEvents: "none", zIndex: 100, whiteSpace: "nowrap" },
  controls: { display: "flex", gap: 10, marginBottom: 16, alignItems: "center" },
}

export default function Cluster() {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState("")
  const [tooltip, setTooltip] = useState(null)
  const [search, setSearch] = useState("")
  const [selected, setSelected] = useState(null)

  const fetchCluster = async () => {
    setLoading(true)
    setError("")
    try {
      const res = await axios.get(`${API}/cluster/`)
      if (res.data?.points) setData(res.data)
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to load cluster data.")
    }
    setLoading(false)
  }

  useEffect(() => { fetchCluster() }, [])

  if (loading) return <div><h2 style={{ marginBottom: 16 }}>Behavioural Map</h2><p style={S.desc}>Running T-SNE on {`all figures`}… this takes ~10 seconds.</p></div>
  if (error) return <div><h2 style={{ marginBottom: 16 }}>Behavioural Map</h2><div style={{ color: "#dc2626", fontSize: 13 }}>{error}</div></div>
  if (!data) return null

  const points = data.points
  const xs = points.map(p => p.x)
  const ys = points.map(p => p.y)
  const minX = Math.min(...xs), maxX = Math.max(...xs)
  const minY = Math.min(...ys), maxY = Math.max(...ys)

  const W = 680, H = 480, PAD = 32
  const rangeX = maxX - minX || 1
  const rangeY = maxY - minY || 1
  const scaleX = x => PAD + ((x - minX) / rangeX) * (W - PAD * 2)
  const scaleY = y => PAD + ((y - minY) / rangeY) * (H - PAD * 2)

  const searchLower = search.toLowerCase()
  const userProfile = (() => {
    try { return JSON.parse(localStorage.getItem("hps_profile")) } catch { return null }
  })()

  return (
    <div>
      <h2 style={{ marginBottom: 6 }}>Behavioural Map</h2>
      <p style={S.desc}>
        {data.total} figures projected to 2D using T-SNE. Proximity = behavioural similarity. Each dot is a historical figure.
      </p>

      <div style={S.legend}>
        {Object.entries(PERIOD_COLORS).filter(([k]) => k).map(([period, color]) => (
          <div key={period} style={S.legendItem}>
            <div style={S.dot(color)} />
            {period}
          </div>
        ))}
      </div>

      <div style={S.controls}>
        <input
          value={search}
          onChange={e => setSearch(e.target.value)}
          placeholder="Highlight a figure…"
          style={{ width: 200, padding: "6px 12px", fontSize: 13 }}
        />
        <button className="secondary" style={{ fontSize: 12, padding: "6px 12px" }} onClick={fetchCluster}>
          Recompute
        </button>
      </div>

      <div style={{ border: "1px solid #e5e5e5", borderRadius: 8, overflow: "hidden", background: "#fafafa" }}>
        <svg width={W} height={H} style={{ display: "block" }}>
          {points.map(p => {
            const x = scaleX(p.x), y = scaleY(p.y)
            const color = getColor(p.period)
            const highlighted = search && p.name.toLowerCase().includes(searchLower)
            const isSelected = selected?.id === p.id
            return (
              <g key={p.id}>
                <circle
                  cx={x} cy={y}
                  r={highlighted || isSelected ? 7 : 4}
                  fill={highlighted || isSelected ? "#111" : color}
                  fillOpacity={highlighted || isSelected ? 1 : 0.7}
                  stroke={isSelected ? "#111" : "none"}
                  strokeWidth={2}
                  style={{ cursor: "pointer" }}
                  onMouseEnter={e => setTooltip({ x: e.clientX + 12, y: e.clientY - 8, name: p.name, era: p.era, period: p.period })}
                  onMouseLeave={() => setTooltip(null)}
                  onClick={() => setSelected(isSelected ? null : p)}
                />
                {highlighted && (
                  <text x={x + 8} y={y + 4} fontSize={10} fill="#111" fontWeight={600}>{p.name}</text>
                )}
              </g>
            )
          })}

          {userProfile && (() => {
            return null
          })()}
        </svg>
      </div>

      {selected && (
        <div style={{ marginTop: 12, padding: "10px 16px", border: "1px solid #e5e5e5", borderRadius: 8, fontSize: 13 }}>
          <strong>{selected.name}</strong>
          <span style={{ color: "#888", marginLeft: 10 }}>
            {selected.era < 0 ? `${Math.abs(selected.era)} BC` : `${selected.era} AD`}
          </span>
          {selected.period && <span style={{ color: "#aaa", marginLeft: 8 }}>{selected.period}</span>}
        </div>
      )}

      {tooltip && (
        <div style={{ ...S.tooltip, left: tooltip.x, top: tooltip.y }}>
          {tooltip.name} · {tooltip.era < 0 ? `${Math.abs(tooltip.era)} BC` : `${tooltip.era} AD`}
        </div>
      )}
    </div>
  )
}
