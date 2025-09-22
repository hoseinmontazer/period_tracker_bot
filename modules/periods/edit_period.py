
import json
from telegram import KeyboardButton, ReplyKeyboardMarkup, Update, WebAppInfo
from telegram.ext import ContextTypes

from config import WEB_APP_URL
from constants import  ASK_EDIT_CYCLE, ASK_EDIT_DURATION, ASK_EDIT_END_DATE, ASK_EDIT_MEDICATION, ASK_EDIT_PERIOD, ASK_EDIT_START_DATE, ASK_EDIT_SYMPTOMS
from utils.get_period_id_from_user_choice import get_period_id_from_user_choice
from modules.periods.api import delete_period, edit_period, get_all_periods
from modules.users.handlers import show_dashboard
from utils.token_store import get_token
from utils.buttons import back_skip_keyboard


async def handel_start_edit_period(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start a conversation to delete  step-by-step."""
    print(context.user_data, "context.user_data in handel_start_edit_period")
    text = update.message.text

    if text == "⬅️ Back to Dashboard":
        from modules.users.handlers import show_dashboard
        return await show_dashboard(update, context)
    else:
        await update.message.reply_text("Please send a number. Or Back to Dashboard.", reply_markup=back_skip_keyboard())
        return ASK_EDIT_PERIOD
        

async def start_edit_period(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ask user to select a period to edit."""
    print(context.user_data, "context.user_data in handel_start_edit_period")

    chat_id = update.effective_chat.id
    token = context.user_data.get("token") or get_token(chat_id)
    
    period_list = await get_all_periods (token=token)
    print(period_list)
    text = update.message.text

    if text == "⬅️ Back to Dashboard":
        from modules.users.handlers import show_dashboard
        return await show_dashboard(update, context)

    period_id = get_period_id_from_user_choice(period_list, text)
    print(period_id)
    if not period_id:
        await update.message.reply_text("Please select a valid number.", reply_markup=back_skip_keyboard())
        return ASK_EDIT_PERIOD
    ###
    keyboard = [
        [KeyboardButton(text="📅 Period Start Date", web_app=WebAppInfo(url=WEB_APP_URL))],
        ["⬅️ Back to Dashboard", "Skip"]
    ]

    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        "Click the button below to open the mini app and send start date to the bot:",
        reply_markup=reply_markup
    )
    context.user_data['period_id'] = period_id
    return ASK_EDIT_START_DATE

###
async def ask_edit_start_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(context.user_data, "context.user_data in handel_start_edit_period 1")

    text = update.message.text
    print(text)

    if text == "⬅️ Back to Dashboard":
        from modules.users.handlers import show_dashboard
        return await show_dashboard(update, context)

    keyboard = [
        [KeyboardButton(text="📅 Period End Date", web_app=WebAppInfo(url=WEB_APP_URL))],
        ["⬅️ Back to Dashboard", "Skip"]
    ]
    # Skip option
    if text and text.lower() == "skip":
        context.user_data['start_date'] = None
        # await update.message.reply_text("Skipped End date.", reply_markup=keyboard)
        # return ASK_EDIT_END_DATE

    # context.user_data["start_date"] = {"start_date": text}
    web_app_data = update.effective_message.web_app_data
    if web_app_data and web_app_data.data:
        # Parse JSON from WebApp
        data_dict = json.loads(web_app_data.data)
        selected_date = data_dict.get("date")  
        print(f"Received date from web app: {selected_date}")
        
        # Store date in user context
        # context.user_data["current_period"] = {"start_date": selected_date}
        context.user_data['start_date'] = selected_date




    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "Click the button below to open the mini app and send end date to the bot:",
        reply_markup=reply_markup
    )
    return ASK_EDIT_END_DATE

###
async def ask_edit_end_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(context.user_data, "context.user_data in handel_start_edit_period")

    text = update.message.text
    print(text,"---->")
    if text == "⬅️ Back to Dashboard":
        from modules.users.handlers import show_dashboard
        return await show_dashboard(update, context)
    # Skip option
    if text and text.lower() == "skip":
        context.user_data['end_date'] = None
        # await update.message.reply_text("Skipped End date.", reply_markup=back_skip_keyboard())
        # return ASK_EDIT_CYCLE
    
    web_app_data = update.effective_message.web_app_data
    if web_app_data and web_app_data.data:
        # Parse JSON from WebApp
        data_dict = json.loads(web_app_data.data)
        selected_date = data_dict.get("date")  
        print(f"Received date from web app: {selected_date}")
        context.user_data['end_date'] = selected_date


    await update.message.reply_text("Enter cycle length (days):", reply_markup=back_skip_keyboard())
    return ASK_EDIT_CYCLE

async def ask_edit_cycle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(context.user_data, "context.user_data in handel_start_edit_period")

    text = update.message.text    
    if text == "⬅️ Back to Dashboard":
        from modules.users.handlers import show_dashboard
        return await show_dashboard(update, context)
    if text.lower() != 'skip':
        context.user_data['cycle_length'] = update.message.text
    await update.message.reply_text("Enter period duration (days):",  reply_markup=back_skip_keyboard())
    return ASK_EDIT_DURATION

async def ask_edit_duration(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(context.user_data, "context.user_data in handel_start_edit_period")

    text = update.message.text    
    if text == "⬅️ Back to Dashboard":
        from modules.users.handlers import show_dashboard
        return await show_dashboard(update, context)
    if text.lower() != 'skip':
        context.user_data['period_duration'] = update.message.text
    await update.message.reply_text("Enter symptoms (comma separated):",  reply_markup=back_skip_keyboard())
    return ASK_EDIT_SYMPTOMS

async def ask_edit_symptoms(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(context.user_data, "context.user_data in handel_start_edit_period")
    text = update.message.text
    if text == "⬅️ Back to Dashboard":
        from modules.users.handlers import show_dashboard
        return await show_dashboard(update, context)
    if text.lower() != 'skip':
        context.user_data['symptoms'] = update.message.text
    await update.message.reply_text("Enter medications (comma separated):",  reply_markup=back_skip_keyboard())
    return ASK_EDIT_MEDICATION

async def ask_edit_medication(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(context.user_data, "context.user_data in handel_start_edit_period end")
    # context.user_data['medication'] = update.message.text
    
    text = update.message.text
    chat_id = update.effective_chat.id
    token = context.user_data.get("token") or get_token(chat_id)  

    if text == "⬅️ Back to Dashboard":
        from modules.users.handlers import show_dashboard
        return await show_dashboard(update, context)
    if text.lower() != "skip":
        context.user_data['medication'] = text
    else:
        context.user_data['medication'] = None 

    period_id = context.user_data.get('period_id')
    await update.message.reply_chat_action(action="typing")
    await update.message.reply_text("Updating your period...")
    result = await edit_period(
        token=token,
        period_id=period_id,
        start_date=context.user_data.get('start_date'),
        end_date=context.user_data.get('end_date'),
        cycle_length=context.user_data.get('cycle_length'),
        period_duration=context.user_data.get('period_duration'),
        symptoms=context.user_data.get('symptoms'),
        medication=context.user_data.get('medication')
    )

    print("result is -----> %s", result)


    if  'error' in result:
        await update.message.reply_text(f"❌ Failed to edit period. Error: {result['error']}")
    elif result and result.get("success"):
        await update.message.reply_text("✅ Period updated successfully!")
    else:
        await update.message.reply_text("❌ Failed to edit period. Please check the details and try again.")
    context.user_data.clear()
    from modules.users.handlers import show_dashboard
    return await show_dashboard(update, context)

