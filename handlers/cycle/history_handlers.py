from multiprocessing import context
import httpx
from config import PERIODS_API
from languages import get_message
from menus import get_main_menu
from utils import load_user_data    
from telegram import Update
from telegram.ext import ContextTypes
import logging
from states import MENU



async def history_handlers(update: Update, ext: ContextTypes.DEFAULT_TYPE) -> int:
    print("handle_view_history called")
    """Handle viewing the cycle history."""

    user_data = load_user_data()


    chat_id = str(update.message.chat_id)
    lang = user_data.get(chat_id, {}).get("language", "en")
    token = user_data.get(chat_id, {}).get("access")
    if not token:
        await update.message.reply_text(get_message(lang, "auth", "login_first"))
        return MENU

    headers = {"Authorization": f"Bearer {token}"}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(PERIODS_API, headers=headers)
            print("API response status:", response.status_code)  # Debug
            print("API response content:", response.text)  # Debug

            if response.status_code == 200:
                cycles = response.json()
                # print("Fetched cycles:", cycles)  # Debug

                if not cycles:
                    await update.message.reply_text(get_message(lang, "history", "no_cycles"))
                else:
                    history_lines = ["📅 **Cycle History**\n"]
                    for c in cycles:
                        history_lines.append(
                            f"{get_message(lang, 'history', 'cycle_id')} {c.get('id')}\n"
                            f"{get_message(lang, 'history', 'start_date')} {c.get('start_date')}\n"
                            f"{get_message(lang, 'history', 'predicted_end')} {c.get('predicted_end_date')}\n"
                            f"{get_message(lang, 'history', 'actual_end')} {c.get('end_date') or get_message(lang, 'history', 'ongoing')}\n"
                            f"{get_message(lang, 'history', 'medication')} {c.get('medication') or get_message(lang, 'history', 'none')}\n"
                            f"{get_message(lang, 'history', 'symptoms')} {c.get('symptoms') or get_message(lang, 'history', 'none')}\n"
                            f"{get_message(lang, 'history', 'separator')}"
                        )
                    history_text = "\n".join(history_lines)
                    await update.message.reply_text(history_text, parse_mode="Markdown")
            else:
                await update.message.reply_text(f"{get_message(lang, 'history', 'fetch_failed')} ({response.status_code})")

        except Exception as e:
            await update.message.reply_text(f"{get_message(lang, 'history', 'fetch_failed')}: {e}")


    # markup = get_main_menu(lang)
    # await update.message.reply_text( reply_markup=markup)
    return MENU