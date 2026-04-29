import { BrowserRouter, Routes, Route, NavLink } from "react-router-dom"
import Match from "./pages/Match"
import Reverse from "./pages/Reverse"
import Analyze from "./pages/Analyze"
import Chat from "./pages/Chat"
import Predict from "./pages/Predict"
import Reconstruct from "./pages/Reconstruct"
import Relics from "./pages/Relics"
import Benchmark from "./pages/Benchmark"

export const API = "https://historical-persona-system-production.up.railway.app"
export const API_KEY = "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"

const nav = [
  { path: "/", label: "Match" },
  { path: "/reverse", label: "Reverse" },
  { path: "/analyze", label: "Analyze" },
  { path: "/chat", label: "Chat" },
  { path: "/predict", label: "Predict" },
  { path: "/reconstruct", label: "Reconstruct" },
  { path: "/relics", label: "Relics" },
  { path: "/benchmark", label: "Benchmark" },
]

export default function App() {
  return (
    <BrowserRouter>
      <div style={{ maxWidth: 720, margin: "0 auto", padding: "0 20px", fontFamily: "sans-serif" }}>
        <h1 style={{ marginTop: 40, marginBottom: 8 }}>Historical Persona System</h1>
        <nav style={{ display: "flex", gap: 16, marginBottom: 32, borderBottom: "1px solid #eee", paddingBottom: 12, flexWrap: "wrap" }}>
          {nav.map(n => (
            <NavLink
              key={n.path}
              to={n.path}
              end={n.path === "/"}
              style={({ isActive }) => ({
                color: isActive ? "#1a1a1a" : "#999",
                textDecoration: "none",
                fontWeight: isActive ? 500 : 400,
                fontSize: 14
              })}
            >
              {n.label}
            </NavLink>
          ))}
        </nav>
        <Routes>
          <Route path="/" element={<Match />} />
          <Route path="/reverse" element={<Reverse />} />
          <Route path="/analyze" element={<Analyze />} />
          <Route path="/chat" element={<Chat />} />
          <Route path="/predict" element={<Predict />} />
          <Route path="/reconstruct" element={<Reconstruct />} />
          <Route path="/relics" element={<Relics />} />
          <Route path="/benchmark" element={<Benchmark />} />
        </Routes>
      </div>
    </BrowserRouter>
  )
}