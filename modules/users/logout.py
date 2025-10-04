from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import ContextTypes

from constants import DASHBOARD, MAIN_MENU
from utils.token_store import remove_token




async def handle_logout_profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start a conversation to edit the user's profile step-by-step."""
    text = update.message.text
    print("handle_logout_profile text ---> " , text)

    if text == "🚪 Logout":
        keyboard = [
            ["Login", "Register"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)      
        await update.message.reply_text("You have been logged out successfully. See you next time! 👋",reply_markup=reply_markup )
        context.user_data.clear()  
        remove_token(update.effective_chat.id)
        return MAIN_MENU
    else:
        keyboard = [
            ["⬅️ Back to Dashboard"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)  
        await update.message.reply_text("Please Back to menu.", reply_markup=reply_markup)
        return MAIN_MENU
