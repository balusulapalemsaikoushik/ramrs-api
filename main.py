from typing import List
from fastapi import FastAPI

import crud
from models import Clue

app = FastAPI()

@app.get("/")
async def main():
    return {
        "message": "welcome to version 0.0.5 of the ramrs api"
    }

@app.get("/{category}", response_model=List[Clue])
async def get_category(category: str):
    return crud.get_category(category)
