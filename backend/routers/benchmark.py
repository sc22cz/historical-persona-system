import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import APIRouter
from services.benchmark import get_benchmark

router = APIRouter(prefix="/benchmark", tags=["benchmark"])

@router.get("/")
def benchmark(era: str = None, region: str = None):
    return get_benchmark(era, region)