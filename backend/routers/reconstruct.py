import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from services.reconstructor import reconstruct_history
from services.figure_resolver import resolve_figure

router = APIRouter(prefix="/reconstruct", tags=["reconstruct"])

class ReconstructRequest(BaseModel):
    name: str
    user_vector: Optional[List[float]] = None

@router.post("/")
def reconstruct(data: ReconstructRequest):
    figure = resolve_figure(data.name)
    if not figure:
        raise HTTPException(status_code=404, detail=f"Figure '{data.name}' not found")
    return reconstruct_history(figure["id"], user_vector=data.user_vector)
