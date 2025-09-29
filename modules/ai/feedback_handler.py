# ========== HANDLE FEEDBACK ==========
from venv import logger
import aiohttp
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import ContextTypes, ConversationHandler
from utils.token_store import get_token
from constants import DASHBOARD, FEEDBACK_TEXT
from modules.ai.api import send_feedback_to_api


async def feedback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("In feedback_handler")
    query = update.callback_query
    await query.answer()

    _, suggestion_id, feedback_value = query.data.split(":")

    chat_id = update.effective_chat.id
    token = context.user_data.get("token") or get_token(chat_id)



    if not token:
        await query.edit_message_text("⚠️ You are not logged in!")
        return

    if feedback_value == "true":
        
        result = await send_feedback_to_api(suggestion_id, token, True)
        print(result)
        if result and result.get("status") == "success":
            await query.edit_message_text("✅ Thanks for your feedback!")
            
            return DASHBOARD
        else:
            await query.edit_message_text("❌ Failed to send feedback. Please try again later.")
        return DASHBOARD
    else:
        print("User indicated the suggestion was not helpful. Starting text feedback.")
        
        # 1. Store the suggestion ID
        context.user_data["pending_feedback_id"] = suggestion_id
        
        # 2. EDIT the ORIGINAL MESSAGE to remove the inline keyboard and update the text.
        #    Crucially, we do NOT pass a ReplyKeyboardMarkup here. We pass None 
        #    or an InlineKeyboardMarkup.
        await query.edit_message_text(
            "❌ Sorry it wasn’t helpful. "
            "Please send the correct label in a **new message**.",
            # Pass reply_markup=None to remove the old Inline Keyboard
            reply_markup=None 
        )

        # 3. SEND A NEW MESSAGE with the ReplyKeyboardMarkup (the one for text input).
        keyboard = [["⬅️ Back to Dashboard"]]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
        
        # The ReplyKeyboardMarkup must be sent via context.bot.send_message
        await context.bot.send_message(
            chat_id=chat_id,
            text="Type the corrected label below, or tap the button to go back to the dashboard:",
            reply_markup=reply_markup
        )
        
        # The next state in the conversation is FEEDBACK_TEXT
        return FEEDBACK_TEXT



async def text_feedback_handler(update, context):
    print("In text_feedback_handler")

    chat_id = update.effective_chat.id
    token = context.user_data.get("token") or get_token(chat_id)


    suggestion_id = context.user_data.get("pending_feedback_id")
    if not suggestion_id:
        return DASHBOARD  

    text = update.message.text

    keyboard = [["⬅️ Back to Dashboard"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    if text == "⬅️ Back to Dashboard":
        context.user_data.pop("pending_feedback_id", None)
        from modules.users.handlers import show_dashboard
        return await show_dashboard(update, context)

    corrected_label = text
    print("Corrected label:", corrected_label)
    resualt = await send_feedback_to_api(suggestion_id, token, False, corrected_label, corrected_label)
    print(resualt)
    await update.message.reply_text(
        "🙏 Thanks, your feedback will help improve the AI!",
        reply_markup=ReplyKeyboardMarkup([["⬅️ Back to Dashboard"]], resize_keyboard=True)
    )

    context.user_data.pop("pending_feedback_id", None)
    
    return DASHBOARD  # یا MAIN_MENU







