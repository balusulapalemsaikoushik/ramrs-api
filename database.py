import json
from pathlib import Path
from urllib.parse import quote_plus

import certifi
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

def get_client(connection_string):
    return MongoClient(
        connection_string,
        server_api=ServerApi("1"),
        tlsCAFile=certifi.where(),
    )

def get_clues(db):
    clues = db["clues"]
    cursor = clues.find({}, {"_id": 0})
    return list(cursor)

def insert_clues(db, clues_data):
    manual_data = {"answer": None, "wildcard": False}
    clues_data = [clue | manual_data for clue in clues_data]
    clues = db["clues"]
    clues.insert_many(clues_data)

client = get_client(get_connection_string(settings))
db = client[settings.DB_NAME]

if __name__ == "__main__":
    try:
        clues_data = get_clues_data(CLUES_PATH)
        insert_clues(db, clues_data)
    finally:
        client.close()
