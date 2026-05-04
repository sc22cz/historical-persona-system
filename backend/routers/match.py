import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import APIRouter
from pydantic import BaseModel
from services.extractor import extract_profile
from services.matcher import find_matches

router = APIRouter(prefix="/match", tags=["match"])

class UserInput(BaseModel):
    description: str
    top_k: int = 5

@router.post("/")
def match_user(data: UserInput):
    profile = extract_profile("user", data.description)
    vector = profile["vector"]
    matches = find_matches(vector, data.top_k)
    return {
        "user_profile": profile,
        "matches": matches
    }
