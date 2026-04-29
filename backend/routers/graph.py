import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from graph import get_relationship_graph
from figure_resolver import resolve_figure

router = APIRouter(prefix="/graph", tags=["graph"])

class GraphRequest(BaseModel):
    name: str
    api_key: str

@router.post("/")
def graph(data: GraphRequest):
    figure = resolve_figure(data.name, data.api_key)
    if not figure:
        raise HTTPException(status_code=404, detail=f"Figure '{data.name}' not found")
    return get_relationship_graph(figure["id"])