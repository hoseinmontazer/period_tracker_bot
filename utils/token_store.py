import json
import os

TOKEN_FILE = "user_tokens.json"

def load_tokens():
    """Load all tokens from file."""
    if not os.path.exists(TOKEN_FILE):
        return {}
    with open(TOKEN_FILE, "r") as f:
        return json.load(f)

def save_tokens(tokens):
    """Save all tokens to file."""
    with open(TOKEN_FILE, "w") as f:
        json.dump(tokens, f)

def get_token(chat_id):
    """Get token for a specific user."""
    tokens = load_tokens()
    return tokens.get(str(chat_id))

def set_token(chat_id, token):
    """Set token for a specific user."""
    tokens = load_tokens()
    tokens[str(chat_id)] = token
    save_tokens(tokens)

def remove_token(chat_id):
    """Remove token when user logs out."""
    tokens = load_tokens()
    tokens.pop(str(chat_id), None)
    save_tokens(tokens)
