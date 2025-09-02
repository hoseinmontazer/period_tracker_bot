# bot.py
import os, logging
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler, CallbackContext
from dotenv import load_dotenv
from handlers.cycle import cycle_analysis
from handlers.setting.setting import handle_settings
from handlers.profile.profile import handle_profile, start_profile
from states import CYCLE_ANALYSIS_MENU, LANGUAGE_SELECTION, PROFILE_MENU, REGISTER, LOGIN, PASSWORD, MENU, ADD_CYCLE_DATE , HISTORY, SETTINGS, ViewProfile
from handlers.login_handlers import handle_login, handle_password
from languages import get_message
from telegram import Update, ReplyKeyboardMarkup
from utils import load_user_data, save_user_data
from menus import get_main_menu,handle_initial_choice, handle_menu, cancel
from telegram.ext import ContextTypes 
from config import TELEGRAM_BOT_TOKEN
from handlers.cycle.add_cycle_handlers import add_cycle_conversation, start_add_cycle
# from handlers.setting.setting import settings_conversation, start_settings
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# -------------------
# Restore user state before any handler
# -------------------
async def restore_user_state(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data = context.user_data
    last_state = user_data.get("last_state", "menu")  
    if last_state == "menu":
        return await handle_menu(update, context)

    elif last_state == "add_cycle":
        return await start_add_cycle(update, context)

    else:
        return await handle_menu(update, context)


# -------------------
# Start command
# -------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    chat_id = str(update.message.chat_id)
    lang = context.user_data.get("language", "en")

    # Load user data
    user_data = load_user_data()

    if chat_id in user_data and "access" in user_data[chat_id]:
        # User logged in → show main menu
        markup, menu_text = get_main_menu(lang)
        await update.message.reply_text(menu_text, reply_markup=markup)

        context.user_data['state'] = MENU
        return MENU
    else:
        reply_keyboard = [
            [get_message(lang, "auth", "register"), get_message(lang, "auth", "login")]
        ]
        await update.message.reply_text(
            get_message(lang, "welcome", "choose_option"),
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True)
        )
        context.user_data['state'] = REGISTER
        return REGISTER






# -------------------
# Save state and tokens
# -------------------
def save_state(chat_id: str, context: ContextTypes.DEFAULT_TYPE):
    user_data = load_user_data()
    data = {
        "access": context.bot_data.get('user_tokens', {}).get(chat_id, {}).get('access'),
        "refresh": context.bot_data.get('user_tokens', {}).get(chat_id, {}).get('refresh'),
        "state": context.user_data.get('state'),
        "username": context.user_data.get('username'),
        "language": context.user_data.get('language', 'en')
    }
    user_data[chat_id] = data
    save_user_data(user_data)

# -------------------
# Main
# -------------------
def main():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Load user tokens
    user_data = load_user_data()
    bot_tokens = {
        chat_id: {"access": info["access"], "refresh": info.get("refresh")}
        for chat_id, info in user_data.items() if "access" in info
    }
    application.bot_data['user_tokens'] = bot_tokens

    # Main conversation (register/login/menu)
    main_conv = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            REGISTER: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_initial_choice)],
            LOGIN: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_login)],
            PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_password)],
            MENU: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_menu)],
            SETTINGS: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_settings)],  # Add this
            LANGUAGE_SELECTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_settings)],  # Add this
            HISTORY: [MessageHandler(filters.TEXT & ~filters.COMMAND, restore_user_state)],
            ADD_CYCLE_DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, restore_user_state)],  
            PROFILE_MENU: [MessageHandler(filters.TEXT & ~filters.COMMAND, start_profile)],
            ViewProfile: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_profile)],
            # cycle analysis state
            CYCLE_ANALYSIS_MENU: [MessageHandler(filters.TEXT & ~filters.COMMAND, cycle_analysis)],
            
        },
        fallbacks=[CommandHandler("cancel", cancel)],
        name="main_conversation",
        conversation_timeout=300,
        allow_reentry=True
    )
    application.add_handler(main_conv, group=0)

    # Add Cycle conversation
    application.add_handler(add_cycle_conversation, group=1)

    # application.add_handler(settings_conversation)
    
    # Global catch-all
    application.add_handler(
        MessageHandler(
            filters.TEXT 
            & ~filters.COMMAND 
            & ~filters.Regex("^(📜 View History|مشاهده تاریخچه)$"),
            restore_user_state
        ),
        group=1
    )

    logger.info("Bot is starting...")
    application.run_polling()


if __name__ == "__main__":
    main()
