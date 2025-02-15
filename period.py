import httpx
from utils import load_tokens
from config import BASE_URL
from datetime import datetime
from languages import get_message

async def fetch_periods(update, access_token):
    lang = update.message.chat_data.get('language', 'en')
    headers = {"Authorization": f"Bearer {access_token}"}
    print(f"Using access token in periods: {access_token}")
   
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/api/periods/", headers=headers)

        if response.status_code == 401:  # Token expired
            chat_id = str(update.message.chat_id)
            new_token = await refresh_token(chat_id)
            if new_token:
                headers["Authorization"] = f"Bearer {new_token}"
                response = await client.get(f"{BASE_URL}/api/periods/", headers=headers)

        if response.status_code == 200:
            periods = response.json()
            
            if not periods:
                await update.message.reply_text(get_message(lang, 'errors', 'no_history'))
                return
            
            formatted_periods = f"{get_message(lang, 'period_history', 'title')}\n\n"
            
            for idx, period in enumerate(sorted(periods, key=lambda x: x["start_date"], reverse=True), start=1):
                start_date = period["start_date"]
                end_date = period["end_date"]
                predicted_end_date = period.get("predicted_end_date")
                
                formatted_periods += (
                    f"{get_message(lang, 'period_history', 'cycle', idx)}\n"
                    f"┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈\n\n"
                    f"🗓 *{start_date}* → *{end_date}*\n"
                    f"{get_message(lang, 'period_history', 'predicted')}: *{predicted_end_date}*\n"
                    f"{get_message(lang, 'period_history', 'duration')}: *{calculate_duration(start_date, end_date)}{get_message(lang, 'period_history', 'days')}*\n\n"
                    f"{get_message(lang, 'period_history', 'symptoms_title')}\n"
                    f"• {period['symptoms'] or get_message(lang, 'period_history', 'none_noted')}\n\n"
                    f"{get_message(lang, 'period_history', 'medicine_title')}\n"
                    f"• {period['medication'] or get_message(lang, 'period_history', 'none_taken')}\n\n"
                    f"•°•°•°•°•°•°•°•°•°\n\n"
                )

            await update.message.reply_text(formatted_periods, parse_mode="Markdown")
        else:
            await update.message.reply_text(get_message(lang, 'errors', 'fetch_failed'))

def calculate_duration(start_date, end_date):
    """Calculate the duration between start and end date"""
    if not start_date or not end_date:
        return get_message(update.message.chat_data.get('language', 'en'), 'errors', 'unknown_duration')
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    return (end - start).days + 1

