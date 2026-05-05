# Historical Persona System

A behavioural analysis platform that encodes historical figures into 10-dimensional vectors and enables cross-civilisation matching, reconstruction, and interactive exploration.

## Overview

The system extracts behavioural profiles from Wikipedia and user-supplied sources using Claude (claude-sonnet-4-6), stores them as 10-dimensional vectors in SQLite, and provides a range of matching and analysis features across 400+ historical figures.

**10 Behavioural Dimensions**

| Dimension | Scale |
|-----------|-------|
| Oppression | Endures silently → Actively resists |
| Group | Lone wolf → Relies on collective |
| Principle | Principle above all → Interest above all |
| Trust | Highly open → Deeply suspicious |
| Change | Preserve status quo → Radical change |
| Emotion | Calm and controlled → Emotional and impulsive |
| Motivation | Idealism → Survival/power |
| Mission | Lives in present → Mission-driven |
| Injustice | Accepts and adapts → Anger and resistance |
| Expression | Silent and reserved → Vocal and assertive |

## Features

| Feature | Description |
|---------|-------------|
| **Match** | Describe yourself → generate your 10D profile → find your historical mirrors |
| **Predict** | Historical figures with similar DNA channel their lived experience to advise you |
| **Reconstruct** | Fill missing dimensions of ancient figures using modern equivalents or your own profile |
| **Figures** | Add any Wikipedia figure to the database; optionally supply supplementary sources |
| **Chat** | Converse with a historical figure in character |
| **Reverse** | Find cross-civilisation behavioural equivalents of any figure |
| **Graph** | Visualise the behavioural network around a figure |
| **Locations** | Key geographical locations of a figure's life |
| **Relics** | Match an artefact description to historical figures by behavioural profile |
| **Benchmark** | Global distribution of behavioural patterns across the database |
| **Map** | T-SNE 2D projection of all figures — explore behavioural clusters |

### Advanced Matching
- **Dynamic dimension weighting** — 5 presets (Equal, Mission-first, Leadership, Idealist, Emotion) plus custom sliders
- **Client-side vector cache** — figure vectors stored in IndexedDB; similarity computed locally for instant results
- **Profile Explorer** — drag radar chart vertices after matching to see real-time match updates
- **Confidence-weighted similarity** — each dimension carries a confidence score; low-confidence dimensions contribute less to matching

## Tech Stack

**Backend**
- Python / FastAPI
- SQLite (via `database.py`)
- Anthropic API (`claude-sonnet-4-6`) for profile extraction, chat, prediction
- scikit-learn (T-SNE clustering)

**Frontend**
- React 19 / Vite
- Recharts (radar charts, benchmark visualisation)
- IndexedDB (local vector cache)
- Custom SVG draggable radar component

## Getting Started

### Prerequisites
- Python 3.10+
- Node.js 18+
- Anthropic API key

### Installation

```bash
git clone https://github.com/sc22cz/historical-persona-system.git
cd historical-persona-system

# Backend
python3 -m venv venv
source venv/bin/activate
pip install -r backend/requirements.txt

# Frontend
cd frontend && npm install && cd ..
```

### Running

**Option A — single command**
```bash
export ANTHROPIC_API_KEY=your_key_here
npm start
```

**Option B — two terminals**
```bash
# Terminal 1 — backend
export ANTHROPIC_API_KEY=your_key_here
source venv/bin/activate
cd backend && uvicorn main:app --reload

# Terminal 2 — frontend
cd frontend && npm run dev
```

Open `http://localhost:5173` in your browser.

### Bulk Import

To populate the database with historical figures:
```bash
source venv/bin/activate
cd backend
python3 bulk_import.py
```

The script includes 500+ figures and skips any already in the database. Allow ~4 seconds per figure for API processing.

## Project Structure

```
historical-persona-system/
├── backend/
│   ├── main.py              # FastAPI app, CORS, startup
│   ├── database.py          # SQLite connection and schema
│   ├── imputer.py           # Missing dimension reconstruction
│   ├── routers/             # API route handlers (14 endpoints)
│   └── services/            # extractor, matcher, predictor, chat…
├── frontend/
│   ├── src/
│   │   ├── pages/           # One component per feature page
│   │   ├── components/      # DraggableRadar, Skeleton
│   │   └── services/        # vectorStore (IndexedDB), similarity
│   └── package.json
└── package.json             # Root — concurrently starts both servers
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/analyze/` | Fetch Wikipedia + optional supplement, extract profile |
| GET | `/figures/` | List all figures with profiles |
| POST | `/match/` | Match user description to figures (supports weights) |
| POST | `/predict/` | Generate historical advice |
| POST | `/reconstruct/` | Reconstruct missing dimensions |
| GET | `/reverse/{name}` | Find cross-civilisation equivalents |
| POST | `/chat/` | Persona dialogue |
| POST | `/graph/` | Behavioural network |
| POST | `/locations/` | Life geography |
| POST | `/relics/match/` | Artefact attribution |
| GET | `/benchmark/` | Database-wide statistics |
| GET | `/cluster/` | T-SNE 2D projection |
