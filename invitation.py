import logging
import aiohttp
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext, ConversationHandler
from languages import get_message
from states import MENU, REGISTER, ACCEPTING_INVITATION

logger = logging.getLogger(__name__)

async def generate_invitation_code(update: Update, context: CallbackContext) -> int:
    """Generate invitation code for partner."""
    chat_id = str(update.message.chat_id)
    lang = context.user_data.get('language', 'en')

    if chat_id not in context.bot_data.get('user_tokens', {}) or "access" not in context.bot_data['user_tokens'][chat_id]:
        await update.message.reply_text(get_message(lang, 'auth', 'login_required'))
        return REGISTER

    try:
        async with aiohttp.ClientSession() as session:
            headers = {
                'Authorization': f'Bearer {context.bot_data["user_tokens"][chat_id]["access"]}'
            }
            async with session.post(
                'https://api-period.shirpala.ir/api/user/invitation/',
                headers=headers
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    invitation_code = data.get('code', 'No code received')
                    await update.message.reply_text(
                        f"✨ Your invitation code is: {invitation_code}\n\n"
                        f"Share this code with your partner. They can accept it using the 'Accept Invitation Code' option in their menu."
                    )
                else:
                    response_text = await response.text()
                    await update.message.reply_text(f"Failed to generate invitation code: {response_text}")
    except Exception as e:
        logger.error(f"Error generating invitation code: {str(e)}")
        await update.message.reply_text("An error occurred while generating the invitation code.")

    return MENU

async def start_accept_invitation(update: Update, context: CallbackContext) -> int:
    """Start the process of accepting an invitation code."""
    chat_id = str(update.message.chat_id)
    lang = context.user_data.get('language', 'en')

    if chat_id not in context.bot_data.get('user_tokens', {}) or "access" not in context.bot_data['user_tokens'][chat_id]:
        await update.message.reply_text(get_message(lang, 'auth', 'login_required'))
        return REGISTER

    await update.message.reply_text(
        "Please enter the invitation code you received from your partner:\n"
        "(You can cancel this operation by typing /cancel)"
    )
    return ACCEPTING_INVITATION

async def accept_invitation(update: Update, context: CallbackContext) -> int:
    """Handle the invitation code acceptance."""
    chat_id = str(update.message.chat_id)
    lang = context.user_data.get('language', 'en')
    invitation_code = update.message.text.strip()

    if not invitation_code.isdigit():
        await update.message.reply_text("Please enter a valid numeric code.")
        return ACCEPTING_INVITATION

    try:
        async with aiohttp.ClientSession() as session:
            headers = {
                'Authorization': f'Bearer {context.bot_data["user_tokens"][chat_id]["access"]}'
            }
            data = {
                'code_to_accept': invitation_code
            }
            
            async with session.post(
                'https://api-period.shirpala.ir/api/user/invitation/',
                headers=headers,
                data=data
            ) as response:
                if response.status == 200:
                    await update.message.reply_text("✅ Partner invitation accepted successfully!")
                else:
                    response_text = await response.text()
                    await update.message.reply_text(
                        f"❌ Failed to accept invitation code.\n"
                        f"Error: {response_text}\n\n"
                        f"Please check the code and try again, or use /cancel to cancel."
                    )
                    return ACCEPTING_INVITATION
    except Exception as e:
        logger.error(f"Error accepting invitation code: {str(e)}")
        await update.message.reply_text(
            "An error occurred while accepting the invitation code.\n"
            "Please try again or use /cancel to cancel."
        )
        return ACCEPTING_INVITATION

    return MENU 