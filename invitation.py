import logging
import uuid
import aiohttp
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext
from languages import get_message
from states import MENU, ACCEPTING_INVITATION, SETTINGS

logger = logging.getLogger(__name__)

async def generate_invitation_code(update: Update, context: CallbackContext) -> int:
    """Generate and display invitation code for partner."""
    chat_id = str(update.message.chat_id)
    lang = context.user_data.get('language', 'en')
    
    try:
        # Get the user's access token
        from utils import load_tokens
        user_tokens = load_tokens()
        
        if chat_id not in user_tokens or "access" not in user_tokens[chat_id]:
            await update.message.reply_text(get_message(lang, 'auth', 'login_required'))
            return MENU

        access_token = user_tokens[chat_id]["access"]
        
        # Make API call to generate invitation code
        async with aiohttp.ClientSession() as session:
            async with session.post(
                'https://api-period.shirpala.ir/api/user/invitation/',
                headers={"Authorization": f"Bearer {access_token}"}
            ) as response:
                if response.status == 200 or response.status == 201:
                    data = await response.json()
                    invitation_code = data.get('invitation_code')
                    
                    # Store the invitation code in user_data
                    context.user_data['invitation_code'] = invitation_code
                    
                    # Send the code to the user
                    await update.message.reply_text(
                        get_message(lang, 'invitation', 'code_generated').format(invitation_code),
                        reply_markup=ReplyKeyboardMarkup([[get_message(lang, 'menu', 'back_to_main')]], 
                                                      one_time_keyboard=True)
                    )
                    return SETTINGS
                else:
                    logger.error(f"Failed to generate invitation code. Status: {response.status}")
                    await update.message.reply_text(get_message(lang, 'invitation', 'generation_error'))
                    return SETTINGS
                    
    except Exception as e:
        logger.error(f"Error generating invitation code: {str(e)}")
        await update.message.reply_text(get_message(lang, 'invitation', 'generation_error'))
        return SETTINGS

async def start_accept_invitation(update: Update, context: CallbackContext) -> int:
    """Start the invitation acceptance process."""
    lang = context.user_data.get('language', 'en')
    
    await update.message.reply_text(
        get_message(lang, 'invitation', 'enter_code'),
        reply_markup=ReplyKeyboardMarkup([[get_message(lang, 'menu', 'back_to_main')]], 
                                      one_time_keyboard=True)
    )
    return ACCEPTING_INVITATION

async def accept_invitation(update: Update, context: CallbackContext) -> int:
    """Process the invitation code."""
    text = update.message.text
    chat_id = str(update.message.chat_id)
    lang = context.user_data.get('language', 'en')
    
    if text == get_message(lang, 'menu', 'back_to_main'):
        from bot import show_main_menu
        return await show_main_menu(update, context)
    
    try:
        # Here you would typically make an API call to validate and process the invitation code
        # For example:
        # async with aiohttp.ClientSession() as session:
        #     async with session.post('your_api_endpoint', json={'code': text}) as response:
        #         if response.status == 200:
        #             # Success
        
        # For now, we'll just show a success message
        await update.message.reply_text(
            get_message(lang, 'invitation', 'accepted'),
            reply_markup=ReplyKeyboardMarkup([[get_message(lang, 'menu', 'back_to_main')]], 
                                          one_time_keyboard=True)
        )
        
        return MENU
        
    except Exception as e:
        logger.error(f"Error accepting invitation: {str(e)}")
        await update.message.reply_text(get_message(lang, 'invitation', 'acceptance_error'))
        return MENU