import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import APIRouter
from pydantic import BaseModel
from services.persona_chat import persona_chat

router = APIRouter(prefix="/chat", tags=["chat"])

class ChatRequest(BaseModel):
    message: str
    api_key: str

@router.post("/{figure_id}")
def chat(figure_id: int, data: ChatRequest):
    return persona_chat(figure_id, data.message, data.api_key)