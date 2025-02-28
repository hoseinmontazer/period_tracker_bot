from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import CallbackContext, ConversationHandler
from languages import get_message
from states import MENU, REGISTER, LOGIN, PERIOD_TRACKING
import logging
import httpx
from utils import load_tokens, save_tokens, refresh_token
from config import BASE_URL

logger = logging.getLogger(__name__)

async def start(update: Update, context: CallbackContext) -> int:
    """Start the bot and check if the user is logged in."""
    chat_id = str(update.message.chat_id)
    context.user_data['language'] = context.user_data.get('language', 'en')
    lang = context.user_data['language']
    
    logger.info(f"Starting bot for chat_id: {chat_id}")
    
    # Get user_tokens from bot_data
    user_tokens = load_tokens()
    
    # Check if user has valid token
    if chat_id in user_tokens and "access" in user_tokens[chat_id]:
        logger.info(f"Found existing token for chat_id: {chat_id}")
        # Try to use the token to verify it's still valid
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{BASE_URL}/api/users/me/",
                    headers={"Authorization": f"Bearer {user_tokens[chat_id]['access']}"}
                )
                
                if response.status_code == 200:
                    logger.info("Token is valid, showing main menu")
                    return await show_main_menu(update, context)
                else:
                    logger.warning("Token is invalid, trying refresh")
                    # Try to refresh the token
                    new_token = await refresh_token(chat_id, user_tokens)
                    if new_token:
                        logger.info("Token refreshed successfully")
                        return await show_main_menu(update, context)
                    
        except Exception as e:
            logger.error(f"Error checking token: {str(e)}")
    
    # If no valid token found, show login/register options
    logger.info("No valid token found, showing login/register options")
    reply_keyboard = [
        [get_message(lang, 'auth', 'register'), get_message(lang, 'auth', 'login')]
    ]
    
    await update.message.reply_text(
        get_message(lang, 'welcome', 'bot'),
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )
    return REGISTER

async def show_main_menu(update: Update, context: CallbackContext) -> int:
    """Display the main menu."""
    lang = context.user_data.get('language', 'en')
    
    # Create menu buttons with exact text
    reply_keyboard = [
        [get_message(lang, 'menu', 'track_period'), 
         get_message(lang, 'menu', 'view_history')],
        [get_message(lang, 'menu', 'cycle_analysis'), 
         get_message(lang, 'menu', 'add_new_cycle')],
        ["👥 Partner Menu" if lang == 'en' else "👥 منوی شریک"],  # Direct text
        [get_message(lang, 'settings', 'menu')]
    ]

    await update.message.reply_text(
        get_message(lang, 'menu', 'main'),
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard,
            one_time_keyboard=True,
            resize_keyboard=True
        ),
        parse_mode="Markdown"
    )
    return MENU

async def handle_menu(update: Update, context: CallbackContext) -> int:
    """Handle main menu selections."""
    text = update.message.text
    lang = context.user_data.get('language', 'en')
    
    # Log the received text and expected partner menu text
    logger.info(f"Received menu text: '{text}'")
    logger.info(f"Expected partner menu text: '{get_message(lang, 'menu', 'partner_menu')}'")
    
    if text == get_message(lang, 'menu', 'add_new_cycle'):
        from add_cycle import start_add_cycle
        return await start_add_cycle(update, context)
    elif text == get_message(lang, 'menu', 'view_history'):
        from period import fetch_periods
        await fetch_periods(update, context)
        return MENU
    elif text == get_message(lang, 'menu', 'cycle_analysis'):
        from cycle_analysis import fetch_cycle_analysis
        return await fetch_cycle_analysis(update, context)
    elif text == "👥 Partner Menu" or text == "👥 منوی شریک":  # Direct text comparison
        from partner import show_partner_menu
        return await show_partner_menu(update, context)
    elif text == get_message(lang, 'settings', 'menu'):
        from settings import show_settings_menu
        return await show_settings_menu(update, context)
    elif text == get_message(lang, 'menu', 'logout'):
        from auth import logout
        return await logout(update, context)
    
    # Log unhandled menu option
    logger.warning(f"Unhandled menu option: '{text}'")
    return MENU

async def handle_initial_choice(update: Update, context: CallbackContext) -> int:
    """Handle the initial Register/Login choice."""
    choice = update.message.text
    lang = context.user_data.get('language', 'en')
    chat_id = str(update.message.chat_id)
    
    # Check if user is already logged in
    user_tokens = context.bot_data.get('user_tokens', {})
    if chat_id in user_tokens and "access" in user_tokens[chat_id]:
        return await show_main_menu(update, context)
    
    if choice == get_message(lang, 'auth', 'register'):
        # Clear any existing registration data
        context.user_data.clear()
        context.user_data['language'] = lang
        await update.message.reply_text(get_message(lang, 'auth', 'enter_username'))
        context.user_data['registration_step'] = 'username'
        return REGISTER
    elif choice == get_message(lang, 'auth', 'login'):
        await update.message.reply_text(get_message(lang, 'auth', 'enter_username'))
        return LOGIN
    
    return REGISTER

async def cancel(update: Update, context: CallbackContext) -> int:
    """Cancel and end the conversation."""
    lang = context.user_data.get('language', 'en')
    await update.message.reply_text(
        get_message(lang, 'errors', 'operation_cancelled'),
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END 