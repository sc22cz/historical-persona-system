from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import init_db
from routers.figures import router as figures_router
from routers.match import router as match_router
from routers.reverse import router as reverse_router


app = FastAPI(title="Historical Persona System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    init_db()

@app.get("/")
def root():
    return {"message": "Historical Persona System is running"}

app.include_router(figures_router)
app.include_router(match_router)
app.include_router(reverse_router)

from fastapi.staticfiles import StaticFiles
import os

static_path = os.path.join(os.path.dirname(__file__), "../frontend/dist")
if os.path.exists(static_path):
    app.mount("/", StaticFiles(directory=static_path, html=True), name="static")