

import aiohttp

from config import BASE_URL


async def send_wellness(
                        token: str,
                        stress_level: int = None,
                        sleep_hours: float = None,
                        mood_level: int = None,
                        energy_level: int = None,
                        pain_level: int = None,
                        exercise_minutes: int = None,
                        nutrition_quality: int = None,
                        caffeine_intake: int = None,
                        alcohol_intake: int = None,
                        smoking: int = None,
                        anxiety_level: int = None,
                        focus_level: int = None,
                        notes: str = None
                    ) -> dict:
    """
    Send daily wellness data to the API (application/json).
    Only sends fields that are not None.
    """
    url = f"{BASE_URL}/api/wellness/"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    # آماده‌سازی داده‌ها
    data = {
        "stress_level": stress_level,
        "sleep_hours": sleep_hours,
        "mood_level": mood_level,
        "energy_level": energy_level,
        "pain_level": pain_level,
        "exercise_minutes": exercise_minutes,
        "nutrition_quality": nutrition_quality,
        "caffeine_intake": caffeine_intake,
        "alcohol_intake": alcohol_intake,
        "smoking": smoking,
        "anxiety_level": anxiety_level,
        "focus_level": focus_level,
        "notes": notes,
    }

    # حذف فیلدهای None
    filtered_data = {k: v for k, v in data.items() if v is not None}

    print("Sending filtered wellness data --->", filtered_data)

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url, json=filtered_data, headers=headers) as response:
                response.raise_for_status()
                return await response.json()
        except aiohttp.ClientResponseError as e:
            print(f"HTTP error: {e.status} - {e.message}")
            text = await response.text()
            return {"error": f"HTTP {e.status}", "response_text": text}
        except Exception as e:
            print(f"Unexpected error: {e}")
            return {"error": str(e)}