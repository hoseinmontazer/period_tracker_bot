# handlers/main_handlers.py

from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ContextTypes, CallbackContext
from states import REGISTER, LOGIN, MENU, ADD_CYCLE_DATE
from languages import get_message
from menus import get_main_menu
from handlers.cycle.cycle_handlers import handle_add_new_cycle
import os, logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def handle_initial_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle the initial Register/Login choice."""
    lang = context.user_data.get("language", "en")
    choice = update.message.text

    if choice.lower() == get_message(lang, "auth", "register").lower():
        await update.message.reply_text(get_message(lang, "auth", "enter_username"))
        return REGISTER
    elif choice.lower() == get_message(lang, "auth", "login").lower():
        await update.message.reply_text(get_message(lang, "auth", "enter_username"))
        return LOGIN
    else:
        await update.message.reply_text(get_message(lang, "welcome", "choose_option"))
        return REGISTER
    
async def handle_menu(update: Update, context: CallbackContext) -> int:
    """Handle main menu selections."""
    text = update.message.text
    lang = context.user_data.get('language', 'en')
    print(f"User selected menu option: {text}")
    if text == get_message(lang, 'menu', 'add_new_cycle'):
        from .cycle.cycle_handlers import handle_add_new_cycle
        return await handle_add_new_cycle(update, context)


    return MENU





async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancel the conversation."""
    lang = context.user_data.get("language", "en")
    cancel_text = get_message(lang, "errors", "operation_cancelled")  

    await update.message.reply_text(
        cancel_text,
        reply_markup=ReplyKeyboardRemove()
    )
    return -1 
