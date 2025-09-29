import aiohttp
import logging

from config import BASE_URL

logger = logging.getLogger(__name__)  # Create a logger for this module
# ========== GET SUGGESTION FROM API ==========
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



# ========== SEND FEEDBACK TO API ==========
async def send_feedback_to_api(suggestion_id, token, feedback: bool, corrected_label=None, response_text=None):
    url = f"{BASE_URL}api/ai/feedback/{suggestion_id}/"
    payload = {
        "feedback": str(feedback),
        "corrected_label": corrected_label or "",
        "response_text": response_text or "",
    }
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload, headers=headers) as response:
            if response.status not in (200, 201):
                text = await response.text()
                logger.error(f"Feedback API failed: {response.status} {text}")
            else:
                #  print(response.json())
                 return await response.json()