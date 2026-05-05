import { BrowserRouter, Routes, Route, NavLink } from "react-router-dom"
import Match from "./pages/Match"
import Predict from "./pages/Predict"
import Reconstruct from "./pages/Reconstruct"
import Figures from "./pages/Analyze"
import Chat from "./pages/Chat"
import Graph from "./pages/Graph"
import Locations from "./pages/Locations"
import Reverse from "./pages/Reverse"
import Relics from "./pages/Relics"
import Benchmark from "./pages/Benchmark"
import Cluster from "./pages/Cluster"

export const API = "http://localhost:8000"

const NAV_GROUPS = [
  {
    label: "You",
    items: [
      { path: "/", label: "Match" },
      { path: "/predict", label: "Predict" },
      { path: "/reconstruct", label: "Reconstruct" },
    ]
  },
  {
    label: "Figures",
    items: [
      { path: "/figures", label: "Database" },
      { path: "/chat", label: "Chat" },
      { path: "/reverse", label: "Reverse" },
    ]
  },
  {
    label: "Explore",
    items: [
      { path: "/graph", label: "Graph" },
      { path: "/locations", label: "Locations" },
      { path: "/relics", label: "Relics" },
      { path: "/cluster", label: "Map" },
      { path: "/benchmark", label: "Benchmark" },
    ]
  },
]

const navLinkStyle = ({ isActive }) => ({
  display: "inline-block",
  padding: "6px 12px",
  fontSize: 13,
  fontWeight: isActive ? 600 : 400,
  color: isActive ? "#111" : "#999",
  textDecoration: "none",
  borderBottom: isActive ? "2px solid #111" : "2px solid transparent",
  whiteSpace: "nowrap",
  transition: "color 0.15s",
})

export default function App() {
  return (
    <BrowserRouter>
      <div style={{ maxWidth: 780, margin: "0 auto", padding: "0 24px 80px" }}>
        <div style={{ padding: "28px 0 0", borderBottom: "1px solid #e5e5e5", marginBottom: 32 }}>
          <div style={{ display: "flex", alignItems: "baseline", gap: 10, marginBottom: 14 }}>
            <span style={{ fontSize: 17, fontWeight: 700, color: "#111", letterSpacing: "-0.4px" }}>
              Historical Persona System
            </span>
            <span style={{ fontSize: 12, color: "#bbb" }}>Behavioural DNA across civilisations</span>
          </div>
          <nav style={{ display: "flex", gap: 0, overflowX: "auto", alignItems: "center" }}>
            {NAV_GROUPS.map((group, gi) => (
              <div key={gi} style={{ display: "flex", alignItems: "center" }}>
                {gi > 0 && (
                  <span style={{ color: "#e0e0e0", fontSize: 16, padding: "0 4px", userSelect: "none" }}>│</span>
                )}
                <span style={{ fontSize: 10, fontWeight: 700, color: "#ccc", letterSpacing: 1.5, textTransform: "uppercase", padding: "6px 8px 6px 4px", whiteSpace: "nowrap" }}>
                  {group.label}
                </span>
                {group.items.map(n => (
                  <NavLink key={n.path} to={n.path} end={n.path === "/"} style={navLinkStyle}>
                    {n.label}
                  </NavLink>
                ))}
              </div>
            ))}
          </nav>
        </div>
        <Routes>
          <Route path="/" element={<Match />} />
          <Route path="/predict" element={<Predict />} />
          <Route path="/reconstruct" element={<Reconstruct />} />
          <Route path="/figures" element={<Figures />} />
          <Route path="/chat" element={<Chat />} />
          <Route path="/graph" element={<Graph />} />
          <Route path="/locations" element={<Locations />} />
          <Route path="/reverse" element={<Reverse />} />
          <Route path="/relics" element={<Relics />} />
          <Route path="/benchmark" element={<Benchmark />} />
          <Route path="/cluster" element={<Cluster />} />
        </Routes>
      </div>
    </BrowserRouter>
  )
}
