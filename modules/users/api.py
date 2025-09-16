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
    if remove_code == None:
        data = {}
    else :
        data = {"remove_code": remove_code}
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=data, headers=headers) as response:
            return await response.json()
        
async def update_user_profile(token,
                         first_name: str = None,
                         last_name: str = None,
                         cycle_length: int = None,
                         period_duration: int = None
                         ):
    """Update user profile via PATCH"""
    url = f"{BASE_URL}/api/user/profile/"
    headers = {"Authorization": f"Bearer {token}"}
    data= {}
    if first_name is not None:
        data["first_name"] = first_name
    if last_name is not None:
        data["last_name"] = last_name
    if cycle_length is not None:
        data["cycle_length"] = str(cycle_length)  # form data as string
    if period_duration is not None:
        data["period_duration"] = str(period_duration)

    async with aiohttp.ClientSession() as session:
            async with session.patch(url, data=data, headers=headers) as response:
                if response.status == 200:
                    json_data = await response.json()
                    return True, json_data  # success
                else:
                    text = await response.text()
                    return False, text       # failure

