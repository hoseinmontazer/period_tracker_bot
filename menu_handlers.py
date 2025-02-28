from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext
from languages import get_message
from states import MENU

async def show_main_menu(update: Update, context: CallbackContext) -> int:
    """Display the main menu."""
    lang = context.user_data.get('language', 'en')
    
    reply_keyboard = [
        [{"text": get_message(lang, 'menu', 'track_period')}, 
         {"text": get_message(lang, 'menu', 'view_history')}],
        [{"text": get_message(lang, 'menu', 'cycle_analysis')}, 
         {"text": get_message(lang, 'menu', 'add_new_cycle')}],
        [{"text": get_message(lang, 'menu', 'partner_menu')}],
        [{"text": get_message(lang, 'settings', 'menu')}]
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
    elif text == get_message(lang, 'menu', 'partner_menu'):
        from partner import show_partner_menu
        return await show_partner_menu(update, context)
    elif text == get_message(lang, 'settings', 'menu'):
        from settings import show_settings_menu
        return await show_settings_menu(update, context)
    
    return MENU 