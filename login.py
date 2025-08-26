import httpx
from config import BASE_URL

async def login_user(username: str, password: str):
    """Call the API to log in and return access token."""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{BASE_URL}api/auth/jwt/create/",
                data={'username': username, 'password': password}
            )
            if response.status_code == 200:
                data = response.json()
                return data['access'], data.get('refresh')
            else:
                return None, None
        except Exception as e:
            print(f"Login error: {e}")
            return None, None
