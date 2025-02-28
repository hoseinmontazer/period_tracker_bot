# cycle_analysis.py

import httpx
from utils import load_tokens, refresh_token  # These utilities should work as expected
from config import BASE_URL
from telegram import Update
from telegram.ext import CallbackContext
from bot import get_message
from states import MENU
from languages import get_message

async def fetch_cycle_analysis(update: Update, context: CallbackContext) -> None:
    """Fetch and display cycle analysis data."""
    chat_id = str(update.message.chat_id)
    lang = context.user_data.get('language', 'en')
    
    # Get access token from user_tokens
    from bot import user_tokens
    if chat_id not in user_tokens or "access" not in user_tokens[chat_id]:
        await update.message.reply_text(get_message(lang, 'auth', 'login_required'))
        return MENU

    access_token = user_tokens[chat_id]["access"]
    headers = {"Authorization": f"Bearer {access_token}"}

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{BASE_URL}/api/periods/cycle_analysis/",
                headers=headers
            )

            if response.status_code == 200:
                data = response.json()['data']
                
                # Format the analysis message
                analysis_message = (
                    "📊 *Your Cycle Analysis*\n\n"
                    f"📅 Next Predicted Period: *{data['next_predicted_date']}*\n"
                    f"⏱ Average Cycle Length: *{data['average_cycle']} days*\n"
                    f"📈 Regularity Score: *{data['regularity_score']}%*\n"
                    f"🎯 Prediction Reliability: *{data['prediction_reliability']}%*\n"
                    f"🔄 Cycle Variations: *{', '.join(map(str, data['cycle_variations']))} days*"
                )
                
                await update.message.reply_text(
                    analysis_message,
                    parse_mode="Markdown"
                )
            else:
                await update.message.reply_text(get_message(lang, 'errors', 'fetch_failed'))
                
    except Exception as e:
        await update.message.reply_text(get_message(lang, 'errors', 'fetch_failed'))
        
    return MENU

