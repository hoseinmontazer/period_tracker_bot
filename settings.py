from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext
from languages import get_message
from states import MENU

async def show_settings_menu(update: Update, context: CallbackContext) -> int:
    """Display settings menu."""
    lang = context.user_data.get('language', 'en')
    
    reply_keyboard = [
        [get_message(lang, 'settings', 'change_language')],
        [get_message(lang, 'settings', 'back_to_main')]
    ]
    
    await update.message.reply_text(
        get_message(lang, 'settings', 'menu'),
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )
    return MENU 