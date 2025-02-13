import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler, CallbackContext
from auth import authenticate_user, refresh_token
from period import fetch_periods
from cycle_analysis import fetch_cycle_analysis
from add_cycle import add_cycle_conversation  # Ensure this import is correct
from utils import load_tokens, save_tokens
import config

# States
REGISTER, LOGIN, PERIOD_TRACKING, MENU = range(4)

# Logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

user_tokens = load_tokens()

async def start(update: Update, context):
    """Check if user has a token. If yes, show menu, otherwise ask for login."""
    chat_id = str(update.message.chat_id)

    if chat_id in user_tokens and "access" in user_tokens[chat_id]:
        return await show_main_menu(update)

    reply_keyboard = [['Register', 'Login']]
    await update.message.reply_text(
        "Welcome to Period Tracker Bot! Please choose an option:",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )
    return REGISTER

async def show_main_menu(update: Update):
    """Displays the main menu with available options."""
    reply_keyboard = [['Track Period', 'View History'], ['Cycle Analysis', 'Add New Cycle'],['Logout']]
    await update.message.reply_text(
        "📋 **Main Menu**\nChoose an option:",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
        parse_mode="Markdown"
    )
    return MENU

async def register(update: Update, context):
    await update.message.reply_text("Enter your username:")
    return LOGIN

async def login(update: Update, context):
    context.user_data['username'] = update.message.text
    await update.message.reply_text("Enter your password:")
    return PERIOD_TRACKING

async def authenticate(update: Update, context):
    username = context.user_data['username']
    password = update.message.text

    token = await authenticate_user(username, password)

    if token:
        chat_id = str(update.message.chat_id)
        user_tokens[chat_id] = {"access": token}
        save_tokens(user_tokens)
        return await show_main_menu(update)

    await update.message.reply_text("❌ Login failed. Please try again.")
    return REGISTER

async def logout(update: Update, context):
    chat_id = str(update.message.chat_id)
    
    if chat_id in user_tokens:
        del user_tokens[chat_id]
        save_tokens(user_tokens)
        await update.message.reply_text("You have been logged out. Use /start to log in again.")
    else:
        await update.message.reply_text("You are not logged in.")

    return ConversationHandler.END

async def view_history(update: Update, context: CallbackContext) -> int:
    """Handles 'View History' button - Fetches and displays periods"""
    print("hi view_history")
    chat_id = str(update.message.chat_id)

    if chat_id not in user_tokens or "access" not in user_tokens[chat_id]:
        await update.message.reply_text("⚠️ You need to log in first. Use /start.")
        return MENU  # ✅ Ensure state transition

    access_token = user_tokens[chat_id]["access"]
    print(f"access_toks in bot.py view_history  is: {access_token}")
    await fetch_periods(update, access_token)

    return MENU  # ✅ Ensure the bot stays in the menu after displaying history


async def cycle_analysis_handler(update, context):
    print("hi cycle_analysis_handler")
    chat_id = str(update.message.chat_id)

    if chat_id not in user_tokens or "access" not in user_tokens[chat_id]:
        await update.message.reply_text("⚠️ You need to log in first. Use /start.")
        return MENU  # Ensure state transition

    access_token = user_tokens[chat_id]["access"]
    print(f"access_toks in bot.py cycle_analysis_handler  is: {access_token}")
    await fetch_cycle_analysis(update, access_token)

    return MENU  # Ensure the bot stays in the menu after displaying the analysis

# This function should trigger the conversation for adding a new cycle
async def add_new_cycle_handler(update: Update, context: CallbackContext) -> int:
    """Handles 'Add New Cycle' button."""
    # The correct way to trigger the conversation handler
    return await add_cycle_conversation.handle_update(update, context)

async def cancel(update: Update, context: CallbackContext) -> int:
    """Handles canceling the operation and ends the conversation."""
    await update.message.reply_text("Operation cancelled.")
    return ConversationHandler.END

def main():
    application = Application.builder().token(config.TELEGRAM_BOT_TOKEN).build()

    # This handler will be used for the "Add New Cycle" functionality
    application.add_handler(add_cycle_conversation)

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            REGISTER: [MessageHandler(filters.TEXT & ~filters.COMMAND, register)],
            LOGIN: [MessageHandler(filters.TEXT & ~filters.COMMAND, login)],
            PERIOD_TRACKING: [MessageHandler(filters.TEXT & ~filters.COMMAND, authenticate)],
            MENU: [
                MessageHandler(filters.Regex("^Track Period$"), fetch_periods),
                MessageHandler(filters.Regex("^View History$"), view_history),
                MessageHandler(filters.Regex("^Cycle Analysis$"), cycle_analysis_handler),
                MessageHandler(filters.Regex("^Add New Cycle$"), add_new_cycle_handler),
                MessageHandler(filters.Regex("^Logout$"), logout),
            ],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    application.add_handler(conv_handler)
    application.add_handler(CommandHandler('logout', logout))

    application.run_polling()

