
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import ContextTypes

from constants import  CONFIRM_DELETE, DASHBOARD, START_DELETE
from utils.get_period_id_from_user_choice import get_period_id_from_user_choice
from modules.periods.api import delete_period, get_all_periods
from modules.users.handlers import show_dashboard
from utils.token_store import get_token
##  start delete

async def handel_start_delete_period(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start a conversation to delete  step-by-step."""
    text = update.message.text
    keyboard = [
        ["⬅️ Back to Dashboard"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    if text == "⬅️ Back to Dashboard":
        from modules.users.handlers import show_dashboard
        return await show_dashboard(update, context)
    else:
        # Check if the text is a valid ID (e.g., a number)
        try:
            # Store the user's provided cycle ID in a temporary variable within the context
            context.user_data['cycle_id_to_delete'] = int(text) 
            await update.message.reply_text("Are you sure you want to delete this cycle? (yes/no)")
            return CONFIRM_DELETE
        except ValueError:
            await update.message.reply_text("Please send a number. Or Back to Dashboard.", reply_markup=reply_markup)
            return START_DELETE

    

async def start_delete_period(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start a conversation to delete step-by-step."""
    text = update.message.text
    chat_id = update.effective_chat.id
    token = context.user_data.get("token") or get_token(chat_id)

    keyboard = [
        ["⬅️ Back to Dashboard"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    if text == "⬅️ Back to Dashboard":
        
        return await show_dashboard(update, context)
    else:
        # Retrieve the stored cycle ID from context.user_data
        cycle_id = context.user_data.get('cycle_id_to_delete')

        if cycle_id is None:
            await update.message.reply_text("Something went wrong. Please try again.")
            return await show_dashboard(update, context)

        await update.message.reply_chat_action(action="typing")
        periods_list = await get_all_periods (token=token)
        id_to_delete = get_period_id_from_user_choice(periods_list, cycle_id)

        print("---->" , id_to_delete)
        result = await delete_period(
            token=token,
            id=id_to_delete 
        )

        print("result is -----> %s", result)

        if result and result.get("success"):
            await update.message.reply_text(f"Successfully deleted cycle with ID: {cycle_id}")
        else:
            await update.message.reply_text("Failed to delete the cycle. Please check the ID and try again.")
        
        # Clean up the user_data after the operation is complete
        context.user_data.pop('cycle_id_to_delete', None)

        return await show_dashboard(update, context)

