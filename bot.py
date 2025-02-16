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
import aiohttp
from languages import get_message, SYMPTOM_OPTIONS, MEDICATION_OPTIONS

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
    context.user_data['language'] = context.user_data.get('language', 'en')  # Default to English

    if chat_id in user_tokens and "access" in user_tokens[chat_id]:
        return await show_main_menu(update, context)

    # Show login/register options
    lang = context.user_data.get('language', 'en')
    reply_keyboard = [
        [get_message(lang, 'auth', 'register'), get_message(lang, 'auth', 'login')]
    ]
    
    await update.message.reply_text(
        get_message(lang, 'welcome', 'bot'),
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )
    return REGISTER

async def show_main_menu(update: Update, context: CallbackContext) -> int:
    """Displays the main menu with available options."""
    lang = context.user_data.get('language', 'en')
    
    reply_keyboard = [
        [get_message(lang, 'menu', 'track_period'), get_message(lang, 'menu', 'view_history')],
        [get_message(lang, 'menu', 'cycle_analysis'), get_message(lang, 'menu', 'add_new_cycle')],
        ['🇬🇧 English' if lang == 'fa' else '🇮🇷 فارسی'],  # Language toggle button
        [get_message(lang, 'menu', 'logout')]
    ]

    await update.message.reply_text(
        get_message(lang, 'menu', 'main'),
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
        parse_mode="Markdown"
    )
    return MENU

async def handle_initial_choice(update: Update, context: CallbackContext) -> int:
    """Handle the initial Register/Login choice."""
    choice = update.message.text
    
    if choice == 'Register':
        # Clear any existing registration data
        context.user_data.clear()
        await update.message.reply_text("Please enter your username:")
        context.user_data['registration_step'] = 'username'
        return REGISTER
    elif choice == 'Login':
        await update.message.reply_text("Please enter your username:")
        return LOGIN
    
    return REGISTER

async def handle_registration(update: Update, context: CallbackContext) -> int:
    """Handle the registration process step by step."""
    current_step = context.user_data.get('registration_step', 'username')
    user_input = update.message.text
    
    if current_step == 'username':
        context.user_data['username'] = user_input
        await update.message.reply_text("Enter your password:")
        context.user_data['registration_step'] = 'password'
        return REGISTER
    
    elif current_step == 'password':
        context.user_data['password'] = user_input
        await update.message.reply_text("Enter your email address (e.g., example@gmail.com):")
        context.user_data['registration_step'] = 'email'
        return REGISTER
    
    elif current_step == 'email':
        if '@' not in user_input or '.' not in user_input:
            await update.message.reply_text("Please enter a valid email address (e.g., example@gmail.com):")
            return REGISTER
            
        # Make API call to register user
        try:
            async with aiohttp.ClientSession() as session:
                data = {
                    'username': context.user_data['username'],
                    'password': context.user_data['password'],
                    're_password': context.user_data['password'],
                    'email': user_input
                }
                logger.info(f"Attempting registration with data: {data}")
                
                async with session.post('https://api-period.shirpala.ir/api/auth/users/', data=data) as response:
                    response_text = await response.text()
                    logger.info(f"Registration response status: {response.status}")
                    logger.info(f"Registration response body: {response_text}")
                    
                    if response.status == 201:
                        await update.message.reply_text("Registration successful!")
                        # Auto-login the user
                        token = await authenticate_user(context.user_data['username'], context.user_data['password'])
                        if token:
                            chat_id = str(update.message.chat_id)
                            user_tokens[chat_id] = {"access": token}
                            save_tokens(user_tokens)
                            context.user_data.clear()
                            return await show_main_menu(update, context)
                        else:
                            await update.message.reply_text("Registration successful but login failed. Please use /start to login.")
                            return ConversationHandler.END
                    else:
                        error_msg = f"Registration failed. Server response: {response_text}"
                        logger.error(error_msg)
                        await update.message.reply_text(error_msg)
                        return REGISTER
                    
        except Exception as e:
            error_msg = f"Registration error: {str(e)}"
            logger.error(error_msg)
            await update.message.reply_text("An error occurred during registration. Please try again.")
            return REGISTER

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
        return await show_main_menu(update, context)

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

async def cancel(update: Update, context: CallbackContext) -> int:
    """Handle canceling the operation and end the conversation."""
    await update.message.reply_text("Operation cancelled.")
    return ConversationHandler.END

async def handle_menu(update: Update, context: CallbackContext) -> int:
    """Handle menu selections."""
    text = update.message.text
    lang = context.user_data.get('language', 'en')

    # Handle language change
    if text in ['🇬🇧 English', '🇮🇷 فارسی']:
        # Toggle language
        new_lang = 'en' if text == '🇬🇧 English' else 'fa'
        context.user_data['language'] = new_lang
        return await show_main_menu(update, context)

    # Handle other menu options
    if text == get_message(lang, 'menu', 'track_period'):
        return await view_history(update, context)
    elif text == get_message(lang, 'menu', 'view_history'):
        return await view_history(update, context)
    elif text == get_message(lang, 'menu', 'cycle_analysis'):
        return await cycle_analysis_handler(update, context)
    elif text == get_message(lang, 'menu', 'add_new_cycle'):
        return await start_add_cycle(update, context)
    elif text == get_message(lang, 'menu', 'logout'):
        return await logout(update, context)

    return MENU

def main():
    """Start the Telegram bot."""
    application = Application.builder().token(config.TELEGRAM_BOT_TOKEN).build()

    # Add the add_cycle_conversation handler FIRST
    application.add_handler(add_cycle_conversation)

    # Then add the main conversation handler
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
            MENU: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_menu)
            ],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    application.add_handler(conv_handler)
    application.add_handler(CommandHandler('logout', logout))

    application.run_polling()

if __name__ == "__main__":
    main()

