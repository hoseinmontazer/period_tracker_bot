import httpx
from utils import load_tokens, save_tokens
from config import BASE_URL

async def authenticate_user(username, password):
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{BASE_URL}/api/auth/jwt/create/", data={"username": username, "password": password})

        if response.status_code == 200:
            json_response = response.json()
            return json_response.get("access")

        return None

async def refresh_token(chat_id, user_tokens):
    """Refresh the access token using the refresh token."""
    if chat_id not in user_tokens or "refresh" not in user_tokens[chat_id]:
        return None

    refresh_token = user_tokens[chat_id]["refresh"]
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{BASE_URL}/api/auth/jwt/refresh/", data={"refresh": refresh_token})

        if response.status_code == 200:
            new_access = response.json().get("access")
            user_tokens[chat_id]["access"] = new_access
            save_tokens(user_tokens)
            return new_access
        return None

