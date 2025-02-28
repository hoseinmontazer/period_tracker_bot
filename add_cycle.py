from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    CallbackContext, ConversationHandler, MessageHandler, 
    filters, CallbackQueryHandler
)
import httpx
from config import BASE_URL
from states import MENU, START_DATE, SYMPTOMS, MEDICATION
from calendar_keyboard import CalendarKeyboard
from languages import get_message, SYMPTOM_OPTIONS, MEDICATION_OPTIONS
import logging

logger = logging.getLogger(__name__)

calendar = CalendarKeyboard()

async def start_add_cycle(update, context):
    chat_id = str(update.message.chat_id)
    lang = context.user_data.get('language', 'en')
    
    # First check if user is authenticated
    from bot import user_tokens
    if chat_id not in user_tokens or "access" not in user_tokens[chat_id]:
        await update.message.reply_text(get_message(lang, 'auth', 'login_required'))
        return ConversationHandler.END
    
    # Show calendar for start date selection
    await update.message.reply_text(
        get_message(lang, 'cycle', 'select_date'),
        reply_markup=calendar.create_calendar()
    )
    return START_DATE

async def handle_calendar_selection(update: Update, context: CallbackContext):
    query = update.callback_query
    if not query:
        return START_DATE

    try:
        await query.answer()
        result = calendar.process_calendar_selection(query)
        
        if isinstance(result, tuple):
            # Navigation action
            _, markup = result
            await query.message.edit_reply_markup(reply_markup=markup)
            return START_DATE
            
        elif result:  # Date selected
            selected_date = result
            context.user_data['start_date'] = selected_date
            lang = context.user_data.get('language', 'en')
            
            # Create symptoms keyboard
            keyboard = []
            for symptom_row in SYMPTOM_OPTIONS[lang]:
                keyboard.append(symptom_row)
            keyboard.append([get_message(lang, 'buttons', 'done')])
            
            markup = ReplyKeyboardMarkup(
                keyboard,
                one_time_keyboard=False,
                resize_keyboard=True
            )
            
            # Delete calendar message and show confirmation
            await query.message.delete()
            
            # Send confirmation and move to symptoms
            await query.message.reply_text(
                f"{get_message(lang, 'cycle', 'date_selected')}: {selected_date}"
            )
            
            await query.message.reply_text(
                get_message(lang, 'cycle', 'select_symptoms'),
                reply_markup=markup
            )
            
            return SYMPTOMS
            
    except Exception as e:
        logger.error(f"Error in calendar selection: {e}")
        
    return START_DATE

async def handle_symptoms(update: Update, context: CallbackContext):
    text = update.message.text
    lang = context.user_data.get('language', 'en')
    
    if 'symptoms' not in context.user_data:
        context.user_data['symptoms'] = []
    
    if text == get_message(lang, 'buttons', 'done'):
        # Move to medication selection
        final_symptoms = ", ".join(context.user_data['symptoms']) if context.user_data['symptoms'] else ""
        context.user_data['final_symptoms'] = final_symptoms
        
        # Create medication keyboard
        keyboard = []
        for med_row in MEDICATION_OPTIONS[lang]:
            keyboard.append(med_row)
        keyboard.append([get_message(lang, 'buttons', 'done')])
        
        markup = ReplyKeyboardMarkup(
            keyboard,
            one_time_keyboard=False,
            resize_keyboard=True
        )
        
        await update.message.reply_text(
            get_message(lang, 'cycle', 'select_medications'),
            reply_markup=markup
        )
        return MEDICATION
    
    # Add symptom if not already in list
    if text not in context.user_data['symptoms']:
        context.user_data['symptoms'].append(text)
        await update.message.reply_text(
            f"{get_message(lang, 'cycle', 'symptom_added')}: {text}\n"
            f"{get_message(lang, 'cycle', 'current_symptoms')}: {', '.join(context.user_data['symptoms'])}",
            reply_markup=update.message.reply_markup
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
    text = update.message.text
    
    # Initialize medications list if it doesn't exist
    if 'medications' not in context.user_data:
        context.user_data['medications'] = []
    
    if text == 'Done':
        # Join all medications with commas
        final_medications = ", ".join(context.user_data['medications']) if context.user_data['medications'] else ""
        context.user_data['medication'] = final_medications
        
        # Prepare cycle data
        cycle_data = {
            "start_date": context.user_data.get('start_date'),
            "symptoms": context.user_data.get('final_symptoms', ""),
            "medication": context.user_data.get('medication', "")
        }
        
        # Import user_tokens here to avoid circular import
        from bot import user_tokens
        chat_id = str(update.message.chat_id)
        
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
        
    elif text == 'Write Custom Medication':
        await update.message.reply_text(
            "Please type your medication and press 'Done' when finished:",
            reply_markup=ReplyKeyboardMarkup([['Done']], one_time_keyboard=True)
        )
        return MEDICATION
        
    elif text not in ['Done', 'Write Custom Medication']:
        # Add the medication to the list if it's not already there
        if text not in context.user_data['medications']:
            context.user_data['medications'].append(text)
            await update.message.reply_text(
                f"Added: {text}\nSelected medications: {', '.join(context.user_data['medications'])}\n\nSelect more or press 'Done'",
                reply_markup=ReplyKeyboardMarkup(MEDICATION_OPTIONS, one_time_keyboard=False)
            )
        return MEDICATION

async def cancel(update: Update, context: CallbackContext) -> int:
    """Handles canceling the operation and ends the conversation."""
    await update.message.reply_text("Operation cancelled.")
    return ConversationHandler.END

add_cycle_conversation = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex("^Add New Cycle$"), start_add_cycle)],
    states={
        START_DATE: [
            CallbackQueryHandler(handle_calendar_selection),
        ],
        SYMPTOMS: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, handle_symptoms)
        ],
        MEDICATION: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, handle_medication)
        ],
    },
    fallbacks=[MessageHandler(filters.Regex('^Cancel$'), cancel)],
    allow_reentry=True,
    per_chat=True,
    per_message=True,
    name="add_cycle_conversation"
)
