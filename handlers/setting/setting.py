from telegram import ReplyKeyboardMarkup, Update
from languages import get_message
from menus import get_main_menu
from states import LANGUAGE_SELECTION, MENU, SETTINGS
from telegram.ext import ContextTypes, CallbackContext

from utils import load_user_data

async def start_settings(update: Update, context: CallbackContext) -> int:
    """Start the settings menu."""
    lang = context.user_data.get('language', 'en')
    
    # Create settings menu keyboard
    settings_keyboard = [
        [get_message(lang, 'settings', 'language')],
        [get_message(lang, 'settings', 'profile')],
        [get_message(lang, 'settings', 'back_to_main_menu')],

    ]
    
    markup = ReplyKeyboardMarkup(
        settings_keyboard,
        one_time_keyboard=False,
        resize_keyboard=True
    )
    
    settings_text = get_message(lang, 'settings', 'menu')
    await update.message.reply_text(settings_text, reply_markup=markup)
    return SETTINGS



async def handle_settings(update: Update, context: CallbackContext) -> int:
    """Handle settings menu selections."""
    print("handle_settings called")
    text = update.message.text
    lang = context.user_data.get('language', 'en')
    
    if text == get_message(lang, 'settings', 'language'):
        # Show language selection menu
        language_keyboard = [
            ["English", "فارسی"],
            [get_message(lang, 'settings', 'back_to_main_menu')]
        ]
        
        markup = ReplyKeyboardMarkup(
            language_keyboard,
            one_time_keyboard=True,
            resize_keyboard=True
        )
        
        await update.message.reply_text(
            get_message(lang, 'settings', 'choose_language'),
            reply_markup=markup
        )
        return LANGUAGE_SELECTION
        
    elif text == get_message(lang, 'settings', 'back_to_main_menu'):
        # Return to main menu
        print("Returning to main menu from settings")
        markup, menu_text = get_main_menu(lang)
        await update.message.reply_text(menu_text, reply_markup=markup)
        return MENU

    return SETTINGS

async def handle_language_selection(update: Update, context: CallbackContext) -> int:
    """Handle language selection."""
    text = update.message.text
    lang = context.user_data.get('language', 'en')
    
    if text == "English":
        context.user_data['language'] = 'en'
        lang = 'en'
        confirmation = get_message(lang, 'settings', 'language_changed')
    elif text == "فارسی":
        context.user_data['language'] = 'fa'
        lang = 'fa'
        confirmation = get_message(lang, 'settings', 'language_changed')
    elif text == get_message(lang, 'settings', 'back_to_main_menu'):
        # Return to main menu
        markup, menu_text = get_main_menu(lang)
        await update.message.reply_text(menu_text, reply_markup=markup)
        return MENU
    else:
        await update.message.reply_text(get_message(lang, 'errors', 'invalid_option'))
        return LANGUAGE_SELECTION
    
    user_data = load_user_data()
    chat_id = str(update.message.chat_id)
    if chat_id in user_data:
        user_data[chat_id]['language'] = context.user_data['language']
        # Save updated language preference
        from utils import save_user_data
        save_user_data(user_data)
    
    # Show settings menu again
    await update.message.reply_text(confirmation)
    return await start_settings(update, context)