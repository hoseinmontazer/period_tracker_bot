from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext
from languages import get_message
from states import MENU, SETTINGS

async def show_settings_menu(update: Update, context: CallbackContext) -> int:
    """Display settings menu."""
    lang = context.user_data.get('language', 'en')
    
    reply_keyboard = [
        ['🇬🇧 English', '🇮🇷 فارسی'],
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
    elif text in ['🇬🇧 English', '🇮🇷 فارسی']:
        new_lang = 'en' if text == '🇬🇧 English' else 'fa'
        context.user_data['language'] = new_lang
        await update.message.reply_text(get_message(new_lang, 'menu', 'language_changed'))
        from bot import show_main_menu
        return await show_main_menu(update, context)
    
    return SETTINGS 