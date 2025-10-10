from typing import List

from pydantic import BaseModel

class Answer(BaseModel):
    answer: str
    category: str

class Clue(BaseModel):
    clue: str
    label: str
    answers: List[Answer]
    frequency: int
