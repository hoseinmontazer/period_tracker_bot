import httpx
from utils import load_tokens
from config import BASE_URL
from datetime import datetime

async def fetch_periods(update, access_token):
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
                await update.message.reply_text("ℹ️ You have no recorded period history.")
                return
            
            formatted_periods = "📅 **Your Period History**:\n\n"
            
            for idx, period in enumerate(sorted(periods, key=lambda x: x["start_date"], reverse=True), start=1):
                start_date = period["start_date"]
                end_date = period["end_date"]
                predicted_end_date = period.get("predicted_end_date")
                
                formatted_periods += (
                    f"✨ *Cycle {idx}* ✨\n"
                    f"┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈\n\n"
                    f"🗓 *{start_date}* → *{end_date}*\n"
                    f"🔮 Predicted: *{predicted_end_date}*\n"
                    f"⏳ Duration: *{calculate_duration(start_date, end_date)}d*\n\n"
                    f"💫 *Symptoms*\n"
                    f"• {period['symptoms'] or 'None noted'}\n\n"
                    f"💊 *Medicine*\n"
                    f"• {period['medication'] or 'None taken'}\n\n"
                    f"•°•°•°•°•°•°•°•°•°\n\n"
                )

            await update.message.reply_text(formatted_periods, parse_mode="Markdown")
        else:
            await update.message.reply_text("❌ Failed to retrieve history. Please try again later.")

def calculate_duration(start_date, end_date):
    """Calculate the duration between start and end date"""
    if not start_date or not end_date:
        return "?"
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    return (end - start).days + 1

