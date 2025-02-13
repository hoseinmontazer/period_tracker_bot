import httpx
from utils import load_tokens
from config import BASE_URL

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
                
                formatted_periods += (
                    f"🔹 **Cycle {idx}**\n"
                    f"   📆 Start: *{start_date}*\n"
                    f"   🛑 End: *{end_date}*\n"
                    f"   ⚕️ Symptoms: `{period['symptoms'] or 'None'}`\n"
                    f"   💊 Medication: `{period['medication'] or 'None'}`\n\n"
                )

            await update.message.reply_text(formatted_periods, parse_mode="Markdown")
        else:
            await update.message.reply_text("❌ Failed to retrieve history. Please try again later.")

