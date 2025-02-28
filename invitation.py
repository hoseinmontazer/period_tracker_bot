import logging
import uuid
import aiohttp
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext
from languages import get_message
from states import MENU, ACCEPTING_INVITATION

logger = logging.getLogger(__name__)

async def generate_invitation_code(update: Update, context: CallbackContext) -> int:
    """Generate and display invitation code for partner."""
    chat_id = str(update.message.chat_id)
    lang = context.user_data.get('language', 'en')
    
    try:
        # Generate a unique invitation code
        invitation_code = str(uuid.uuid4())[:8]
        
        # Store the invitation code in user_data
        context.user_data['invitation_code'] = invitation_code
        
        # Send the code to the user
        await update.message.reply_text(
            get_message(lang, 'invitation', 'code_generated').format(invitation_code),
            reply_markup=ReplyKeyboardMarkup([[get_message(lang, 'menu', 'back_to_main')]], 
                                          one_time_keyboard=True)
        )
        
        return MENU
        
    except Exception as e:
        logger.error(f"Error generating invitation code: {str(e)}")
        await update.message.reply_text(get_message(lang, 'invitation', 'generation_error'))
        return MENU

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
    invitation_code = update.message.text
    chat_id = str(update.message.chat_id)
    lang = context.user_data.get('language', 'en')
    
    if invitation_code == get_message(lang, 'menu', 'back_to_main'):
        return MENU
    
    try:
        # Here you would typically make an API call to validate and process the invitation code
        # For example:
        # async with aiohttp.ClientSession() as session:
        #     async with session.post('your_api_endpoint', json={'code': invitation_code}) as response:
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