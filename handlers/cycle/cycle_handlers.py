import httpx
from config import PERIODS_API
from languages import get_message
from menus import get_main_menu
from utils import load_user_data
from telegram import Update
from telegram.ext import ContextTypes   , CallbackContext
import logging 
from states import MENU


# cycle_handlers.py
async def handle_add_new_cycle(update: Update, context: CallbackContext) -> int:
    print("handle_add_new_cycle called")
    """Handle the actual adding of the cycle after date input."""
    lang = context.user_data.get("language", "en")
    chat_id = str(update.message.chat_id)
    start_date = update.message.text.strip()

    user_data = load_user_data()
    token = user_data.get(chat_id, {}).get("access")
    if not token:
        await update.message.reply_text(get_message(lang, "auth", "login_first"))
        return MENU

    headers = {"Authorization": f"Bearer {token}"}
    data = {"start_date": start_date}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(PERIODS_API, headers=headers, data=data)
            if response.status_code == 201:
                await update.message.reply_text(get_message(lang, "cycle", "cycle_added"))
            else:
                await update.message.reply_text(f"{get_message(lang, 'cycle', 'add_failed')} ({response.status_code})")
        except Exception as e:
            await update.message.reply_text(f"{get_message(lang, 'cycle', 'add_failed')}: {e}")

    # بعد از ثبت، منو اصلی را فقط یک بار نشان بده
    menu_text, markup = get_main_menu(lang)
    await update.message.reply_text(menu_text, reply_markup=markup)
    return MENU



