from pydantic import BaseModel
from typing import List


class ChatInput(BaseModel):
    message: str


class FormInput(BaseModel):
    variables: List[float] 