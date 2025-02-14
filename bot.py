import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, MessageHandler, filters, 
    ConversationHandler, CallbackContext
)
from auth import authenticate_user
from period import fetch_periods
from cycle_analysis import fetch_cycle_analysis
from add_cycle import add_cycle_conversation, start_add_cycle
from utils import load_tokens, save_tokens
import config
from states import REGISTER, LOGIN, PERIOD_TRACKING, MENU

# Logging setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Load user tokens
user_tokens = load_tokens()

# At the top of the file, add MENU to the exports
__all__ = ['MENU', 'show_main_menu']

async def start(update: Update, context: CallbackContext) -> int:
    """Start the bot and check if the user is logged in."""
    chat_id = str(update.message.chat_id)

    if chat_id in user_tokens and "access" in user_tokens[chat_id]:
        return await show_main_menu(update)

    reply_keyboard = [['Register', 'Login']]
    await update.message.reply_text(
        "Welcome to Period Tracker Bot! Please choose an option:",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )
    return REGISTER

async def show_main_menu(update: Update) -> int:
    """Displays the main menu with available options."""
    reply_keyboard = [
        ['Track Period', 'View History'],
        ['Cycle Analysis', 'Add New Cycle'],
        ['Logout']
    ]
    await update.message.reply_text(
        "📋 **Main Menu**\nChoose an option:",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
        parse_mode="Markdown"
    )
    return MENU

async def register(update: Update, context: CallbackContext) -> int:
    """Handle user registration."""
    await update.message.reply_text("Enter your username:")
    return LOGIN

async def login(update: Update, context: CallbackContext) -> int:
    """Handle user login."""
    context.user_data['username'] = update.message.text
    await update.message.reply_text("Enter your password:")
    return PERIOD_TRACKING

async def authenticate(update: Update, context: CallbackContext) -> int:
    """Authenticate user and store token."""
    username = context.user_data['username']
    password = update.message.text

    token = await authenticate_user(username, password)
    chat_id = str(update.message.chat_id)

    if token:
        user_tokens[chat_id] = {"access": token}
        save_tokens(user_tokens)
        return await show_main_menu(update)

    await update.message.reply_text("❌ Login failed. Please try again.")
    return REGISTER

async def logout(update: Update, context: CallbackContext) -> int:
    """Logout user and remove token."""
    chat_id = str(update.message.chat_id)

    if chat_id in user_tokens:
        del user_tokens[chat_id]
        save_tokens(user_tokens)
        await update.message.reply_text("You have been logged out. Use /start to log in again.")
    else:
        await update.message.reply_text("You are not logged in.")

    return ConversationHandler.END

async def view_history(update: Update, context: CallbackContext) -> int:
    """Handle 'View History' - Fetch and display periods."""
    chat_id = str(update.message.chat_id)

    if chat_id not in user_tokens or "access" not in user_tokens[chat_id]:
        await update.message.reply_text("⚠️ You need to log in first. Use /start.")
        return MENU

    access_token = user_tokens[chat_id]["access"]
    await fetch_periods(update, access_token)

    return MENU  # Return to menu after displaying history

async def cycle_analysis_handler(update: Update, context: CallbackContext) -> int:
    """Handle 'Cycle Analysis' - Fetch and display cycle analysis."""
    chat_id = str(update.message.chat_id)

    if chat_id not in user_tokens or "access" not in user_tokens[chat_id]:
        await update.message.reply_text("⚠️ You need to log in first. Use /start.")
        return MENU

    access_token = user_tokens[chat_id]["access"]
    await fetch_cycle_analysis(update, access_token)

    return MENU  # Return to menu after displaying analysis

async def cancel(update: Update, context: CallbackContext) -> int:
    """Handle canceling the operation and end the conversation."""
    await update.message.reply_text("Operation cancelled.")
    return ConversationHandler.END

def main():
    """Start the Telegram bot."""
    application = Application.builder().token(config.TELEGRAM_BOT_TOKEN).build()

    # Add the add_cycle_conversation handler FIRST
    application.add_handler(add_cycle_conversation)

    # Then add the main conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            REGISTER: [MessageHandler(filters.TEXT & ~filters.COMMAND, register)],
            LOGIN: [MessageHandler(filters.TEXT & ~filters.COMMAND, login)],
            PERIOD_TRACKING: [MessageHandler(filters.TEXT & ~filters.COMMAND, authenticate)],
            MENU: [
                MessageHandler(filters.Regex("^Track Period$"), view_history),
                MessageHandler(filters.Regex("^View History$"), view_history),
                MessageHandler(filters.Regex("^Cycle Analysis$"), cycle_analysis_handler),
                MessageHandler(filters.Regex("^Add New Cycle$"), start_add_cycle),
                MessageHandler(filters.Regex("^Logout$"), logout),
            ],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    application.add_handler(conv_handler)
    application.add_handler(CommandHandler('logout', logout))

    application.run_polling()

if __name__ == "__main__":
    main()

