from contextlib import asynccontextmanager
from typing import List
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.encoders import jsonable_encoder

from auth import has_scope, validate_token
import crud
from database import client
from models import Clue, ClueUpdate

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    client.close()

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def main():
    return {
        "message": "welcome to version 0.2.1 of the ramrs api"
    }

@app.get("/categories/{category}", response_model=List[Clue])
async def get_category_clues(category: str, nresults: int | None = None, verified: bool | None = None):
    if nresults is not None:
        if nresults < 0:
            raise HTTPException(
                status_code=400,
                details="Query parameter \"nresults\" must be a positive integer or zero."
            )
    return crud.get_ranked_clues(category, nresults, verified)

@app.patch("/clues/{clue_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_clue(clue_id: str, clue: ClueUpdate, claims: dict = Depends(validate_token)):
    if has_scope(claims, "write:clues"):
        crud.update_clue(clue_id, jsonable_encoder(clue))
    else:
        raise HTTPException(status_code=401, detail=f"You are not authorized to perform this action.")

@app.delete("/clues/{clue_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_clue(clue_id: str, claims: dict = Depends(validate_token)):
    if has_scope(claims, "write:clues"):
        crud.delete_clue(clue_id)
    else:
        raise HTTPException(status_code=401, detail=f"You are not authorized to perform this action.")
