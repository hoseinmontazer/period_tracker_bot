import logging
import aiohttp
from telegram import Update, ReplyKeyboardMarkup, CallbackQuery
from telegram.ext import (
    Application, CommandHandler, MessageHandler, filters, 
    ConversationHandler, CallbackContext, CallbackQueryHandler
)
from auth import authenticate_user, handle_registration
from period import fetch_periods
from cycle_analysis import fetch_cycle_analysis as cycle_analysis_handler
from add_cycle import (
    add_cycle_conversation, 
    start_add_cycle,
    handle_calendar_selection,
    handle_symptoms,
    handle_medication
)
from utils import load_tokens, save_tokens
from settings import show_settings_menu, handle_settings
import config
from states import (
    REGISTER, LOGIN, PERIOD_TRACKING, MENU, ACCEPTING_INVITATION, 
    SETTINGS, START_DATE, SYMPTOMS, MEDICATION, PARTNER_MENU
)
from languages import get_message, SYMPTOM_OPTIONS, MEDICATION_OPTIONS
from invitation import generate_invitation_code, start_accept_invitation, accept_invitation
from partner import (
    show_partner_menu, 
    handle_partner_menu, 
    handle_partner_message
)
from calendar_keyboard import CalendarKeyboard
from menu_handlers import (
    start, show_main_menu, handle_menu, 
    handle_initial_choice, cancel
)

# Enhanced logging setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Load user tokens
user_tokens = load_tokens()
logger.info("User tokens loaded")

# At the top of the file, add MENU to the exports
__all__ = ['MENU', 'show_main_menu']

# Add this near the top of the file, after the imports
calendar = CalendarKeyboard()  # Create global calendar instance

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
        # Update bot_data with new tokens
        context.bot_data['user_tokens'] = user_tokens
        return await show_main_menu(update, context)

    await update.message.reply_text("❌ Login failed. Please try again.")
    return REGISTER

async def logout(update: Update, context: CallbackContext) -> int:
    """Logout user and remove token."""
    chat_id = str(update.message.chat_id)

    if chat_id in user_tokens:
        del user_tokens[chat_id]
        save_tokens(user_tokens)
        # Update bot_data after logout
        context.bot_data['user_tokens'] = user_tokens
        await update.message.reply_text("You have been logged out. Use /start to log in again.")
    else:
        await update.message.reply_text("You are not logged in.")

    return ConversationHandler.END

async def view_history(update: Update, context: CallbackContext) -> int:
    """Handle 'View History' - Fetch and display periods."""
    chat_id = str(update.message.chat_id)
    lang = context.user_data.get('language', 'en')
    
    if chat_id in user_tokens and "access" in user_tokens[chat_id]:
        await fetch_periods(update, context)
        return MENU
    else:
        await update.message.reply_text(get_message(lang, 'auth', 'login_required'))
        return REGISTER

async def cycle_analysis_handler(update: Update, context: CallbackContext) -> int:
    """Handle 'Cycle Analysis' - Fetch and display cycle analysis."""
    chat_id = str(update.message.chat_id)

    if chat_id not in user_tokens or "access" not in user_tokens[chat_id]:
        await update.message.reply_text("⚠️ You need to log in first. Use /start.")
        return MENU

    access_token = user_tokens[chat_id]["access"]
    await fetch_cycle_analysis(update, access_token)

    return MENU  # Return to menu after displaying analysis

def main():
    """Start the Telegram bot."""
    logger.info("Initializing bot...")
    application = Application.builder().token(config.TELEGRAM_BOT_TOKEN).build()
    logger.info("Bot application created")

    # Add handlers with logging
    logger.info("Adding conversation handlers...")
    
    # Add the add_cycle_conversation handler
    application.add_handler(add_cycle_conversation, group=0)
    logger.info("Added add_cycle_conversation handler")

    # Main conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            REGISTER: [
                MessageHandler(
                    filters.Regex(f'^({get_message("en", "auth", "register")}|{get_message("fa", "auth", "register")}|'
                                f'{get_message("en", "auth", "login")}|{get_message("fa", "auth", "login")})$'),
                    handle_initial_choice
                ),
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_registration)
            ],
            LOGIN: [MessageHandler(filters.TEXT & ~filters.COMMAND, login)],
            PERIOD_TRACKING: [MessageHandler(filters.TEXT & ~filters.COMMAND, authenticate)],
            MENU: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_menu)],
            SETTINGS: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_settings)],
            PARTNER_MENU: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_partner_menu)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
        allow_reentry=True,
        name="main_conversation"
    )
    logger.info("Created main conversation handler")

    # Add main conversation handler
    application.add_handler(conv_handler, group=1)
    logger.info("Added main conversation handler")

    # Add error handler
    application.add_error_handler(error_handler)
    logger.info("Added error handler")
    
    # Add logout handler
    application.add_handler(CommandHandler('logout', logout))
    logger.info("Added logout handler")

    logger.info("Bot initialization complete. Starting polling...")
    application.run_polling()

async def error_handler(update: Update, context: CallbackContext) -> None:
    """Log Errors caused by Updates."""
    logger.error("Exception while handling an update:", exc_info=context.error)
    
    if update:
        if update.message:
            chat_id = update.message.chat_id
            message_text = update.message.text
            logger.error(f"Error in chat {chat_id}")
            logger.error(f"Message text: {message_text}")
            logger.error(f"User data: {context.user_data}")
        elif update.callback_query:
            chat_id = update.callback_query.message.chat_id
            callback_data = update.callback_query.data
            logger.error(f"Error in chat {chat_id}")
            logger.error(f"Callback data: {callback_data}")
            logger.error(f"User data: {context.user_data}")
    
    # Log the full error traceback
    logger.exception("Full error traceback:")

if __name__ == "__main__":
    logger.info("Starting bot application...")
    main()

