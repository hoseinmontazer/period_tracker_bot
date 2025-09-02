import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    ConversationHandler, CallbackContext, MessageHandler,
    filters, CommandHandler, CallbackQueryHandler
)
import aiohttp
from menus import get_main_menu
from states import START_DATE, SYMPTOMS, MEDICATION, MENU
from languages import get_message, SYMPTOM_OPTIONS, MEDICATION_OPTIONS
from handlers.calenders.calendar_keyboard import CalendarKeyboard

logger = logging.getLogger(__name__)
calendar = CalendarKeyboard()


async def start_add_cycle(update: Update, context: CallbackContext) -> int:
    """Start the add cycle conversation with symptoms selection."""
    lang = context.user_data.get('language', 'en')
    done_text = get_message(lang, 'buttons', 'done')
    cancel_text = get_message(lang, 'buttons', 'cancel')

    # Get symptoms
    symptoms = SYMPTOM_OPTIONS.get(lang, SYMPTOM_OPTIONS.get('en', []))
    if not symptoms:
        logger.error(f"No symptoms found for language {lang}")
        await update.message.reply_text(
            "Error: No symptoms available. Please contact support.",
            reply_markup=ReplyKeyboardRemove()
        )
        return ConversationHandler.END

    # Build keyboard
    symptom_keyboard = [[str(item) for item in row] for row in symptoms]
    symptom_keyboard.append([done_text, cancel_text])

    # Send message
    await update.message.reply_text(
        get_message(lang, 'cycle', 'select_symptoms'),
        reply_markup=ReplyKeyboardMarkup(
            symptom_keyboard,
            one_time_keyboard=False,
            resize_keyboard=True
        )
    )
    context.user_data['symptoms'] = []
    return SYMPTOMS


async def handle_symptoms(update: Update, context: CallbackContext) -> int:
    text = update.message.text
    lang = context.user_data.get('language', 'en')
    done_text = get_message(lang, 'buttons', 'done')
    cancel_text = get_message(lang, 'buttons', 'cancel')
    custom_text = get_message(lang, 'buttons', 'write_custom_symptoms')

    if 'symptoms' not in context.user_data:
        context.user_data['symptoms'] = []

    if text == cancel_text:
        await update.message.reply_text(
            get_message(lang, 'cycle', 'cancelled'),
            reply_markup=ReplyKeyboardRemove()
        )

        markup, menu_text = get_main_menu(lang)
        await update.message.reply_text(menu_text, reply_markup=markup)

        return ConversationHandler.END

    # Done → move to medication
    if text == done_text:
        print("User finished selecting symptoms:", context.user_data['symptoms'])
        medications = MEDICATION_OPTIONS.get(lang, MEDICATION_OPTIONS.get('en', []))
        medication_keyboard = [[str(item) for item in row] for row in medications]
        medication_keyboard.append([done_text, cancel_text])
        await update.message.reply_text(
            get_message(lang, 'cycle', 'select_medications'),
            reply_markup=ReplyKeyboardMarkup(
                medication_keyboard,
                one_time_keyboard=False,
                resize_keyboard=True
            )
        )
        context.user_data['medication'] = []
        return MEDICATION

    # Custom symptom
    if text == custom_text:
        await update.message.reply_text(get_message(lang, 'cycle', 'custom_symptoms'))
        return SYMPTOMS

    # Normal symptom
    if text not in context.user_data['symptoms']:
        context.user_data['symptoms'].append(text)
        await update.message.reply_text(
            f"✅ Added: {text}\nCurrent: {', '.join(context.user_data['symptoms'])}"
        )
    else:
        await update.message.reply_text(f"⚠️ Already added: {text}")

    return SYMPTOMS


async def handle_medication(update: Update, context: CallbackContext) -> int:
    """Handle medication selection."""
    text = update.message.text
    lang = context.user_data.get('language', 'en')
    done_text = get_message(lang, 'buttons', 'done')
    cancel_text = get_message(lang, 'buttons', 'cancel')
    custom_med_text = get_message(lang, 'buttons', 'write_custom_medication')

    if text == cancel_text:
        await update.message.reply_text(
            get_message(lang, 'cycle', 'cancelled'),
            reply_markup=ReplyKeyboardRemove()
        )

        markup, menu_text = get_main_menu(lang)
        await update.message.reply_text(menu_text, reply_markup=markup)

        return ConversationHandler.END

    if text == done_text:
        # Remove the medication keyboard first
        await update.message.reply_text(
            "✓",  # Send a quick message to clear the keyboard
            reply_markup=ReplyKeyboardRemove()
        )
        
        # Create calendar and get the keyboard layout
        calendar_markup = calendar.create_calendar()
        
        # Extract the keyboard rows from the markup and convert to list
        keyboard = list(calendar_markup.inline_keyboard)
        
        # Add cancel button as a new row
        cancel_button = InlineKeyboardButton(cancel_text, callback_data="calendar_cancel")
        keyboard.append([cancel_button])
        
        # Create new markup with the cancel button
        updated_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            get_message(lang, 'cycle', 'select_date'),
            reply_markup=updated_markup
        )
        return START_DATE






    if text == custom_med_text:
        await update.message.reply_text(get_message(lang, 'cycle', 'custom_medication'))
        return MEDICATION

    if 'medication' not in context.user_data:
        context.user_data['medication'] = []

    if text not in context.user_data['medication']:
        context.user_data['medication'].append(text)
        await update.message.reply_text(
            f"✅ Added: {text}\nCurrent: {', '.join(context.user_data['medication'])}"
        )
    else:
        await update.message.reply_text(f"⚠️ Already added: {text}")

    return MEDICATION


async def handle_calendar_selection(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    result = calendar.process_calendar_selection(query)

    if isinstance(result, tuple):
        _, new_markup = result
        await query.message.edit_reply_markup(reply_markup=new_markup)
        return START_DATE

    if result is None:
        return START_DATE

    context.user_data['start_date'] = result
    return await submit_cycle(update, context)


async def submit_cycle(update: Update, context: CallbackContext) -> int:
    """Submit cycle data to API."""
    query = update.callback_query
    await query.answer()
    
    chat_id = str(query.message.chat_id)
    user_tokens = context.bot_data.get('user_tokens', {})
    access_token = user_tokens.get(chat_id, {}).get('access')
    lang = context.user_data.get('language', 'en')

    if not access_token:
        await query.message.reply_text("Please login first.")
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
                    await query.message.reply_text(
                        get_message(lang, 'cycle', 'save_success'),
                        reply_markup=ReplyKeyboardRemove()
                    )

                    # Show main menu once, but end conversation
                    markup, menu_text = get_main_menu(lang)
                    await query.message.reply_text(
                        menu_text,
                        reply_markup=markup,
                        parse_mode="Markdown"
                    )

                    # ✅ End conversation here
                    return ConversationHandler.END  

                else:
                    await query.message.reply_text(
                        get_message(lang, 'cycle', 'save_failed')
                    )
                    markup, menu_text = get_main_menu(lang)
                    await query.message.reply_text(menu_text, reply_markup=markup)
                    return ConversationHandler.END

    except Exception as e:
        logger.error(f"Error submitting cycle: {e}")
        await query.message.reply_text(
            get_message(lang, 'cycle', 'save_failed')
        )
        # Use callback_query.message instead of update.message
        markup, menu_text = get_main_menu(lang)
        await query.message.reply_text(menu_text, reply_markup=markup)
        return ConversationHandler.END
        
async def handle_cancel(update: Update, context: CallbackContext) -> int:
    print("Add cycle conversation cancelled by user")
    lang = context.user_data.get('language', 'en')

    await update.message.reply_text(
        get_message(lang, 'cycle', 'cancelled'),
        reply_markup=ReplyKeyboardRemove()
    )
    print("Preparing to show main menu")
    reply_markup = get_main_menu(lang)  
    print("Main menu markup:", reply_markup)
    await update.message.reply_text(
        get_message(lang, 'menu', 'main'),
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

    return MENU 




# Conversation handler
add_cycle_conversation = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex('^(➕ Add New Cycle|➕ افزودن دوره جدید)$'), start_add_cycle)],
    states={
        SYMPTOMS: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_symptoms)],
        MEDICATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_medication)],
        START_DATE: [CallbackQueryHandler(handle_calendar_selection)],
    },
    fallbacks=[CommandHandler('cancel', handle_cancel)],
    name="add_cycle_conversation"
)