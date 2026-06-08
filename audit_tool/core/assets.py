import json
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "assets.json"

def load_assets():
    with open(DATA_FILE, "r") as f:
        return json.load(f)
    