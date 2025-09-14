import aiohttp
from config import BASE_URL

async def get_profile(token):
    """Get user profile"""
    url = f"{BASE_URL}/api/user/profile/"
    headers = {"Authorization": f"Bearer {token}"}
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            return await response.json()

async def get_invitation_code(token):
    """Get invitation code"""
    url = f"{BASE_URL}/api/user/invitation/"
    headers = {"Authorization": f"Bearer {token}"}
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            return await response.json()

async def generate_invitation_code(token):
    """Generate new invitation code"""
    url = f"{BASE_URL}/api/user/invitation/"
    headers = {"Authorization": f"Bearer {token}"}
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers) as response:
            return await response.json()

async def accept_invitation_code(token, code_to_accept):
    """Accept invitation code"""
    url = f"{BASE_URL}/api/user/invitation/"
    headers = {"Authorization": f"Bearer {token}"}
    data = {"code_to_accept": code_to_accept}
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=data, headers=headers) as response:
            return await response.json()

async def remove_partner(token, remove_code):
    """Remove partner"""
    url = f"{BASE_URL}/api/user/partner/remove/"
    headers = {"Authorization": f"Bearer {token}"}
    data = {"remove_code": remove_code}
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=data, headers=headers) as response:
            return await response.json()