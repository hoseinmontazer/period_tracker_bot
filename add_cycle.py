from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    CallbackContext, ConversationHandler, MessageHandler, 
    filters, CallbackQueryHandler
)
from states import MENU, START_DATE, END_DATE, SYMPTOMS, MEDICATION
from calendar_keyboard import CalendarKeyboard
import httpx
from config import BASE_URL

calendar = CalendarKeyboard()

# Define the states for adding a new cycle
START_DATE, END_DATE, SYMPTOMS, MEDICATION = range(4)

# This is the function for starting the add cycle conversation
async def start_add_cycle(update, context):
    chat_id = str(update.message.chat_id)
    
    # First check if user is authenticated
    from bot import user_tokens
    if chat_id not in user_tokens or "access" not in user_tokens[chat_id]:
        await update.message.reply_text("⚠️ You need to log in first. Use /start to login.")
        return ConversationHandler.END
    
    # Show calendar for start date selection
    await update.message.reply_text(
        "Please select the start date:",
        reply_markup=calendar.create_calendar()
    )
    return START_DATE

async def handle_calendar_selection(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    
    selected_date = calendar.process_calendar_selection(query)
    
    if isinstance(selected_date, str):  # Date was selected
        context.user_data['start_date'] = selected_date
        await query.message.edit_text(f"Selected date: {selected_date}")
        
        # Ask for end date
        await query.message.reply_text(
            "Please select the end date or press Skip:",
            reply_markup=calendar.create_calendar()
        )
        return END_DATE
    else:  # Navigation through calendar
        await query.message.edit_reply_markup(reply_markup=selected_date)
        return START_DATE

# State handler for capturing the start date
async def handle_start_date(update, context):
    if update.message.text.lower() == 'skip':
        # If the user skips, this is invalid since start date is required
        await update.message.reply_text("The start date is required. Please enter a valid date (YYYY-MM-DD).")
        return START_DATE

    context.user_data['start_date'] = update.message.text.strip()  # Save the start date
    await update.message.reply_text("Enter the end date (YYYY-MM-DD) or press 'Skip':")
    return END_DATE

# State handler for capturing the end date
async def handle_end_date(update, context):
    if update.message.text.lower() == 'skip':
        # If user skips, move to the next step (SYMPTOMS)
        context.user_data['end_date'] = None  # Mark as skipped
        await update.message.reply_text("Skipping end date. Let's move to the next step (Symptoms).")
        return SYMPTOMS

    context.user_data['end_date'] = update.message.text.strip()  # Save the end date
    await update.message.reply_text("Enter any symptoms (or leave blank to skip):")
    return SYMPTOMS

# State handler for capturing symptoms
async def handle_symptoms(update, context):
    if update.message.text.lower() == 'skip':
        # If user skips, move to the next step (MEDICATION)
        context.user_data['symptoms'] = None  # Mark as skipped
        await update.message.reply_text("Skipping symptoms. Let's move to the next step (Medication).")
        return MEDICATION
    
    context.user_data['symptoms'] = update.message.text.strip() or ""  # Save symptoms
    await update.message.reply_text("Enter any medication (or leave blank to skip):")
    return MEDICATION

async def save_cycle_to_api(chat_id, cycle_data, user_tokens):
    """Save cycle data to the API"""
    if chat_id not in user_tokens or "access" not in user_tokens[chat_id]:
        return False, "Authentication required"
    
    access_token = user_tokens[chat_id]["access"]
    headers = {"Authorization": f"Bearer {access_token}"}
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{BASE_URL}/api/periods/",
                headers=headers,
                data={
                    "start_date": cycle_data["start_date"],
                    "end_date": cycle_data["end_date"],
                    "symptoms": cycle_data["symptoms"],
                    "medication": cycle_data["medication"]
                }
            )
            
            if response.status_code == 201:
                return True, response.json()
            else:
                return False, f"API Error: {response.status_code}"
                
        except Exception as e:
            return False, f"Error: {str(e)}"

async def handle_medication(update, context):
    chat_id = str(update.message.chat_id)
    
    if update.message.text.lower() == 'skip':
        context.user_data['medication'] = None
    else:
        context.user_data['medication'] = update.message.text.strip() or ""
    
    # Prepare cycle data
    cycle_data = {
        "start_date": context.user_data.get('start_date'),
        "end_date": context.user_data.get('end_date'),
        "symptoms": context.user_data.get('symptoms', ""),
        "medication": context.user_data.get('medication', "")
    }
    
    # Import user_tokens here to avoid circular import
    from bot import user_tokens
    
    # Save to API
    success, result = await save_cycle_to_api(chat_id, cycle_data, user_tokens)
    
    if success:
        await update.message.reply_text(
            "✅ Cycle data has been saved successfully!",
            reply_markup=ReplyKeyboardRemove()
        )
    else:
        await update.message.reply_text(
            f"❌ Failed to save cycle data: {result}",
            reply_markup=ReplyKeyboardRemove()
        )

    # Clear user data
    context.user_data.clear()

    # Show menu keyboard
    reply_keyboard = [
        ['Track Period', 'View History'],
        ['Cycle Analysis', 'Add New Cycle'],
        ['Logout']
    ]
    await update.message.reply_text(
        "📋 **Main Menu**\nChoose an option:",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
        parse_mode="Markdown"
    )
    
    return ConversationHandler.END

# Cancel handler
async def cancel(update: Update, context: CallbackContext) -> int:
    """Handles canceling the operation and ends the conversation."""
    await update.message.reply_text("Operation cancelled.")
    return ConversationHandler.END

add_cycle_conversation = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex("^Add New Cycle$"), start_add_cycle)],
    states={
        START_DATE: [
            CallbackQueryHandler(handle_calendar_selection),
            MessageHandler(filters.TEXT & ~filters.COMMAND, handle_start_date)
        ],
        END_DATE: [
            CallbackQueryHandler(handle_calendar_selection),
            MessageHandler(filters.TEXT & ~filters.COMMAND, handle_end_date)
        ],
        SYMPTOMS: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_symptoms)],
        MEDICATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_medication)],
    },
    fallbacks=[MessageHandler(filters.Regex('^Cancel$'), cancel)],
    allow_reentry=True
)
