import aiohttp
from config import BASE_URL

async def cycle_analysis(token, start_date=None):
    """Get cycle analysis"""
    url = f"{BASE_URL}/api/periods/cycle_analysis/"
    headers = {"Authorization": f"Bearer {token}"}
    params = {}
    
    if start_date:
        params["start_date"] = start_date
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params, headers=headers) as response:
            return await response.json()