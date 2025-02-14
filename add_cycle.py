from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import CallbackContext, ConversationHandler, MessageHandler, filters
from telegram import Update
from states import MENU, START_DATE, END_DATE, SYMPTOMS, MEDICATION


# Define the states for adding a new cycle
START_DATE, END_DATE, SYMPTOMS, MEDICATION = range(4)

# This is the function for starting the add cycle conversation
async def start_add_cycle(update, context):
    # Create custom keyboard with "Skip" option
    reply_keyboard = [['Skip']]
    await update.message.reply_text(
        "Enter the start date of your new cycle (YYYY-MM-DD):",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )
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

# State handler for capturing medication
async def handle_medication(update, context):
    if update.message.text.lower() == 'skip':
        context.user_data['medication'] = None
    else:
        context.user_data['medication'] = update.message.text.strip() or ""
    
    # Use ReplyKeyboardRemove to clear the keyboard
    await update.message.reply_text(
        "✅ Cycle data has been saved successfully!",
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
    return MENU

# Cancel handler
async def cancel(update: Update, context: CallbackContext) -> int:
    """Handles canceling the operation and ends the conversation."""
    await update.message.reply_text("Operation cancelled.")
    return ConversationHandler.END

add_cycle_conversation = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex("^Add New Cycle$"), start_add_cycle)],  # Start cycle addition
    states={
        START_DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_start_date)],  
        END_DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_end_date)],  
        SYMPTOMS: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_symptoms)],  
        MEDICATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_medication)],  
    },
    fallbacks=[MessageHandler(filters.Regex('^Cancel$'), cancel)],  
    allow_reentry=True  # <-- Add this so the user can restart the conversation
)
