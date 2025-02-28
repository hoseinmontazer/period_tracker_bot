import json
import os
import logging
import httpx
from config import BASE_URL

logger = logging.getLogger(__name__)

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
def save_tokens(tokens):
    """Save user tokens to JSON file."""
    with open('user_tokens.json', 'w') as f:
        json.dump(tokens, f, indent=4)

# Refresh token using the refresh token
async def refresh_token(chat_id, user_tokens):
    """Refresh the access token using the refresh token."""
    if chat_id not in user_tokens or "refresh" not in user_tokens[chat_id]:
        logger.warning(f"No refresh token found for chat_id: {chat_id}")
        return None

    refresh_token = user_tokens[chat_id]["refresh"]
    logger.info(f"Attempting to refresh token for chat_id: {chat_id}")
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{BASE_URL}/api/auth/jwt/refresh/", 
                data={"refresh": refresh_token}
            )

            logger.info(f"Refresh response status: {response.status_code}")
            if response.status_code == 200:
                new_access = response.json().get("access")
                user_tokens[chat_id]["access"] = new_access
                save_tokens(user_tokens)
                logger.info("Token refresh successful")
                return new_access
            else:
                logger.error(f"Token refresh failed: {response.text}")
                return None

    except Exception as e:
        logger.error(f"Token refresh error: {str(e)}")
        return None

