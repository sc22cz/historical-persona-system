import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import APIRouter
from graph import get_relationship_graph

router = APIRouter(prefix="/graph", tags=["graph"])

@router.get("/{figure_id}")
def graph(figure_id: int):
    return get_relationship_graph(figure_id)