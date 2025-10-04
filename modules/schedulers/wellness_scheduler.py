import logging
from pathlib import Path
from telegram.ext import ContextTypes
# Need to ensure these imports are present in the actual file:
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, WebAppInfo

from constants import DASHBOARD, WELLNESS
from modules.users.handlers import show_dashboard
from modules.wellness.api import send_wellness
from utils.token_store import get_token 

logger = logging.getLogger(__name__)
USER_TOKENS_FILE = Path("./data/user_tokens.json")

async def handle_webapp_data(update: Update, context: ContextTypes.DEFAULT_TYPE):

    chat_id = update.effective_chat.id
    token = context.user_data.get("token") or get_token(chat_id)
    
    if not token:
        await update.message.reply_text("Please login first.")
        return DASHBOARD

    if update.message.web_app_data:
        data = update.message.web_app_data.data
        print(data)
        # parse JSON and save to DB
        import json
        wellness_data = json.loads(data)
        chat_id = update.effective_chat.id
        logger.info(f"Received wellness data from {chat_id}: {wellness_data}")

        chat_id = update.effective_chat.id
        token = context.user_data.get("token") or get_token(chat_id)

        if not token:
            await update.message.reply_text("❌ No token found. Please login first.")
            return await show_dashboard(update, context)
        
        
        response = await send_wellness(token=token, **wellness_data)
        if "error" in response:
            await update.message.reply_text(f"⚠️ Failed to submit wellness data: {response['error']}")
            return await show_dashboard(update, context)
        else:
            await update.message.reply_text("✅ Wellness form submitted successfully!")
            logger.info(f"API response for {chat_id}: {response}")
            await update.message.reply_text(
                "Back to dashboard:",
                reply_markup=ReplyKeyboardRemove()
            )
            return await show_dashboard(update, context)
        
        
async def wellness_checkin_callback(context: ContextTypes.DEFAULT_TYPE):
    """Send a web-app button + back button to all users for wellness check-in."""
    logger.info("Running wellness_checkin_callbacksssssssssss")

   

    users = context.application.bot_data.get("users", set())

    for chat_id in users:
        try:
            # WebApp button
            web_app_button = KeyboardButton(
                text="📝 Fill Daily Wellness Form",
                web_app=WebAppInfo(url="https://calendar.shirpala.ir/wellness")
            )

            # Back button (just a text button)
            back_button = KeyboardButton(text="⬅️ Back to Dashboard")

            # Two rows: one for WebApp, one for Back
            keyboard = [
                [web_app_button],
                [back_button]
            ]

            reply_markup = ReplyKeyboardMarkup(
                keyboard,
                resize_keyboard=True,
                one_time_keyboard=True
            )

            text=(
                "👋 Time for your daily wellness check-in!\n\n"
                "📝 *Fill Daily Wellness Form*: Opens the web form to log today’s wellness.\n"
                "⬅️ *Back to Dashboard*: Return to your main menu."
            )
            await context.bot.send_message(
                chat_id=chat_id,
                text=text,
                reply_markup=reply_markup
            )
            logger.info(f"Sent wellness WebApp button + back button to {chat_id}")
            return WELLNESS
        except Exception as e:
            logger.error(f"Failed to send wellness check-in to {chat_id}: {e}")
            return WELLNESS


async def handle_webapp_router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    token = context.user_data.get("token") or get_token(chat_id)
    
    if not token:
        await update.message.reply_text("Please login first.")
        return DASHBOARD


    if not update.message.web_app_data:
        return

    import json
    raw_data = update.message.web_app_data.data
    try:
        payload = json.loads(raw_data)
    except Exception:
        await update.message.reply_text("⚠️ Invalid data received.")
        return

    if isinstance(payload, dict) and payload.get("type") == "date":
        print("1")
        from modules.periods.handlers import handle_period_date
        return await handle_period_date(update, context)

    else:
        print("2")
        from modules.schedulers.wellness_scheduler import handle_webapp_data
        return await handle_webapp_data(update, context)
