import { useRef, useState, useCallback } from "react"

const DIMS = ["Oppression", "Group", "Principle", "Trust", "Change", "Emotion", "Motivation", "Mission", "Injustice", "Expression"]
const N = DIMS.length
const CX = 160, CY = 160, R = 120

function angle(i) { return (i / N) * 2 * Math.PI - Math.PI / 2 }
function toXY(i, r) { return [CX + r * Math.cos(angle(i)), CY + r * Math.sin(angle(i))] }

export default function DraggableRadar({ vector, onChange }) {
  const svgRef = useRef(null)
  const [dragging, setDragging] = useState(null)

  const getVal = useCallback((e, i) => {
    const svg = svgRef.current
    const rect = svg.getBoundingClientRect()
    const mx = (e.clientX ?? e.touches?.[0]?.clientX) - rect.left
    const my = (e.clientY ?? e.touches?.[0]?.clientY) - rect.top
    const dx = mx - CX, dy = my - CY
    const a = angle(i)
    const proj = dx * Math.cos(a) + dy * Math.sin(a)
    const val = Math.min(1, Math.max(0, proj / R))
    return Math.round(val * 100) / 100
  }, [])

  const onMouseMove = useCallback(e => {
    if (dragging === null) return
    const val = getVal(e, dragging)
    const next = [...vector]
    next[dragging] = val
    onChange(next)
  }, [dragging, vector, onChange, getVal])

  const onMouseUp = useCallback(() => setDragging(null), [])

  const points = vector.map((v, i) => toXY(i, v * R))
  const polyline = points.map(([x, y]) => `${x},${y}`).join(" ")

  const gridLevels = [0.25, 0.5, 0.75, 1.0]

  return (
    <svg
      ref={svgRef}
      width={320} height={320}
      style={{ userSelect: "none", touchAction: "none", cursor: dragging !== null ? "grabbing" : "default" }}
      onMouseMove={onMouseMove}
      onMouseUp={onMouseUp}
      onMouseLeave={onMouseUp}
      onTouchMove={onMouseMove}
      onTouchEnd={onMouseUp}
    >
      {/* grid */}
      {gridLevels.map(lvl => (
        <polygon
          key={lvl}
          points={DIMS.map((_, i) => toXY(i, lvl * R).join(",")).join(" ")}
          fill="none" stroke="#e5e5e5" strokeWidth={1}
        />
      ))}

      {/* axes */}
      {DIMS.map((_, i) => {
        const [x, y] = toXY(i, R)
        return <line key={i} x1={CX} y1={CY} x2={x} y2={y} stroke="#e5e5e5" strokeWidth={1} />
      })}

      {/* filled area */}
      <polygon points={polyline} fill="#111" fillOpacity={0.12} stroke="#111" strokeWidth={1.5} />

      {/* labels */}
      {DIMS.map((dim, i) => {
        const [x, y] = toXY(i, R + 18)
        const anchor = x < CX - 5 ? "end" : x > CX + 5 ? "start" : "middle"
        return (
          <text key={i} x={x} y={y} textAnchor={anchor} dominantBaseline="middle"
            fontSize={10} fill="#888">
            {dim}
          </text>
        )
      })}

      {/* draggable handles */}
      {vector.map((v, i) => {
        const [x, y] = toXY(i, v * R)
        return (
          <circle
            key={i}
            cx={x} cy={y} r={6}
            fill={dragging === i ? "#111" : "#fff"}
            stroke="#111" strokeWidth={2}
            style={{ cursor: "grab" }}
            onMouseDown={e => { e.preventDefault(); setDragging(i) }}
            onTouchStart={e => { e.preventDefault(); setDragging(i) }}
          />
        )
      })}
    </svg>
  )
}
