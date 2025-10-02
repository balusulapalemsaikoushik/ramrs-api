from fastapi import FastAPI

import crud

app = FastAPI()

@app.get("/")
async def main():
    return {
        "message": "welcome to version 0.0.1 of the ramrs api"
    }

@app.get("/{category}")
async def get_category(category: str):
    return crud.get_category(category)
