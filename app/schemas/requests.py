from pydantic import BaseModel
from typing import List


class ChatInput(BaseModel):
    message: str
    session_id: str # ID of the chat session for context


class FormInput(BaseModel):
    variables: List[float] 