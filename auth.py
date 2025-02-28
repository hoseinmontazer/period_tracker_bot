import httpx
import aiohttp
import logging
from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler
from states import REGISTER, MENU
from utils import load_tokens, save_tokens
from config import BASE_URL
from menu_handlers import show_main_menu

logger = logging.getLogger(__name__)

async def authenticate_user(username, password):
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{BASE_URL}/api/auth/jwt/create/", data={"username": username, "password": password})

        if response.status_code == 200:
            json_response = response.json()
            return json_response.get("access")

        return None

async def refresh_token(chat_id, user_tokens):
    """Refresh the access token using the refresh token."""
    if chat_id not in user_tokens or "refresh" not in user_tokens[chat_id]:
        return None

    refresh_token = user_tokens[chat_id]["refresh"]
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{BASE_URL}/api/auth/jwt/refresh/", data={"refresh": refresh_token})

        if response.status_code == 200:
            new_access = response.json().get("access")
            user_tokens[chat_id]["access"] = new_access
            save_tokens(user_tokens)
            return new_access
        return None

async def handle_registration(update: Update, context: CallbackContext) -> int:
    """Handle the registration process step by step."""
    current_step = context.user_data.get('registration_step', 'username')
    user_input = update.message.text
    
    logger.info(f"Registration step: {current_step}, Input: {user_input}")
    
    if current_step == 'username':
        context.user_data['username'] = user_input
        logger.info(f"Username set: {user_input}")
        await update.message.reply_text("Enter your password:")
        context.user_data['registration_step'] = 'password'
        return REGISTER
    
    elif current_step == 'password':
        context.user_data['password'] = user_input
        logger.info("Password received and stored")
        await update.message.reply_text("Enter your email address (e.g., example@gmail.com):")
        context.user_data['registration_step'] = 'email'
        return REGISTER
    
    elif current_step == 'email':
        if '@' not in user_input or '.' not in user_input:
            logger.warning(f"Invalid email format: {user_input}")
            await update.message.reply_text("Please enter a valid email address (e.g., example@gmail.com):")
            return REGISTER
        
        context.user_data['email'] = user_input
        logger.info(f"Email set: {user_input}")
        await update.message.reply_text("Please select your sex (male/female):")
        context.user_data['registration_step'] = 'sex'
        return REGISTER
            
    elif current_step == 'sex':
        if user_input.lower() not in ['male', 'female']:
            logger.warning(f"Invalid sex input: {user_input}")
            await update.message.reply_text("Please enter either 'male' or 'female':")
            return REGISTER
            
        logger.info(f"Sex set: {user_input}")
        # Make API call to register user
        try:
            async with aiohttp.ClientSession() as session:
                data = {
                    'username': context.user_data['username'],
                    'password': context.user_data['password'],
                    're_password': context.user_data['password'],
                    'email': context.user_data['email'],
                    'sex': user_input.lower()
                }
                logger.info(f"Sending registration request with data: {data}")
                
                async with session.post(f'{BASE_URL}/api/auth/users/', data=data) as response:
                    response_text = await response.text()
                    logger.info(f"Registration response status: {response.status}")
                    logger.info(f"Registration response body: {response_text}")
                    
                    if response.status == 201:
                        logger.info("Registration successful")
                        await update.message.reply_text("Registration successful!")
                        # Auto-login the user
                        token = await authenticate_user(context.user_data['username'], context.user_data['password'])
                        if token:
                            chat_id = str(update.message.chat_id)
                            user_tokens = load_tokens()
                            user_tokens[chat_id] = {"access": token}
                            save_tokens(user_tokens)
                            context.user_data.clear()
                            logger.info(f"Auto-login successful for user: {data['username']}")
                            return await show_main_menu(update, context)
                        else:
                            logger.error("Auto-login failed after successful registration")
                            await update.message.reply_text("Registration successful but login failed. Please use /start to login.")
                            return ConversationHandler.END
                    else:
                        error_msg = f"Registration failed. Server response: {response_text}"
                        logger.error(error_msg)
                        await update.message.reply_text(error_msg)
                        return REGISTER
                    
        except Exception as e:
            error_msg = f"Registration error: {str(e)}"
            logger.error(error_msg)
            await update.message.reply_text("An error occurred during registration. Please try again.")
            return REGISTER

