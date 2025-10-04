import json
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, Update, ReplyKeyboardRemove, WebAppInfo 
from telegram.ext import ContextTypes
from config import WEB_APP_URL
from constants import DASHBOARD, TRACK_PERIOD_START, TRACK_PERIOD_SYMPTOMS, TRACK_PERIOD_MEDICATION
from modules.users.handlers import handle_dashboard, show_dashboard
from utils.token_store import get_token
from .api import get_all_periods, create_period
from utils.helpers import format_period_data
from utils.validators import validate_date
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove

async def show_period_history(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show period history"""
    # token = context.user_data.get("token")
    print("show_period_history")
    chat_id = update.effective_chat.id
    token = context.user_data.get("token") or get_token(chat_id)
    
    if not token:
        await update.message.reply_text("Please login first.")
        return DASHBOARD
    
    await update.message.reply_chat_action(action="typing")
    periods = await get_all_periods(token)

    if isinstance(periods, list):
        formatted_data = format_period_data(periods)
        await update.message.reply_text(formatted_data, parse_mode='Markdown')
    else:
        await update.message.reply_text("❌ No period history found.")
    
    return DASHBOARD

async def show_partner_period_history(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show period history"""
    # token = context.user_data.get("token")

    chat_id = update.effective_chat.id
    token = context.user_data.get("token") or get_token(chat_id)
    
    if not token:
        await update.message.reply_text("Please login first.")
        return DASHBOARD
    partner = "partner"
    await update.message.reply_chat_action(action="typing")
    periods = await get_all_periods(token, partner)

    if isinstance(periods, list):
        formatted_data = format_period_data(periods)
        await update.message.reply_text(formatted_data, parse_mode='Markdown')
    else:
        await update.message.reply_text("❌ No period history found.")
    
    return DASHBOARD


async def handler_period_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show partner menu"""
    chat_id = update.effective_chat.id
    token = context.user_data.get("token") or get_token(chat_id)
    print("handler_period_menu")
    if not token:
        await update.message.reply_text("Please login first.")
        return DASHBOARD
    keyboard = [
        ["➕ Add Period", "✍️ Edit Period"],
        ["🗑️ Delete Period"],
        ["⬅️ Back to Dashboard"]
    ]

    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("🗓️ Please select an option for managing periods:", reply_markup=reply_markup)    
    return DASHBOARD


#add perios
async def start_track_period(update, context):
    """
    Send a KeyboardButton that opens a WebApp (Mini App).
    User selects a date and sends it directly to the bot.
    """
    chat_id = update.effective_chat.id
    token = context.user_data.get("token") or get_token(chat_id)
    
    if not token:
        await update.message.reply_text("Please login first.")
        return DASHBOARD


    keyboard = [
        [KeyboardButton(text="📅 Period Start Date", web_app=WebAppInfo(url=WEB_APP_URL))],
        ["⬅️ Back to Dashboard"]
    ]

    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        "Click the button below to open the mini app and send date directly to the bot:",
        reply_markup=reply_markup
    )
    return TRACK_PERIOD_START



async def handle_period_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
#async def handle_period_date(update: Update, context: ContextTypes.DEFAULT_TYPE, data: str):
    chat_id = update.effective_chat.id
    token = context.user_data.get("token") or get_token(chat_id)
    
    if not token:
        await update.message.reply_text("Please login first.")
        return DASHBOARD

    print("Web app data received! strat period")
    text = update.message.text
    print(text)
    chat_id = update.effective_chat.id
    token = context.user_data.get("token") or get_token(chat_id)
    print(token)
    
    if text == "⬅️ Back to Dashboard":
        return await show_dashboard(update, context)
    else:
        try:
            web_app_data = update.effective_message.web_app_data
            if web_app_data and web_app_data.data:
                # Parse JSON from WebApp
                data_dict = json.loads(web_app_data.data)
                selected_date = data_dict.get("date")  
                print(f"Received date from web app: {selected_date}")
                
                # Store date in user context
                context.user_data["current_period"] = {"start_date": selected_date}

                # Keyboard for next step
                keyboard = [["Skip", "Back to Dashboard"]]
                reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)

            #     await update.message.reply_text(
            #         f"✅ Selected start date: {selected_date}\n\n"
            #         "Now, please describe any symptoms you're experiencing:\n"
            #         "(Type 'skip' to skip this step)",
            #         reply_markup=reply_markup
            #     )
            #     return TRACK_PERIOD_SYMPTOMS
            # else:
            #     print("No web app data found in messagees")
            #     await update.message.reply_text(
            #         "❌ No date received. Please try selecting the date again.",
            #         reply_markup=ReplyKeyboardRemove()
            #     )
            #     return await start_track_period(update, context)



            result = await create_period(
                token=token,
                start_date=selected_date,
                cycle_length=28,
                period_duration=5,
                # symptoms=period_data.get("symptoms"),
                # medication=period_data.get("medication")
            )

            print("result is %s",result)
            if "id" in result:
                await update.message.reply_text("✅ Period tracked successfully!")
            else:
                await update.message.reply_text("❌ Failed to track period.")

            return await show_dashboard(update, context)




        except Exception as e:
            logging.exception("Error handling web app data")
            await update.message.reply_text(
                f"❌ An error occurred. Please try again. {e}",
                reply_markup=ReplyKeyboardRemove()
            )
            return await start_track_period(update, context)


# --- Get period start ---
async def get_period_start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    chat_id = update.effective_chat.id
    token = context.user_data.get("token") or get_token(chat_id)
    
    if not token:
        await update.message.reply_text("Please login first.")
        return DASHBOARD

    text = update.message.text.strip()

    if text == "Back to Dashboard":
        return await show_dashboard(update, context)

    if not validate_date(text):
        await update.message.reply_text("Invalid date format. Use YYYY-MM-DD.")
        return TRACK_PERIOD_START
    
    context.user_data["current_period"] = {"start_date": text}
    keyboard = [["Back to Dashboard"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    
    await update.message.reply_text("Add symptoms (or type 'skip'):", reply_markup=reply_markup)
    return TRACK_PERIOD_SYMPTOMS

# --- Get period symptoms ---
async def get_period_symptoms(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("start get_period_symptoms")
    text = update.message.text.strip()

    if text == "Back to Dashboard":
        return await show_dashboard(update, context)
    
    if text.lower() != 'skip':
        context.user_data["current_period"]["symptoms"] = text

    keyboard = [["Back to Dashboard"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    await update.message.reply_text("Add medication (or type 'skip'):", reply_markup=reply_markup)
    return TRACK_PERIOD_MEDICATION

# --- Get period medication ---
async def get_period_medication(update: Update, context: ContextTypes.DEFAULT_TYPE):



    text = update.message.text.strip()
    chat_id = update.effective_chat.id
    token = context.user_data.get("token") or get_token(chat_id)
    
    if not token:
        await update.message.reply_text("Please login first.")
        return DASHBOARD

    period_data = context.user_data.get("current_period", {})

    if text == "Back to Dashboard":
        return await show_dashboard(update, context)

    if text.lower() != 'skip':
        period_data["medication"] = text

    # Default values
    period_data.setdefault("cycle_length", 28)
    period_data.setdefault("period_duration", 5)

    await update.message.reply_chat_action(action="typing")
    result = await create_period(
        token=token,
        start_date=period_data["start_date"],
        cycle_length=period_data["cycle_length"],
        period_duration=period_data["period_duration"],
        symptoms=period_data.get("symptoms"),
        medication=period_data.get("medication")
    )

    print("result is %s",result)
    if "id" in result:
        await update.message.reply_text("✅ Period tracked successfully!")
    else:
        await update.message.reply_text("❌ Failed to track period.")

    return await show_dashboard(update, context)


