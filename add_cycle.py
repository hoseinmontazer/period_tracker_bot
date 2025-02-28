import logging
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    ConversationHandler, CallbackContext, MessageHandler,
    filters, CommandHandler, CallbackQueryHandler
)
import aiohttp
from states import START_DATE, SYMPTOMS, MEDICATION, MENU
from languages import get_message, SYMPTOM_OPTIONS, MEDICATION_OPTIONS
from calendar_keyboard import CalendarKeyboard
from menu_handlers import handle_menu  # Changed from bot to menu_handlers

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
    result = calendar.process_calendar_selection(query)
    
    if isinstance(result, tuple):
        # Navigation was selected, update the calendar
        _, new_markup = result
        await query.message.edit_reply_markup(reply_markup=new_markup)
        return START_DATE
    
    if result is None:
        return START_DATE
    
    # Date was selected
    context.user_data['start_date'] = result
    return await submit_cycle(update, context)

async def submit_cycle(update: Update, context: CallbackContext) -> int:
    """Submit the cycle data to the API."""
    chat_id = str(update.callback_query.message.chat_id)
    user_tokens = context.bot_data.get('user_tokens', {})
    access_token = user_tokens.get(chat_id, {}).get('access')
    lang = context.user_data.get('language', 'en')
    
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
                    # Show success message
                    await update.callback_query.message.reply_text(
                        get_message(lang, 'cycle', 'save_success'),
                        reply_markup=ReplyKeyboardRemove()
                    )
                    
                    # Show main menu
                    reply_keyboard = [
                        [{"text": get_message(lang, 'menu', 'track_period')}, 
                         {"text": get_message(lang, 'menu', 'view_history')}],
                        [{"text": get_message(lang, 'menu', 'cycle_analysis')}, 
                         {"text": get_message(lang, 'menu', 'add_new_cycle')}],
                        [{"text": get_message(lang, 'menu', 'partner_menu')}],
                        [{"text": get_message(lang, 'settings', 'menu')}]
                    ]

                    await update.callback_query.message.reply_text(
                        get_message(lang, 'menu', 'main'),
                        reply_markup=ReplyKeyboardMarkup(
                            reply_keyboard,
                            one_time_keyboard=True,
                            resize_keyboard=True
                        ),
                        parse_mode="Markdown"
                    )
                    # Return to MENU state instead of ending conversation
                    return MENU
                else:
                    await update.callback_query.message.reply_text(
                        get_message(lang, 'cycle', 'save_failed')
                    )
    
    except Exception as e:
        logger.error(f"Error submitting cycle: {e}")
        await update.callback_query.message.reply_text(
            get_message(lang, 'cycle', 'save_failed')
        )
    
    return ConversationHandler.END

# Update the conversation handler to include MENU state
add_cycle_conversation = ConversationHandler(
    entry_points=[MessageHandler(
        filters.Regex('^(➕ Add New Cycle|➕ افزودن دوره جدید)$'),
        start_add_cycle
    )],
    states={
        SYMPTOMS: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_symptoms)],
        MEDICATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_medication)],
        START_DATE: [CallbackQueryHandler(handle_calendar_selection)],
        MENU: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_menu)],  # Add menu state
    },
    fallbacks=[CommandHandler('cancel', lambda u, c: ConversationHandler.END)],
    name="add_cycle_conversation"
)
