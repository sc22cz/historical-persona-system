import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import init_db
from routers.figures import router as figures_router
from routers.match import router as match_router
from routers.reverse import router as reverse_router
from routers.impute import router as impute_router
from routers.reconstruct import router as reconstruct_router
from routers.predict import router as predict_router
from routers.analyze import router as analyze_router
from routers.chat import router as chat_router
from routers.graph import router as graph_router
from routers.locations import router as locations_router
from routers.relics import router as relics_router
from routers.benchmark import router as benchmark_router


app = FastAPI(title="Historical Persona System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    if not os.environ.get("ANTHROPIC_API_KEY"):
        raise RuntimeError("ANTHROPIC_API_KEY environment variable is not set")
    init_db()

@app.get("/")
def root():
    return {"message": "Historical Persona System is running"}

app.include_router(figures_router)
app.include_router(match_router)
app.include_router(reverse_router)
app.include_router(impute_router)
app.include_router(reconstruct_router)
app.include_router(analyze_router)
app.include_router(predict_router)
app.include_router(chat_router)
app.include_router(graph_router)
app.include_router(locations_router)
app.include_router(relics_router)
app.include_router(benchmark_router)
