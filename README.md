# Historical Persona System

A behavioural analysis platform that encodes historical figures into 10-dimensional vectors and enables cross-civilisation matching, reconstruction, and interactive exploration.

## Overview

The system extracts behavioural profiles from Wikipedia and user-supplied sources using Claude (claude-sonnet-4-6), stores them as 10-dimensional vectors in SQLite, and provides a range of matching and analysis features across 470+ historical figures.

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
| **Reverse** | Find cross-civilisation behavioural equivalents of any figure |
| **Predict** | Ancient and modern figures with similar DNA answer your question in first person |
| **Reconstruct** | Describe an action → find similar ancient figures → generate fabricated historical accounts |
| **Chat** | Converse with any historical figure in character |
| **Database** | Add any Wikipedia figure; optionally supply supplementary sources |
| **Graph** | Visualise the behavioural network around a figure |
| **Locations** | Key geographical locations of a figure's life |
| **Relics** | Match an artefact description to historical figures by behavioural profile |
| **Map** | PCA 2D projection of all figures — explore behavioural clusters (client-side) |
| **Benchmark** | Global distribution of behavioural patterns across the database (client-side) |

### Advanced Matching
- **Dynamic dimension weighting** — 5 presets (Equal, Mission-first, Leadership, Idealist, Emotion) plus custom sliders
- **Client-side vector cache** — figure vectors stored in IndexedDB; similarity computed locally for instant results
- **Profile Explorer** — drag radar chart vertices after matching to see real-time match updates
- **Confidence-weighted similarity** — each dimension carries a confidence score; low-confidence dimensions contribute less to matching
- **Dark mode** — toggle in the top-right corner

## Tech Stack

**Backend**
- Python / FastAPI
- SQLite (via `database.py`)
- Anthropic API (`claude-sonnet-4-6`) for profile extraction, chat, prediction, reconstruction

**Frontend**
- React 19 / Vite
- Recharts (radar charts, benchmark visualisation)
- IndexedDB (local vector cache)
- Client-side PCA for behavioural map
- Custom SVG draggable radar component

## Getting Started

### Prerequisites
- Python 3.10+
- Node.js 18+
- Anthropic API key — **you must supply your own key**. Sign up at https://console.anthropic.com, generate a key, and set it as an environment variable before running. Usage is billed to your own account.

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

```bash
export ANTHROPIC_API_KEY=your_key_here
npm start
```

Open `http://localhost:5173` in your browser.

### Database

The repository includes a pre-populated SQLite database (`backend/data/historical.db`) with 473 historical figures already extracted and ready to use. **You do not need to run bulk_import.py** unless you want to add more figures.

### Bulk Import (optional)

To add more historical figures to the database:
```bash
source venv/bin/activate
cd backend
python3 bulk_import.py
```

The script includes 500+ figures and skips any already in the database. Allow ~4 seconds per figure for API processing.

### Running Tests

```bash
venv/bin/python -m pytest backend/tests/ -v
```

## Project Structure

```
historical-persona-system/
├── backend/
│   ├── main.py              # FastAPI app, CORS, static file serving
│   ├── database.py          # SQLite connection and schema
│   ├── imputer.py           # Missing dimension reconstruction
│   ├── routers/             # API route handlers
│   ├── services/            # extractor, matcher, predictor, reconstructor, chat…
│   ├── tests/               # pytest test suite (36 tests)
│   └── data/
│       └── historical.db    # SQLite database (470+ figures)
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
| POST | `/predict/` | Ancient and modern figures answer your question |
| POST | `/reconstruct/` | Fabricate historical accounts from behavioural DNA |
| GET | `/reverse/{name}` | Find cross-civilisation equivalents |
| POST | `/chat/` | Persona dialogue |
| POST | `/graph/` | Behavioural network |
| POST | `/locations/` | Life geography |
| POST | `/relics/match/` | Artefact attribution |
