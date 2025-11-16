# from typing import List

from pydantic import BaseModel, Field

# class Answer(BaseModel):
#     answer: str
#     category: str

# class Clue(BaseModel):
#     clue: str
#     label: str
#     answer: Answer | None
#     answers: List[Answer]
#     wildcard: bool
#     frequency: int

class Clue(BaseModel):
    id: str = Field(alias="_id")
    clue: str
    label: str
    verified: bool
    answer: str
    category: str
    wildcard: bool
    frequency: int
