import json
import os
import httpx
from config import BASE_URL

# Load user tokens from file
def load_tokens():
    """Load user tokens from JSON file."""
    try:
        if os.path.exists('user_tokens.json') and os.path.getsize('user_tokens.json') > 0:
            with open('user_tokens.json', 'r') as f:
                return json.load(f)
        else:
            # If file doesn't exist or is empty, return empty dict
            return {}
    except json.JSONDecodeError:
        # If JSON is invalid, return empty dict
        return {}

# Save user tokens to file
def save_tokens(user_tokens):
    """Save user tokens to JSON file."""
    with open('user_tokens.json', 'w') as f:
        json.dump(user_tokens, f, indent=4)

# Refresh token using the refresh token
async def refresh_token(chat_id, user_tokens):
    """Refresh the access token using the refresh token."""
    if chat_id not in user_tokens or "refresh" not in user_tokens[chat_id]:
        return None  # No refresh token available

    refresh_token = user_tokens[chat_id]["refresh"]

    async with httpx.AsyncClient() as client:
        response = await client.post(f"{BASE_URL}/api/auth/jwt/refresh/", data={"refresh": refresh_token})

        if response.status_code == 200:
            new_access = response.json().get("access")
            user_tokens[chat_id]["access"] = new_access
            save_tokens(user_tokens)  # Save updated token
            return new_access
        else:
            return None  # Refresh failed

