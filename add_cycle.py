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
    
    # Get symptoms for the current language with fallback to English
    symptoms = SYMPTOM_OPTIONS.get(lang, SYMPTOM_OPTIONS.get('en', []))
    
    if not symptoms:
        logger.error(f"No symptoms found for language {lang}")
        await update.message.reply_text(
            "Error: No symptoms available. Please contact support.",
            reply_markup=ReplyKeyboardRemove()
        )
        return ConversationHandler.END
    
    # Create keyboard with symptoms using the predefined structure
    symptom_keyboard = [[{"text": str(item)} for item in row] for row in symptoms]
    
    try:
        await update.message.reply_text(
            get_message(lang, 'cycle', 'select_symptoms'),
            reply_markup=ReplyKeyboardMarkup(
                symptom_keyboard,
                one_time_keyboard=False,  # Allow multiple selections
                resize_keyboard=True
            )
        )
        context.user_data['symptoms'] = []
        return SYMPTOMS
    except Exception as e:
        logger.error(f"Error creating symptoms keyboard: {e}")
        await update.message.reply_text(
            "An error occurred. Please try again or contact support.",
            reply_markup=ReplyKeyboardRemove()
        )
        return ConversationHandler.END

async def handle_symptoms(update: Update, context: CallbackContext) -> int:
    """Handle symptom selection."""
    text = update.message.text
    lang = context.user_data.get('language', 'en')
    done_text = get_message(lang, 'buttons', 'done')
    
    if text == done_text:
        # Move to medication selection
        medications = MEDICATION_OPTIONS.get(lang, MEDICATION_OPTIONS.get('en', []))
        medication_keyboard = [[{"text": str(item)} for item in row] for row in medications]
        
        await update.message.reply_text(
            get_message(lang, 'cycle', 'select_medications'),
            reply_markup=ReplyKeyboardMarkup(
                medication_keyboard,
                one_time_keyboard=False,  # Allow multiple selections
                resize_keyboard=True
            )
        )
        context.user_data['medication'] = []
        return MEDICATION
    
    # Handle custom symptoms
    custom_symptoms_text = get_message(lang, 'buttons', 'write_custom_symptoms')
    if text == custom_symptoms_text:
        await update.message.reply_text(get_message(lang, 'cycle', 'custom_symptoms'))
        return SYMPTOMS
    
    # Add the symptom if it's not a control button
    if text not in [custom_symptoms_text, done_text]:
        if 'symptoms' not in context.user_data:
            context.user_data['symptoms'] = []
        if text not in context.user_data['symptoms']:
            context.user_data['symptoms'].append(text)
            await update.message.reply_text(
                get_message(lang, 'cycle', 'added_item', 
                text, 
                get_message(lang, 'period_history', 'symptoms_title'),
                ', '.join(context.user_data['symptoms']))
            )
    
    return SYMPTOMS

async def handle_medication(update: Update, context: CallbackContext) -> int:
    """Handle medication selection."""
    text = update.message.text
    lang = context.user_data.get('language', 'en')
    done_text = get_message(lang, 'buttons', 'done')
    
    if text == done_text:
        # Move to date selection
        await update.message.reply_text(
            get_message(lang, 'cycle', 'select_date'),
            reply_markup=calendar.create_calendar()
        )
        return START_DATE
    
    # Handle custom medication
    custom_med_text = get_message(lang, 'buttons', 'write_custom_medication')
    if text == custom_med_text:
        await update.message.reply_text(get_message(lang, 'cycle', 'custom_medication'))
        return MEDICATION
    
    # Add the medication if it's not a control button
    if text not in [custom_med_text, done_text]:
        if 'medication' not in context.user_data:
            context.user_data['medication'] = []
        if text not in context.user_data['medication']:
            context.user_data['medication'].append(text)
            await update.message.reply_text(
                get_message(lang, 'cycle', 'added_item',
                text,
                get_message(lang, 'period_history', 'medicine_title'),
                ', '.join(context.user_data['medication']))
            )
    
    return MEDICATION

async def handle_calendar_selection(update: Update, context: CallbackContext) -> int:
    """Handle the calendar date selection and submit the cycle data."""
    query = update.callback_query
    selected_date = calendar.process_calendar_selection(query)
    
    if selected_date is None:
        return START_DATE
    
    # The selected_date is already in YYYY-MM-DD format, no need for strftime
    context.user_data['start_date'] = selected_date
    return await submit_cycle(update, context)

async def submit_cycle(update: Update, context: CallbackContext) -> int:
    """Submit the cycle data to the API."""
    chat_id = str(update.callback_query.message.chat_id)
    user_tokens = context.bot_data.get('user_tokens', {})
    access_token = user_tokens.get(chat_id, {}).get('access')
    
    if not access_token:
        await update.callback_query.message.reply_text("Please login first.")
        return ConversationHandler.END
    
    try:
        async with aiohttp.ClientSession() as session:
            headers = {'Authorization': f'Bearer {access_token}'}
            data = {
                'start_date': context.user_data['start_date'],  # Already in YYYY-MM-DD format
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
                        get_message(context.user_data.get('language', 'en'), 'cycle', 'save_success'),
                        reply_markup=ReplyKeyboardRemove()
                    )
                else:
                    await update.callback_query.message.reply_text(
                        get_message(context.user_data.get('language', 'en'), 'cycle', 'save_failed')
                    )
    
    except Exception as e:
        logger.error(f"Error submitting cycle: {e}")
        await update.callback_query.message.reply_text(
            get_message(context.user_data.get('language', 'en'), 'cycle', 'save_failed')
        )
    
    return ConversationHandler.END

# Create the conversation handler
add_cycle_conversation = ConversationHandler(
    entry_points=[MessageHandler(
        filters.Regex('^(➕ Add New Cycle|➕ افزودن دوره جدید)$'),
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
