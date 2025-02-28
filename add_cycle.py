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
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def start_add_cycle(update, context):
    print("\n=== Starting Add Cycle Flow ===")
    logger.info("Starting add cycle process")
    
    chat_id = str(update.message.chat_id)
    lang = context.user_data.get('language', 'en')
    
    print(f"Chat ID: {chat_id}, Language: {lang}")
    logger.info(f"User {chat_id} starting add cycle with language {lang}")
    
    # First check if user is authenticated
    if 'user_tokens' not in context.bot_data:
        logger.warning(f"User {chat_id} not authenticated")
        await update.message.reply_text(get_message(lang, 'auth', 'login_required'))
        return ConversationHandler.END
    
    user_tokens = context.bot_data['user_tokens']
    if chat_id not in user_tokens or "access" not in user_tokens[chat_id]:
        logger.warning(f"User {chat_id} not authenticated")
        await update.message.reply_text(get_message(lang, 'auth', 'login_required'))
        return ConversationHandler.END
    
    # Show calendar for start date selection
    print("Creating calendar markup")
    from bot import calendar  # Import the global calendar instance
    calendar_markup = calendar.create_calendar()
    logger.info("Calendar markup created")
    
    await update.message.reply_text(
        get_message(lang, 'cycle', 'select_date'),
        reply_markup=calendar_markup
    )
    logger.info("Calendar displayed to user")
    return START_DATE

async def handle_calendar_selection(update: Update, context: CallbackContext):
    print("\n=== Calendar Selection Handler Started ===")
    query = update.callback_query
    
    if not query:
        print("ERROR: No callback query received")
        return START_DATE

    try:
        print(f"Received callback data: {query.data}")
        
        # Always answer the callback query first
        await query.answer()
        print("Callback query answered")
        
        from bot import calendar  # Import the global calendar instance
        
        # Process the selection using calendar keyboard's method
        result = calendar.process_calendar_selection(query)
        
        # If result is a tuple, it's a navigation action
        if isinstance(result, tuple):
            _, new_markup = result
            await query.message.edit_reply_markup(reply_markup=new_markup)
            return START_DATE
            
        # If result is a string, it's a date selection
        if isinstance(result, str):
            # Store the date
            context.user_data['start_date'] = result
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
            
            try:
                # Send confirmation and symptoms prompt
                await query.message.reply_text(
                    f"{get_message(lang, 'cycle', 'date_selected')}: {result}"
                )
                
                await query.message.reply_text(
                    get_message(lang, 'cycle', 'select_symptoms'),
                    reply_markup=markup
                )
                
                # Delete the calendar message
                await query.message.delete()
                
                return SYMPTOMS
                
            except Exception as e:
                print(f"Error in message handling: {e}")
                logger.error(f"Message handling error: {e}", exc_info=True)
                
    except Exception as e:
        print(f"ERROR in calendar selection handler: {e}")
        logger.error("Calendar selection error", exc_info=True)
        
    print("=== Calendar Selection Handler Completed ===")
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

# Add logging to calendar keyboard class
class CalendarKeyboard:
    def create_calendar(self, year=None, month=None):
        print("\n=== Creating Calendar ===")
        now = datetime.now()
        if year is None:
            year = now.year
        if month is None:
            month = now.month
            
        print(f"Creating calendar for {year}-{month}")
        logger.info(f"Creating calendar for {year}-{month}")
        
        # ... rest of the create_calendar code ...
        
        print("Calendar creation complete")
        return InlineKeyboardMarkup(keyboard)

    def process_calendar_selection(self, callback_query):
        print("\n=== Processing Calendar Selection ===")
        try:
            data = callback_query.data
            print(f"Processing callback data: {data}")
            logger.info(f"Processing calendar callback: {data}")
            
            if data == "ignore":
                print("Ignore button pressed")
                return None
                
            elif data.startswith(("prev_", "next_")):
                print("Navigation button pressed")
                _, year, month = data.split("_")
                year, month = int(year), int(month)
                print(f"Creating new calendar for {year}-{month}")
                return None, self.create_calendar(year, month)
                
            elif data.startswith("date_"):
                print("Date selection detected")
                selected_date = data.split("_")[1]
                print(f"Selected date: {selected_date}")
                return selected_date
                
        except Exception as e:
            print(f"Error processing calendar selection: {e}")
            logger.error(f"Calendar processing error: {str(e)}", exc_info=True)
            return None
            
        return None
