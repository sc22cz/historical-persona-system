import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import APIRouter
from pydantic import BaseModel
from services.extractor import extract_profile
from services.matcher import find_matches
from services.predictor import predict_future

router = APIRouter(prefix="/predict", tags=["predict"])

class PredictRequest(BaseModel):
    description: str

@router.post("/")
def predict(data: PredictRequest):
    profile = extract_profile("user", data.description)
    vector = profile["vector"]
    matches = find_matches(vector, top_k=3)
    prediction = predict_future(data.description, vector, matches)
    return prediction
