import logging
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    ConversationHandler, CallbackContext, MessageHandler,
    filters, CommandHandler, CallbackQueryHandler
)
import aiohttp
from states import START_DATE, SYMPTOMS, MEDICATION
from languages import get_message, SYMPTOM_OPTIONS, MEDICATION_OPTIONS
from calendar_keyboard import CalendarKeyboard

logger = logging.getLogger(__name__)
calendar = CalendarKeyboard()

async def start_add_cycle(update: Update, context: CallbackContext) -> int:
    """Start the add cycle conversation with symptoms selection."""
    lang = context.user_data.get('language', 'en')
    
    # Show symptoms options first
    symptom_keyboard = [[option] for option in SYMPTOM_OPTIONS.get(lang, [])]
    symptom_keyboard.append([get_message(lang, 'general', 'done')])
    
    await update.message.reply_text(
        get_message(lang, 'cycle', 'select_symptoms'),
        reply_markup=ReplyKeyboardMarkup(symptom_keyboard, one_time_keyboard=True)
    )
    context.user_data['symptoms'] = []
    return SYMPTOMS

async def handle_symptoms(update: Update, context: CallbackContext) -> int:
    """Handle symptom selection."""
    text = update.message.text
    lang = context.user_data.get('language', 'en')
    
    if text == get_message(lang, 'general', 'done'):
        # Move to medication selection
        medication_keyboard = [[option] for option in MEDICATION_OPTIONS.get(lang, [])]
        medication_keyboard.append([get_message(lang, 'general', 'done')])
        
        await update.message.reply_text(
            get_message(lang, 'cycle', 'select_medication'),
            reply_markup=ReplyKeyboardMarkup(medication_keyboard, one_time_keyboard=True)
        )
        context.user_data['medication'] = []
        return MEDICATION
    
    if text in SYMPTOM_OPTIONS.get(lang, []):
        if 'symptoms' not in context.user_data:
            context.user_data['symptoms'] = []
        context.user_data['symptoms'].append(text)
        await update.message.reply_text(get_message(lang, 'cycle', 'symptom_added'))
    
    return SYMPTOMS

async def handle_medication(update: Update, context: CallbackContext) -> int:
    """Handle medication selection."""
    text = update.message.text
    lang = context.user_data.get('language', 'en')
    
    if text == get_message(lang, 'general', 'done'):
        # Move to date selection
        await update.message.reply_text(
            get_message(lang, 'cycle', 'select_start_date'),
            reply_markup=calendar.create_calendar()
        )
        return START_DATE
    
    if text in MEDICATION_OPTIONS.get(lang, []):
        if 'medication' not in context.user_data:
            context.user_data['medication'] = []
        context.user_data['medication'].append(text)
        await update.message.reply_text(get_message(lang, 'cycle', 'medication_added'))
    
    return MEDICATION

async def handle_calendar_selection(update: Update, context: CallbackContext) -> int:
    """Handle the calendar date selection and submit the cycle data."""
    query = update.callback_query
    selected_date = calendar.handle_calendar_selection(query)
    
    if selected_date is None:
        return START_DATE
    
    context.user_data['start_date'] = selected_date.strftime("%Y-%m-%d")
    return await submit_cycle(update, context)

async def submit_cycle(update: Update, context: CallbackContext) -> int:
    """Submit the cycle data to the API."""
    chat_id = str(update.callback_query.message.chat_id)  # Updated to use callback_query
    user_tokens = context.bot_data.get('user_tokens', {})
    access_token = user_tokens.get(chat_id, {}).get('access')
    
    if not access_token:
        await update.callback_query.message.reply_text("Please login first.")
        return ConversationHandler.END
    
    try:
        async with aiohttp.ClientSession() as session:
            headers = {'Authorization': f'Bearer {access_token}'}
            data = {
                'start_date': context.user_data['start_date'],
                'symptoms': ','.join(context.user_data.get('symptoms', [])),
                'medication': ','.join(context.user_data.get('medication', []))
            }
            
            async with session.post(
                'https://api-period.shirpala.ir/api/periods/',
                headers=headers,
                data=data
            ) as response:
                if response.status == 201:
                    await update.callback_query.message.reply_text(
                        get_message(context.user_data.get('language', 'en'), 'cycle', 'add_success'),
                        reply_markup=ReplyKeyboardRemove()
                    )
                else:
                    await update.callback_query.message.reply_text(
                        get_message(context.user_data.get('language', 'en'), 'cycle', 'add_error')
                    )
    
    except Exception as e:
        logger.error(f"Error submitting cycle: {e}")
        await update.callback_query.message.reply_text(
            get_message(context.user_data.get('language', 'en'), 'cycle', 'add_error')
        )
    
    return ConversationHandler.END

# Create the conversation handler
add_cycle_conversation = ConversationHandler(
    entry_points=[MessageHandler(
        filters.Regex('^(Add New Cycle|چرخه جدید)$'),
        start_add_cycle
    )],
    states={
        SYMPTOMS: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_symptoms)],
        MEDICATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_medication)],
        START_DATE: [CallbackQueryHandler(handle_calendar_selection)],
    },
    fallbacks=[CommandHandler('cancel', lambda u, c: ConversationHandler.END)],
    name="add_cycle_conversation"
)
