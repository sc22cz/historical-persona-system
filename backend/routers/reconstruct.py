import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import APIRouter
from pydantic import BaseModel
from services.reconstructor import reconstruct_history

router = APIRouter(prefix="/reconstruct", tags=["reconstruct"])

class ReconstructRequest(BaseModel):
    api_key: str

@router.post("/{figure_id}")
def reconstruct(figure_id: int, data: ReconstructRequest):
    return reconstruct_history(figure_id, data.api_key)