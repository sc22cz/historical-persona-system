from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import init_db
from routers.figures import router as figures_router
from routers.match import router as match_router

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