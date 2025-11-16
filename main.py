from contextlib import asynccontextmanager
from typing import Dict, List
from fastapi import FastAPI

import crud
from database import client
from models import Clue

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    client.close()

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def main():
    return {
        "message": "welcome to version 0.0.8 of the ramrs api"
    }

@app.get("/clues", response_model=Dict[str, List[Clue]])
async def get_grouped_clues():
    return crud.get_grouped_clues()

@app.get("/clues/{category}", response_model=List[Clue])
async def get_category_clues(category: str):
    return crud.get_category_clues(category)
