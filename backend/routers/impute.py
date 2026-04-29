import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from imputer import impute_profile
from services.figure_resolver import resolve_figure

router = APIRouter(prefix="/impute", tags=["impute"])

class ImputeRequest(BaseModel):
    name: str
    api_key: str

@router.post("/")
def impute(data: ImputeRequest):
    figure = resolve_figure(data.name, data.api_key)
    if not figure:
        raise HTTPException(status_code=404, detail=f"Figure '{data.name}' not found")
    return impute_profile(figure["id"])