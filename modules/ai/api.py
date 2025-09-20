import aiohttp
import requests
from config import BASE_URL


async def get_suggestion(token: str, start_date: str = None) -> dict:
    print("==========> hi")

    url = f"{BASE_URL}/api/ai/suggestions/"
    headers = {"Authorization": f"Bearer {token}"}
    params = {}

    if start_date:
        params["start_date"] = start_date

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, params=params) as response:
            response.raise_for_status()  # Raise exception for HTTP errors
            return await response.json()
