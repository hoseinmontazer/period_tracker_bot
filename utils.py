import json
from pathlib import Path

TOKEN_FILE = Path("user_data.json")

def load_user_data():
    if TOKEN_FILE.exists():
        return json.loads(TOKEN_FILE.read_text())
    return {}

def save_user_data(data):
    TOKEN_FILE.write_text(json.dumps(data))
