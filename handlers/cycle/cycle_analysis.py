import aiohttp
from telegram import ReplyKeyboardMarkup, Update 
from telegram.ext import ContextTypes, ConversationHandler
from states import CYCLE_ANALYSIS_MENU, MENU
from languages import get_message
from menus import get_main_menu

async def start_cycle_analysis(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Start the cycle analysis menu."""
    lang = context.user_data.get('language', 'en')
    
    # Create cycle analysis menu keyboard
    cycle_analysis_keyboard = [
        [get_message(lang, 'cycle_analysis', 'view_analysis')],
        [get_message(lang, 'cycle_analysis', 'back_to_main_menu')],
    ]
    
    markup = ReplyKeyboardMarkup(
        cycle_analysis_keyboard,
        one_time_keyboard=False,
        resize_keyboard=True
    )
    
    cycle_analysis_text = get_message(lang, 'cycle_analysis', 'menu')
    await update.message.reply_text(cycle_analysis_text, reply_markup=markup)
    return CYCLE_ANALYSIS_MENU

async def cycle_analysis(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle cycle analysis menu selections."""
    print("cycle_analysis called")
    text = update.message.text
    lang = context.user_data.get('language', 'en')
    
    if text == get_message(lang, 'cycle_analysis', 'view_analysis'):
        lang = context.user_data.get("language", "en")
        chat_id = str(update.message.chat_id)
        user_tokens = context.bot_data.get("user_tokens", {})
        access_token = user_tokens.get(chat_id, {}).get("access")
        if not access_token:
            await update.message.reply_text(get_message(lang, "errors", "something_went_wrong"))
            return CYCLE_ANALYSIS_MENU
        headers = {"Authorization": f"Bearer {access_token}" , "role": "self"}
        try:

            async with aiohttp.ClientSession() as session:
                async with session.get(
                    "https://api-period.shirpala.ir/api/periods/cycle_analysis/",
                    headers=headers
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        data = result.get("data", {})

                        msg = (
                            f"{get_message(lang, 'cycle_analysis', 'header')}"
                            f"{get_message(lang, 'cycle_analysis', 'average_cycle')} `{data.get('average_cycle', '-')}` days\n"
                            f"{get_message(lang, 'cycle_analysis', 'regularity_score')} `{data.get('regularity_score', '-')}`%\n"
                            f"{get_message(lang, 'cycle_analysis', 'prediction_reliability')} `{data.get('prediction_reliability', '-')}`%\n"
                            f"{get_message(lang, 'cycle_analysis', 'next_predicted_date')} `{data.get('next_predicted_date', '-')}`\n"
                        )

                        variations = data.get("cycle_variations", [])
                        if variations:
                            msg += f"{get_message(lang, 'cycle_analysis', 'cycle_variations')} {', '.join(map(str, variations))}"

                        await update.message.reply_text(msg, parse_mode="Markdown")
                        return ConversationHandler.END
                    else:
                        await update.message.reply_text(f"❌ Error {response.status}")
                        return CYCLE_ANALYSIS_MENU

        except Exception as e:
            await update.message.reply_text(f"⚠️ Request failed: {str(e)}")
            return CYCLE_ANALYSIS_MENU



    elif text == get_message(lang, 'cycle_analysis', 'back_to_main_menu'):
        # Return to main menu
        markup, menu_text = get_main_menu(lang)
        await update.message.reply_text(menu_text, reply_markup=markup)
        return MENU

    return CYCLE_ANALYSIS_MENU