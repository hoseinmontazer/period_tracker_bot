from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    CallbackContext, ConversationHandler, MessageHandler, 
    filters, CallbackQueryHandler
)
import httpx
from config import BASE_URL
from states import MENU, START_DATE, SYMPTOMS, MEDICATION
from calendar_keyboard import CalendarKeyboard

calendar = CalendarKeyboard()

# Predefined symptom options
SYMPTOM_OPTIONS = [
    ['Cramps', 'Headache', 'Fatigue'],
    ['Bloating', 'Mood Swings', 'Acne'],
    ['Back Pain', 'Breast Tenderness'],
    ['Write Custom Symptoms', 'Done']
]

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
        
        # Initialize empty symptoms list
        context.user_data['symptoms'] = []
        
        # Move to symptoms selection
        await query.message.reply_text(
            "Select your symptoms (you can select multiple):",
            reply_markup=ReplyKeyboardMarkup(SYMPTOM_OPTIONS, one_time_keyboard=False)
        )
        return SYMPTOMS
    else:  # Navigation through calendar
        await query.message.edit_reply_markup(reply_markup=selected_date)
        return START_DATE

async def handle_symptoms(update, context):
    text = update.message.text
    
    # Initialize symptoms list if it doesn't exist
    if 'symptoms' not in context.user_data:
        context.user_data['symptoms'] = []
    
    if text == 'Done':
        # Join all symptoms with commas
        final_symptoms = ", ".join(context.user_data['symptoms']) if context.user_data['symptoms'] else ""
        context.user_data['final_symptoms'] = final_symptoms
        
        # Move to medication
        await update.message.reply_text(
            "Enter any medication (or press Skip):",
            reply_markup=ReplyKeyboardMarkup([['Skip']], one_time_keyboard=True)
        )
        return MEDICATION
        
    elif text == 'Write Custom Symptoms':
        await update.message.reply_text(
            "Please type your symptoms and press 'Done' when finished:",
            reply_markup=ReplyKeyboardMarkup([['Done']], one_time_keyboard=True)
        )
        return SYMPTOMS
        
    elif text not in ['Done', 'Write Custom Symptoms']:
        # Add the symptom to the list if it's not already there
        if text not in context.user_data['symptoms']:
            context.user_data['symptoms'].append(text)
            await update.message.reply_text(
                f"Added: {text}\nSelected symptoms: {', '.join(context.user_data['symptoms'])}\n\nSelect more or press 'Done'",
                reply_markup=ReplyKeyboardMarkup(SYMPTOM_OPTIONS, one_time_keyboard=False)
            )
        return SYMPTOMS

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
        context.user_data['medication'] = ""
    else:
        context.user_data['medication'] = update.message.text.strip()
    
    # Prepare cycle data
    cycle_data = {
        "start_date": context.user_data.get('start_date'),
        "symptoms": context.user_data.get('final_symptoms', ""),
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

async def cancel(update: Update, context: CallbackContext) -> int:
    """Handles canceling the operation and ends the conversation."""
    await update.message.reply_text("Operation cancelled.")
    return ConversationHandler.END

add_cycle_conversation = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex("^Add New Cycle$"), start_add_cycle)],
    states={
        START_DATE: [
            CallbackQueryHandler(handle_calendar_selection),
            MessageHandler(filters.TEXT & ~filters.COMMAND, handle_calendar_selection)
        ],
        SYMPTOMS: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_symptoms)],
        MEDICATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_medication)],
    },
    fallbacks=[MessageHandler(filters.Regex('^Cancel$'), cancel)],
    allow_reentry=True
)
