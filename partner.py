from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext
from languages import get_message
from states import MENU, PARTNER_MENU, PARTNER_MESSAGE

async def show_partner_menu(update: Update, context: CallbackContext) -> int:
    """Display partner menu."""
    lang = context.user_data.get('language', 'en')
    
    reply_keyboard = [
        [get_message(lang, 'partner', 'view_partner_cycles'), 
         get_message(lang, 'partner', 'partner_analysis')],
        [get_message(lang, 'partner', 'send_message'), 
         get_message(lang, 'partner', 'partner_notifications')],
        [get_message(lang, 'partner', 'partner_settings')],
        [get_message(lang, 'settings', 'back_to_main')]
    ]
    
    await update.message.reply_text(
        get_message(lang, 'partner', 'menu'),
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )
    return PARTNER_MENU

async def handle_partner_menu(update: Update, context: CallbackContext) -> int:
    """Handle partner menu selections."""
    text = update.message.text
    lang = context.user_data.get('language', 'en')
    
    if text == get_message(lang, 'settings', 'back_to_main'):
        from bot import show_main_menu
        return await show_main_menu(update, context)
    elif text == get_message(lang, 'partner', 'view_partner_cycles'):
        return await view_partner_cycles(update, context)
    elif text == get_message(lang, 'partner', 'partner_analysis'):
        return await partner_analysis(update, context)
    elif text == get_message(lang, 'partner', 'send_message'):
        return await start_partner_message(update, context)
    elif text == get_message(lang, 'partner', 'partner_notifications'):
        return await partner_notifications(update, context)
    elif text == get_message(lang, 'partner', 'partner_settings'):
        return await partner_settings(update, context)
    
    return PARTNER_MENU

async def view_partner_cycles(update: Update, context: CallbackContext) -> int:
    """View partner's cycle history."""
    lang = context.user_data.get('language', 'en')
    # Add API call to fetch partner's cycles
    await update.message.reply_text(get_message(lang, 'partner', 'coming_soon'))
    return PARTNER_MENU

async def partner_analysis(update: Update, context: CallbackContext) -> int:
    """View partner's cycle analysis."""
    lang = context.user_data.get('language', 'en')
    # Add API call to fetch partner's analysis
    await update.message.reply_text(get_message(lang, 'partner', 'coming_soon'))
    return PARTNER_MENU

async def start_partner_message(update: Update, context: CallbackContext) -> int:
    """Start the process of sending a message to partner."""
    lang = context.user_data.get('language', 'en')
    await update.message.reply_text(
        get_message(lang, 'partner', 'enter_message'),
        reply_markup=ReplyKeyboardMarkup([[get_message(lang, 'settings', 'back_to_main')]], 
                                      one_time_keyboard=True)
    )
    return PARTNER_MESSAGE

async def partner_notifications(update: Update, context: CallbackContext) -> int:
    """Manage partner notifications."""
    lang = context.user_data.get('language', 'en')
    # Add notification settings logic
    await update.message.reply_text(get_message(lang, 'partner', 'coming_soon'))
    return PARTNER_MENU

async def partner_settings(update: Update, context: CallbackContext) -> int:
    """Manage partner settings."""
    lang = context.user_data.get('language', 'en')
    # Add partner settings logic
    await update.message.reply_text(get_message(lang, 'partner', 'coming_soon'))
    return PARTNER_MENU 