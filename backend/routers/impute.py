import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import APIRouter
from imputer import impute_profile

router = APIRouter(prefix="/impute", tags=["impute"])

@router.get("/{figure_id}")
def impute(figure_id: int):
    return impute_profile(figure_id)