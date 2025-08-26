from telegram import ReplyKeyboardMarkup
from languages import get_message

def get_main_menu(lang: str):
    """Return the main menu text and reply keyboard."""
    # متن منو
    menu_text = get_message(lang, 'menu', 'main')

    reply_keyboard = [
        [get_message(lang, 'menu', 'track_period'), get_message(lang, 'menu', 'view_history')],
        [get_message(lang, 'menu', 'cycle_analysis'), get_message(lang, 'menu', 'add_new_cycle')],
        ["👥 Partner Menu" if lang == 'en' else "👥 منوی شریک"],
        [get_message(lang, 'settings', 'menu')]
    ]

    markup = ReplyKeyboardMarkup(
        reply_keyboard,
        one_time_keyboard=True,
        resize_keyboard=True
    )

    return menu_text, markup
