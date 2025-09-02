# handlers/login_handlers.py
from telegram import Update
from telegram.ext import ContextTypes
from states import LOGIN, MENU, PASSWORD
from menus import get_main_menu
from login import login_user
from languages import get_message
from utils import load_user_data, save_user_data  # تغییر نام توابع برای consistency


async def handle_login(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Step 1: Ask for password after username is entered."""
    lang = context.user_data.get("language", "en")
    username = update.message.text
    context.user_data["username"] = username

    # Ask for password (multi-language)
    await update.message.reply_text(get_message(lang, "auth", "enter_password"))
    return PASSWORD


async def handle_password(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Step 2: Verify password, save tokens and state, show main menu if success."""
    chat_id = str(update.message.chat_id)
    lang = context.user_data.get("language", "en")
    password = update.message.text
    username = context.user_data.get("username")

    access, refresh = await login_user(username, password)

    if access:
        user_data = load_user_data()

        user_data[chat_id] = {
            "access": access,
            "refresh": refresh,
            "state": MENU,
            "language": lang
        }
        save_user_data(user_data)

        context.bot_data['user_tokens'] = user_data

        menu_text, markup = get_main_menu(lang)
        await update.message.reply_text(menu_text, reply_markup=markup)

        context.user_data['state'] = MENU
        return MENU
    else:
        await update.message.reply_text(
            f"{get_message(lang, 'auth', 'login_failed')}\n{get_message(lang, 'auth', 'enter_username')}"
        )
        return LOGIN
