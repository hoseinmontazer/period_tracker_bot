import aiohttp
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import CallbackContext, ConversationHandler
from languages import get_message
from menus import get_main_menu
from states import MENU, PROFILE_MENU
import requests
import logging
from config import BASE_URL

logger = logging.getLogger(__name__)


async def  start_profile(update: Update, context: CallbackContext) -> int:
    """Start the profile menu."""
    lang = context.user_data.get('language', 'en')
    
    # Create profile menu keyboard
    profile_keyboard = [
        [get_message(lang, 'Profile', 'view_profile')],
        [get_message(lang, 'Profile', 'edit_profile')],
        [get_message(lang, 'Profile', 'back_to_main_menu')]
    ]
    
    markup = ReplyKeyboardMarkup(
        profile_keyboard,
        one_time_keyboard=False,
        resize_keyboard=True
    )
    
    profile_text = get_message(lang, 'Profile', 'menu')
    await update.message.reply_text(profile_text, reply_markup=markup)
    return PROFILE_MENU


async def handle_profile(update: Update, context: CallbackContext) -> int:
    """Handle profile menu selections."""
    text = update.message.text
    lang = context.user_data.get('language', 'en')
    
    if text == get_message(lang, 'Profile', 'view_profile'):
        chat_id = str(update.message.chat_id)
        user_tokens = context.bot_data.get('user_tokens', {})
        access_token = user_tokens.get(chat_id, {}).get('access')

        if not access_token:
            await update.message.reply_text(get_message(lang, 'errors', 'something_went_wrong'))
            return PROFILE_MENU

        headers = {"Authorization": f"Bearer {access_token}"}

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{BASE_URL}/api/user/profile/",
                    headers=headers
                ) as response:
                    if response.status == 200:
                        profile_data = await response.json()
                        user = profile_data.get("user", {})

                        profile_text = (
                            f"👤 *Profile Information*\n\n"
                            f"▫️ Username: `{user.get('username', '-')}`\n"
                            f"▫️ Email: `{user.get('email', '-')}`\n"
                            f"▫️ Sex: `{profile_data.get('sex', '-')}`\n"
                            f"▫️ Period Duration: `{profile_data.get('period_duration', '-')}` days\n"
                            f"▫️ Cycle Length: `{profile_data.get('cycle_length', '-')}` days\n"
                        )

                        partners = profile_data.get("partners", [])
                        if partners:
                            partner_lines = "\n".join(
                                [f"   - {p['username']} ({p['email']})" for p in partners]
                            )
                            profile_text += f"\n🤝 *Partners:*\n{partner_lines}"

                        await update.message.reply_text(
                            profile_text,
                            parse_mode="Markdown",
                            reply_markup=ReplyKeyboardRemove()
                        )

                        markup, menu_text = get_main_menu(lang)
                        await update.message.reply_text(
                            menu_text,
                            reply_markup=markup,
                            parse_mode="Markdown"
                        )
                        return ConversationHandler.END
                    else:
                        await update.message.reply_text(
                            f"❌ Error {response.status}",
                            reply_markup=ReplyKeyboardRemove()
                        )
                        return PROFILE_MENU

        except Exception as e:
            await update.message.reply_text(f"⚠️ Request failed: {str(e)}")
            return PROFILE_MENU
        
    elif text == get_message(lang, 'Profile', 'edit_profile'):
        await update.message.reply_text(get_message(lang, 'profile', 'feature_coming_soon'))
        return PROFILE_MENU
        
    elif text == get_message(lang, 'Profile', 'back_to_main_menu'):
        # Return to main menu
        markup, menu_text = get_main_menu(lang)
        await update.message.reply_text(menu_text, reply_markup=markup)
        return MENU
        
    else:
        # Invalid option: reset conversation to profile menu
        await update.message.reply_text(
            get_message(lang, 'errors', 'invalid_option')
        )
        return PROFILE_MENU