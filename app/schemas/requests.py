from pydantic import BaseModel
from typing import List


class ChatInput(BaseModel):
    message: str
    session_id: int  # ID of the chat session for context


class FormInput(BaseModel):
    variables: List[float] 