import json
from pathlib import Path
from urllib.parse import quote_plus

from pymongo import MongoClient
from pymongo.server_api import ServerApi

from config import settings

CLUES_PATH = Path("./clues.json")
CONNECTION_STRING = "mongodb+srv://{username}:{password}@{cluster}/?retryWrites=true&w=majority&appName={name}"

def get_connection_string(settings):
    return CONNECTION_STRING.format(
        username=quote_plus(settings.DB_USERNAME),
        password=quote_plus(settings.DB_PASSWORD),
        cluster=settings.CLUSTER,
        name=settings.DB_NAME,
    )

def get_clues_data(clues_path):
    with open(clues_path, "rt") as clues_file:
        clues_data = json.loads(clues_file.read())
    return clues_data

def get_db(connection_string):
    client = MongoClient(connection_string, server_api=ServerApi("1"))
    return client[settings.DB_NAME]

def get_clues(db):
    clues = db["clues"]
    cursor = clues.find({}, {"_id": 0})
    return list(cursor)

def insert_clues(db, clues_data):
    clues_data = [clue | {"wildcard": False} for clue in clues_data]
    clues = db["clues"]
    clues.insert_many(clues_data)

db = get_db(get_connection_string(settings))

if __name__ == "__main__":
    clues_data = get_clues_data(CLUES_PATH)
    insert_clues(db, clues_data)
