from argparse import ArgumentParser
from datetime import datetime
import json
from pathlib import Path

from database import client, db, get_clues

def _get_timestamp_as_filename():
    return f"{datetime.now().strftime("%Y-%m-%d %H%M%S")}.json"

def download_backup(backup_path=None):
    clues = get_clues(db)
    if backup_path is None:
        backup_path = _get_timestamp_as_filename()
    elif (backup_path := Path(backup_path)).is_dir():
        backup_path = backup_path / _get_timestamp_as_filename()
    with open(backup_path, "wt") as backup_file:
        backup_file.write(json.dumps(clues))

def load_backup(backup_path):
    if (backup_path := Path(backup_path)).is_dir():
        backup_paths = backup_path.glob("*.json")
        backup_path = max(backup_paths, key=lambda path: path.stat().st_mtime)
    with open(backup_path, "rt") as backup_file:
        backup = json.loads(backup_file.read())
    db.drop_collection("clues")
    clues = db["clues"]
    clues.insert_many(backup)

def _get_parser():
    parser = ArgumentParser("backup", description="download/load ramrs backups")
    subparsers = parser.add_subparsers(required=True)
    parser_download = subparsers.add_parser("download")
    parser_download.add_argument("-b", "--backup-path", default="./backup/")
    parser_download.set_defaults(func=download_backup)
    parser_load = subparsers.add_parser("load")
    parser_load.add_argument("-b", "--backup-path", default="./backup/")
    parser_load.set_defaults(func=load_backup)
    return parser

if __name__ == "__main__":
    parser = _get_parser()
    try:
        args = parser.parse_args()
        args.func(args.backup_path)
    finally:
        client.close()
