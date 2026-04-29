import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import APIRouter
from pydantic import BaseModel
from locations import get_figure_locations

router = APIRouter(prefix="/locations", tags=["locations"])

class LocationRequest(BaseModel):
    api_key: str

@router.post("/{figure_id}")
def locations(figure_id: int, data: LocationRequest):
    return get_figure_locations(figure_id, data.api_key)