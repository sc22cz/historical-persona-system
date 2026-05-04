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

export const API = "http://localhost:8000"

const nav = [
  { path: "/", label: "Match" },
  { path: "/predict", label: "Predict" },
  { path: "/reconstruct", label: "Reconstruct" },
  { path: "/figures", label: "Figures" },
  { path: "/chat", label: "Chat" },
  { path: "/graph", label: "Graph" },
  { path: "/locations", label: "Locations" },
  { path: "/reverse", label: "Reverse" },
  { path: "/relics", label: "Relics" },
  { path: "/benchmark", label: "Benchmark" },
]

const S = {
  wrap: { maxWidth: 760, margin: "0 auto", padding: "0 24px 80px" },
  header: { padding: "32px 0 0", borderBottom: "1px solid #e5e5e5", marginBottom: 32 },
  title: { fontSize: 18, fontWeight: 700, color: "#111", letterSpacing: "-0.3px", marginBottom: 16 },
  nav: { display: "flex", gap: 0, overflowX: "auto" },
}

export default function App() {
  return (
    <BrowserRouter>
      <div style={S.wrap}>
        <div style={S.header}>
          <div style={S.title}>Historical Persona System</div>
          <nav style={S.nav}>
            {nav.map(n => (
              <NavLink
                key={n.path}
                to={n.path}
                end={n.path === "/"}
                style={({ isActive }) => ({
                  display: "inline-block",
                  padding: "8px 14px",
                  fontSize: 13,
                  fontWeight: isActive ? 600 : 400,
                  color: isActive ? "#111" : "#888",
                  textDecoration: "none",
                  borderBottom: isActive ? "2px solid #111" : "2px solid transparent",
                  whiteSpace: "nowrap",
                })}
              >
                {n.label}
              </NavLink>
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
        </Routes>
      </div>
    </BrowserRouter>
  )
}
