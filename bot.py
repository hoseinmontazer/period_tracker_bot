# bot.py
import os, logging
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler
from dotenv import load_dotenv
from states import REGISTER, LOGIN, PASSWORD, MENU, ADD_CYCLE_DATE
from handlers.main_handlers import handle_initial_choice, handle_menu, cancel
from handlers.login_handlers import handle_login, handle_password
from languages import get_message
from telegram import Update, ReplyKeyboardMarkup
from utils import load_user_data, save_user_data
from menus import get_main_menu
from telegram.ext import ContextTypes
from handlers.cycle.cycle_handlers import handle_add_new_cycle


load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# -------------------
# Restore user state before any handler
# -------------------
async def restore_user_state(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        chat_id = str(update.message.chat_id)
        user_data = load_user_data()
        if chat_id in user_data:
            context.user_data['state'] = user_data[chat_id].get('state', REGISTER)
            context.user_data['username'] = user_data[chat_id].get('username')
            context.user_data['language'] = user_data[chat_id].get('language', 'en')

            # اگر قبلاً در منوی اصلی بوده، منو را نمایش بده
            if context.user_data['state'] == MENU:
                menu_text, markup = get_main_menu(context.user_data['language'])
                await update.message.reply_text(menu_text, reply_markup=markup)
        else:
            context.user_data['state'] = REGISTER
            context.user_data['language'] = 'en'

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
        menu_text, markup = get_main_menu(lang)
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
    bot_tokens = {chat_id: {"access": info["access"], "refresh": info.get("refresh")} 
                  for chat_id, info in user_data.items() if "access" in info}
    application.bot_data['user_tokens'] = bot_tokens


    # Conversation handler FIRST (add to group 0)
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            REGISTER: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_initial_choice)],
            LOGIN: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_login)],
            PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_password)],
            MENU: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_menu)],
            ADD_CYCLE_DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_add_new_cycle)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
        allow_reentry=True
    )


    application.add_handler(conv_handler, group=0)  # Add to group 0

    # Restore user state in a DIFFERENT group (group 1)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, restore_user_state), group=1)

    logger.info("Bot is starting...")
    application.run_polling()

if __name__ == "__main__":
    main()
