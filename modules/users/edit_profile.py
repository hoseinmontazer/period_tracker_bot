from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import ContextTypes

from utils.token_store import get_token
from .api  import  update_user_profile
from utils.helpers import format_user_profile
from constants import DASHBOARD, EDIT_CYCLE_LENGTH, EDIT_FIRST_NAME, EDIT_LAST_NAME, EDIT_PERIOD_DURATION, SETTINGS


async def handle_edit_profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start a conversation to edit the user's profile step-by-step."""
    text = update.message.text
    keyboard = [
        ["Skip"],
        ["⬅️ Back to Dashboard"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    if text == "⬅️ Back to Dashboard":
        from modules.users.handlers import show_dashboard
        return await show_dashboard(update, context)
    else:
        await update.message.reply_text("Please send your new first name. Or send 'skip' to keep it unchanged.", reply_markup=reply_markup)
        return EDIT_FIRST_NAME


async def handle_first_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the user's first name input and ask for the next field."""
    text = update.message.text
    keyboard = [
        ["Skip"],
        ["⬅️ Back to Dashboard"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    if text == "⬅️ Back to Dashboard":
        from modules.users.handlers import show_dashboard
        return await show_dashboard(update, context)
    if text!= "Skip":
        context.user_data['first_name'] = text

    await update.message.reply_text("Please send your new last name. Or send 'skip' to keep it unchanged.", reply_markup=reply_markup)
    return EDIT_LAST_NAME



async def handle_last_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    keyboard = [
        ["Skip"],
        ["⬅️ Back to Dashboard"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    if text == "⬅️ Back to Dashboard":
        from modules.users.handlers import show_dashboard
        return await show_dashboard(update, context)
    if text!= "Skip":
        context.user_data['last_name'] = text
    await update.message.reply_text("Please send your new cycle length (in days). Or send 'skip'.", reply_markup=reply_markup)
    return EDIT_CYCLE_LENGTH

async def handle_cycle_length(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the cycle length and ask for period duration."""
    text = update.message.text
    print(text)
    keyboard = [
        ["Skip"],
        ["⬅️ Back to Dashboard"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    if text == "⬅️ Back to Dashboard":
        from modules.users.handlers import show_dashboard
        return await show_dashboard(update, context)
    if text!= "Skip":
        try:
            context.user_data['cycle_length'] = int(text)
        except (ValueError, TypeError):
            await update.message.reply_text("That's not a valid number. Please send a number for your cycle length. Or send 'skip'.", reply_markup=reply_markup)
            return EDIT_CYCLE_LENGTH # Stay in the same state if input is invalid
    
    await update.message.reply_text("Please send your new period duration (in days). Or send 'skip'.", reply_markup=reply_markup)
    return EDIT_PERIOD_DURATION

async def handle_period_duration(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the period duration and finalize the update."""
    from modules.users.handlers import show_dashboard
    text = update.message.text
    chat_id = update.effective_chat.id
    token = context.user_data.get("token") or get_token(chat_id)

    keyboard = [
        ["⬅️ Back to Dashboard"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    if text == "⬅️ Back to Dashboard":
        from modules.users.handlers import show_dashboard
        return await show_dashboard(update, context)
    if text!= "Skip":
        try:
            context.user_data['period_duration'] = int(text)
        except (ValueError, TypeError):
            await update.message.reply_text("That's not a valid number. Please send a number for your period duration. Or send 'skip'.")
            return EDIT_PERIOD_DURATION
    
    # Now, with all the data collected, make the API call
    data_to_update = {k: v for k, v in context.user_data.items() if k in ['first_name', 'last_name', 'cycle_length', 'period_duration']}
    print("data_to_update --- > ",data_to_update)
    if not data_to_update:
        await update.message.reply_text("No changes were made.")
        return DASHBOARD
    await update.message.reply_chat_action(action="typing")
    success,result = await update_user_profile(token, **data_to_update)
    print(result)

    if success:
        message_text = "✅ Profile updated successfully!\n\n" + format_user_profile(result)
        await update.message.reply_text(message_text)

    else:
        await update.message.reply_text(f"Failed to update profile:\n{result}")


    context.user_data.pop('first_name', None) # Clear temporary data
    context.user_data.pop('last_name', None)
    context.user_data.pop('cycle_length', None)
    context.user_data.pop('period_duration', None)
    
    await show_dashboard(update, context)
    return DASHBOARD