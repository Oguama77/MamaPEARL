from pydantic import BaseModel
from typing import List


class ChatInput(BaseModel):
    message: str
    user_id: str  # Unique identifier for the user to maintain per-user memory


class FormInput(BaseModel):
    variables: List[float] 