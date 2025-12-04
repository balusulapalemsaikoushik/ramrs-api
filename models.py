from pydantic import BaseModel, Field

class Clue(BaseModel):
    id: str = Field(alias="_id")
    clue: str
    label: str
    verified: bool
    answer: str
    category: str
    wildcard: bool
    frequency: int

class ClueUpdate(BaseModel):
    clue: str
    answer: str
    category: str
    wildcard: bool
