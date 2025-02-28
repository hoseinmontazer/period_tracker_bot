from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext, ConversationHandler
from languages import get_message
from states import MENU, SETTINGS

async def show_settings_menu(update: Update, context: CallbackContext) -> int:
    """Display settings menu."""
    lang = context.user_data.get('language', 'en')
    
    reply_keyboard = [
        [get_message(lang, 'menu', 'invitation_partner'), get_message(lang, 'menu', 'accept_invitation')],
        ['🇬🇧 English', '🇮🇷 فارسی'],
        [get_message(lang, 'menu', 'logout')],
        [get_message(lang, 'settings', 'back_to_main')]
    ]
    
    await update.message.reply_text(
        get_message(lang, 'settings', 'menu'),
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )
    return SETTINGS

async def handle_settings(update: Update, context: CallbackContext) -> int:
    """Handle settings menu selections."""
    text = update.message.text
    lang = context.user_data.get('language', 'en')
    
    if text == get_message(lang, 'settings', 'back_to_main'):
        from bot import show_main_menu
        return await show_main_menu(update, context)
    elif text == '🇬🇧 English':
        context.user_data['language'] = 'en'
        await update.message.reply_text(get_message('en', 'menu', 'language_changed'))
        return await show_settings_menu(update, context)
    elif text == '🇮🇷 فارسی':
        context.user_data['language'] = 'fa'
        await update.message.reply_text(get_message('fa', 'menu', 'language_changed'))
        return await show_settings_menu(update, context)
    elif text == get_message(lang, 'menu', 'invitation_partner'):
        return await generate_invitation_code(update, context)
    elif text == get_message(lang, 'menu', 'accept_invitation'):
        return await start_accept_invitation(update, context)
    elif text == get_message(lang, 'menu', 'logout'):
        from bot import logout
        return await logout(update, context)
    
    return SETTINGS 