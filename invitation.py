import logging
import httpx
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext, ConversationHandler
from languages import get_message
from states import MENU, REGISTER, ACCEPTING_INVITATION
from config import BASE_URL
from auth import refresh_token

logger = logging.getLogger(__name__)

async def generate_invitation_code(update: Update, context: CallbackContext) -> int:
    """Generate invitation code for partner."""
    chat_id = str(update.message.chat_id)
    lang = context.user_data.get('language', 'en')

    # First check if user is authenticated
    from bot import user_tokens
    if chat_id not in user_tokens or "access" not in user_tokens[chat_id]:
        await update.message.reply_text(get_message(lang, 'auth', 'login_required'))
        return REGISTER

    access_token = user_tokens[chat_id]["access"]
    headers = {"Authorization": f"Bearer {access_token}"}

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{BASE_URL}/api/user/invitation/", headers=headers)

            if response.status_code == 401:  # Token expired
                new_token = await refresh_token(chat_id, user_tokens)
                if new_token:
                    headers["Authorization"] = f"Bearer {new_token}"
                    response = await client.post(f"{BASE_URL}/api/user/invitation/", headers=headers)
                else:
                    await update.message.reply_text(get_message(lang, 'auth', 'login_required'))
                    return REGISTER

            if response.status_code == 200:
                data = response.json()
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

    # First check if user is authenticated
    from bot import user_tokens
    if chat_id not in user_tokens or "access" not in user_tokens[chat_id]:
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

    # Check if user is authenticated
    from bot import user_tokens
    if chat_id not in user_tokens or "access" not in user_tokens[chat_id]:
        await update.message.reply_text(get_message(lang, 'auth', 'login_required'))
        return REGISTER

    access_token = user_tokens[chat_id]["access"]
    headers = {"Authorization": f"Bearer {access_token}"}
    data = {'code_to_accept': invitation_code}

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{BASE_URL}/api/user/invitation/",
                headers=headers,
                data=data
            )

            if response.status_code == 401:  # Token expired
                new_token = await refresh_token(chat_id, user_tokens)
                if new_token:
                    headers["Authorization"] = f"Bearer {new_token}"
                    response = await client.post(
                        f"{BASE_URL}/api/user/invitation/",
                        headers=headers,
                        data=data
                    )
                else:
                    await update.message.reply_text(get_message(lang, 'auth', 'login_required'))
                    return REGISTER

            if response.status_code == 200:
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