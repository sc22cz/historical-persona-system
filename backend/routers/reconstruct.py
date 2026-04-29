import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from reconstructor import reconstruct_history
from figure_resolver import resolve_figure

router = APIRouter(prefix="/reconstruct", tags=["reconstruct"])

class ReconstructRequest(BaseModel):
    name: str
    api_key: str

@router.post("/")
def reconstruct(data: ReconstructRequest):
    figure = resolve_figure(data.name, data.api_key)
    if not figure:
        raise HTTPException(status_code=404, detail=f"Figure '{data.name}' not found")
    return reconstruct_history(figure["id"], data.api_key)