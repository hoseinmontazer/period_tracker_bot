import logging
import aiohttp
from config import BASE_URL

async def get_all_periods(token: str, partner: str = None):
    """Get all periods"""
    url = f"{BASE_URL}/api/periods/"
    headers = {"Authorization": f"Bearer {token}"}
    if partner:
        print(" partner ---->" , partner)
        headers["role"] = partner
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            return await response.json()

async def create_period(token, start_date, cycle_length, period_duration, symptoms=None, medication=None):
    """
    Create a new period using form-data (multipart/form-data) like curl --form.
    """
    url = f"{BASE_URL}/api/periods/"
    headers = {
        "Authorization": f"Bearer {token}"
    }

    data = {
        "start_date": str(start_date),
        "cycle_length": str(cycle_length),
        "period_duration": str(period_duration)
    }

    if symptoms is not None:
        data["symptoms"] = str(symptoms)
    if medication is not None:
        data["medication"] = str(medication)

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=data, headers=headers) as response:
                result = await response.json()
                logging.debug("create_period response: %s", result)
                return result
    except aiohttp.ClientError as e:
        logging.exception("HTTP error while creating period")
        return {"error": str(e)}
    except Exception as e:
        logging.exception("Unexpected error while creating period")
        return {"error": str(e)}


async def update_latest_period(token, end_date):
    """Update latest period"""
    url = f"{BASE_URL}/api/periods/update_latest/"
    headers = {"Authorization": f"Bearer {token}"}
    data = {"end_date": end_date}
    
    async with aiohttp.ClientSession() as session:
        async with session.patch(url, data=data, headers=headers) as response:
            return await response.json()
        

async def delete_period(token,id):
    """ Delete Preriod id """
    url = f"{BASE_URL}/api/periods/{id}/"
    headers = {"Authorization" : f"Bearer {token}"}

    async with aiohttp.ClientSession() as session:
        # Use session.delete() for a DELETE request
        async with session.delete(url, headers=headers) as response:
            if response.status == 204:  # 204 No Content is a common success status for DELETE
                return {"success": True, "message": "Period deleted successfully"}
            else:
                try:
                    return await response.json()
                except aiohttp.client_exceptions.ContentTypeError:
                    return {"success": False, "message": f"Server responded with status {response.status} and no JSON content."}

