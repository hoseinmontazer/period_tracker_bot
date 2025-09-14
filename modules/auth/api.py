import aiohttp
from config import BASE_URL

async def register_user(username, password, email, sex):
    """Register a new user"""
    url = f"{BASE_URL}/api/auth/users/"
    data = {
        "username": username,
        "password": password,
        "re_password": password,
        "email": email,
        "sex": sex
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=data) as response:
            return await response.json()

async def login_user(username, password):
    """Login user and get JWT tokens"""
    url = f"{BASE_URL}/api/auth/jwt/create/"
    data = {
        "username": username,
        "password": password
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=data) as response:
            return await response.json()