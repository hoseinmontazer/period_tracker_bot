# cycle_analysis.py

import httpx
from utils import load_tokens, refresh_token  # These utilities should work as expected
from config import BASE_URL

async def fetch_cycle_analysis(update, access_token):
    """Fetch and display cycle analysis data."""
    chat_id = str(update.message.chat_id)
    headers = {"Authorization": f"Bearer {access_token}"}
    print(f"Using access token: {access_token}")

    # Load user tokens to check for refresh tokens
    user_tokens = load_tokens()  # Ensure this function loads the user tokens correctly

    # Make the request for cycle analysis
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/api/periods/cycle_analysis/", headers=headers)

        if response.status_code == 200:
            # Handle successful response
            analysis = response.json().get("data", {})
            if not analysis:
                await update.message.reply_text("ℹ️ No cycle analysis data available.")
                return

            # Formatting the cycle analysis
            formatted_analysis = (
                "📊 **Cycle Analysis Report**\n\n"
                f"📅 **Average Cycle Length:** `{analysis.get('average_cycle', 'N/A')} days`\n"
                f"📈 **Regularity Score:** `{analysis.get('regularity_score', 'N/A')}%`\n"
                f"🔄 **Cycle Variations:** `{', '.join(map(str, analysis.get('cycle_variations', [])))}`\n"
                f"🔮 **Prediction Reliability:** `{analysis.get('prediction_reliability', 'N/A')}%`\n"
            )

            # Sending the formatted analysis to the user
            await update.message.reply_text(formatted_analysis, parse_mode="Markdown")

        elif response.status_code == 401:
            # If session expired, attempt to refresh the token
            new_token = await refresh_token(chat_id, user_tokens)  # Pass user_tokens here
            if new_token:
                headers["Authorization"] = f"Bearer {new_token}"
                response = await client.get(f"{BASE_URL}/api/periods/cycle_analysis/", headers=headers)

                if response.status_code == 200:
                    # Retry after refreshing the token
                    analysis = response.json().get("data", {})
                    formatted_analysis = (
                        "📊 **Cycle Analysis Report**\n\n"
                        f"📅 **Average Cycle Length:** `{analysis.get('average_cycle', 'N/A')} days`\n"
                        f"📈 **Regularity Score:** `{analysis.get('regularity_score', 'N/A')}%`\n"
                        f"🔄 **Cycle Variations:** `{', '.join(map(str, analysis.get('cycle_variations', [])))}`\n"
                        f"🔮 **Prediction Reliability:** `{analysis.get('prediction_reliability', 'N/A')}%`\n"
                    )
                    await update.message.reply_text(formatted_analysis, parse_mode="Markdown")
                else:
                    await update.message.reply_text("❌ Failed to retrieve cycle analysis after refreshing the token.")
            else:
                await update.message.reply_text("❌ Session expired! Please log in again using /start.")

        else:
            await update.message.reply_text("❌ Failed to retrieve cycle analysis. Please try again later.")

