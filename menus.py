import logging
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import ContextTypes, CallbackContext, ConversationHandler, MessageHandler, filters
from languages import get_message
from states import ACCEPT_INVITE_CODE, ADD_CYCLE_DATE, LOGIN, MENU, REGISTER

def get_main_menu(lang: str):
    """Return the main menu text and reply keyboard."""
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

    return  markup , menu_text


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def handle_initial_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle the initial Register/Login choice."""
    lang = context.user_data.get("language", "en")
    choice = update.message.text

    if choice.lower() == get_message(lang, "auth", "register").lower():
        await update.message.reply_text(get_message(lang, "auth", "enter_username"))
        return REGISTER
    elif choice.lower() == get_message(lang, "auth", "login").lower():
        await update.message.reply_text(get_message(lang, "auth", "enter_username"))
        return LOGIN
    else:
        await update.message.reply_text(get_message(lang, "welcome", "choose_option"))
        return REGISTER
    
async def handle_menu(update: Update, context: CallbackContext) -> int:
    """Handle main menu selections."""
    text = update.message.text
    lang = context.user_data.get('language', 'en')
    print(f"User selected menu option: {text}")
    
    # Import at the top of your file instead of inside functions
    from handlers.cycle.add_cycle_handlers import start_add_cycle
    from handlers.cycle.history_handlers import history_handlers
    from handlers.setting.setting import start_settings
    from handlers.profile.profile import handle_profile, start_profile
    try:
 
        if text == get_message(lang, 'menu', 'add_new_cycle'):
            return await start_add_cycle(update, context)
        elif text == get_message(lang, 'menu', 'track_period'):
            # Make sure this state is defined in your ConversationHandler
            return ADD_CYCLE_DATE
        elif text == get_message(lang, 'menu', 'view_history'):
            return await history_handlers(update, context)
        elif text == get_message(lang, 'settings', 'menu'):
            print("Navigating to settings menu")
            return await start_settings(update, context)
        elif text == get_message(lang , 'settings','language'):
            from handlers.setting.setting import handle_settings
            return await handle_settings(update, context)
        elif text == get_message(lang, 'settings', 'EN') or text == get_message(lang, 'settings', 'FA'):
            from handlers.setting.setting import handle_language_selection
            return await handle_language_selection(update, context)

        elif text == get_message(lang, 'Profile', 'menu'):
            return await start_profile(update, context)
        elif text == get_message(lang,'Profile','view_profile'):
            return await handle_profile(update, context)
        #cycle analysis
        elif text == get_message(lang, 'menu', 'cycle_analysis'):
            from handlers.cycle.cycle_analysis import start_cycle_analysis
            return await start_cycle_analysis(update, context)
        elif text == get_message(lang, 'cycle_analysis', 'view_analysis'):
            from handlers.cycle.cycle_analysis import cycle_analysis
            return await cycle_analysis(update, context)
        #partner menu
        elif text == get_message(lang, 'menu', 'partner_menu'):
            from handlers.partner.partner import start_partner_menu
            return await start_partner_menu(update, context)
        elif text == get_message(lang,'partner','add_partner'):
            from handlers.partner.partner import handle_partner_menu
            return await handle_partner_menu(update, context)
        elif text == get_message(lang, 'partner', 'view_partners'):
            from handlers.partner.partner import handle_partner_menu
            return await handle_partner_menu(update, context)
        elif text == get_message(lang,'partner','get_invite_code'):
            from handlers.partner.partner import handle_partner_menu
            return await handle_partner_menu(update, context)
        
        elif text == get_message(lang, 'partner', 'accept_invite'):

            from handlers.partner.partner import handle_partner_menu
            return await handle_partner_menu(update, context)

        
        elif text == get_message(lang, 'partner', 'get_remove_code'):
            from handlers.partner.partner import handle_partner_menu
            return await handle_partner_menu(update, context)
        elif text == get_message(lang, 'partner', 'remove_partner'):
            from handlers.partner.partner import handle_partner_menu
            return await handle_partner_menu(update, context)
        ###
        elif text == get_message(lang, 'menu', 'back_to_main_menu'):
            markup, menu_text = get_main_menu(lang)
            await update.message.reply_text(menu_text, reply_markup=markup)
            return MENU
        else:
            print(f"Invalid menu option selected: {text}")
            # Invalid option: reset conversation to main menu
            await update.message.reply_text(
                get_message(lang, 'errors', 'invalid_option')
            )
            markup, menu_text = get_main_menu(lang)
            await update.message.reply_text(menu_text, reply_markup=markup)
            # Reset to MENU state
            return MENU
            
    except Exception as e:
        logger.error(f"Error in handle_menu: {e}")
        await update.message.reply_text(get_message(lang, 'errors', 'something_went_wrong'))
        return MENU  # Stay in current state


    

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancel the conversation."""
    lang = context.user_data.get("language", "en")
    cancel_text = get_message(lang, "errors", "operation_cancelled")  

    await update.message.reply_text(
        cancel_text,
        reply_markup=ReplyKeyboardRemove()
    )
    return -1 