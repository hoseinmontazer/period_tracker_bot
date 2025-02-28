import logging
import httpx
import aiohttp
from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler
from states import REGISTER, MENU
from utils import load_tokens, save_tokens
from config import BASE_URL
from menu_handlers import show_main_menu

logger = logging.getLogger(__name__)

async def authenticate_user(username, password):
    """Authenticate user and get access token."""
    logger.info(f"Attempting to authenticate user: {username}")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{BASE_URL}/api/auth/jwt/create/", 
                data={
                    "username": username, 
                    "password": password
                }
            )
            
            logger.info(f"Auth response status: {response.status_code}")
            if response.status_code == 200:
                json_response = response.json()
                logger.info("Authentication successful")
                return json_response.get("access")
            else:
                logger.error(f"Authentication failed: {response.text}")
                return None

    except Exception as e:
        logger.error(f"Authentication error: {str(e)}")
        return None

async def refresh_token(chat_id, user_tokens):
    """Refresh the access token using the refresh token."""
    if chat_id not in user_tokens or "refresh" not in user_tokens[chat_id]:
        logger.warning(f"No refresh token found for chat_id: {chat_id}")
        return None

    refresh_token = user_tokens[chat_id]["refresh"]
    logger.info(f"Attempting to refresh token for chat_id: {chat_id}")
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{BASE_URL}/api/auth/jwt/refresh/", 
                data={"refresh": refresh_token}
            )

            logger.info(f"Refresh response status: {response.status_code}")
            if response.status_code == 200:
                new_access = response.json().get("access")
                user_tokens[chat_id]["access"] = new_access
                save_tokens(user_tokens)
                logger.info("Token refresh successful")
                return new_access
            else:
                logger.error(f"Token refresh failed: {response.text}")
                return None

    except Exception as e:
        logger.error(f"Token refresh error: {str(e)}")
        return None

async def handle_registration(update: Update, context: CallbackContext) -> int:
    """Handle the registration process step by step."""
    current_step = context.user_data.get('registration_step', 'username')
    user_input = update.message.text
    
    print(f"DEBUG: Current step: {current_step}")
    print(f"DEBUG: User input: {user_input}")
    logger.info(f"Processing registration step: {current_step}")
    
    if current_step == 'username':
        context.user_data['username'] = user_input
        print(f"DEBUG: Stored username: {user_input}")
        logger.info(f"Username stored: {user_input}")
        await update.message.reply_text("Enter your password:")
        context.user_data['registration_step'] = 'password'
        return REGISTER
    
    elif current_step == 'password':
        context.user_data['password'] = user_input
        print("DEBUG: Password stored (hidden)")
        logger.info("Password received and stored")
        await update.message.reply_text("Enter your email address (e.g., example@gmail.com):")
        context.user_data['registration_step'] = 'email'
        return REGISTER
    
    elif current_step == 'email':
        if '@' not in user_input or '.' not in user_input:
            print(f"DEBUG: Invalid email: {user_input}")
            logger.warning(f"Invalid email format: {user_input}")
            await update.message.reply_text("Please enter a valid email address (e.g., example@gmail.com):")
            return REGISTER
        
        context.user_data['email'] = user_input
        print(f"DEBUG: Stored email: {user_input}")
        logger.info(f"Email stored: {user_input}")
        await update.message.reply_text("Please select your sex (male/female):")
        context.user_data['registration_step'] = 'sex'
        return REGISTER
            
    elif current_step == 'sex':
        print(f"DEBUG: Processing sex input: {user_input}")
        if user_input.lower() not in ['male', 'female']:
            print(f"DEBUG: Invalid sex input: {user_input}")
            logger.warning(f"Invalid sex input: {user_input}")
            await update.message.reply_text("Please enter either 'male' or 'female':")
            return REGISTER
            
        print(f"DEBUG: Sex validated: {user_input}")
        logger.info(f"Sex input validated: {user_input}")
        # Make API call to register user
        try:
            print("DEBUG: Starting API registration process")
            logger.info("Initiating API registration")
            
            print("DEBUG: Creating aiohttp session")
            async with aiohttp.ClientSession() as session:
                data = {
                    'username': context.user_data['username'],
                    'password': context.user_data['password'],
                    're_password': context.user_data['password'],
                    'email': context.user_data['email'],
                    'sex': user_input.lower()
                }
                print(f"DEBUG: Registration data prepared: {data}")
                logger.info(f"Registration data prepared (username: {data['username']}, email: {data['email']}, sex: {data['sex']})")
                
                api_url = f'{BASE_URL}/api/auth/users/'
                print(f"DEBUG: Making API request to: {api_url}")
                
                async with session.post(api_url, data=data) as response:
                    response_text = await response.text()
                    print(f"DEBUG: API Response status: {response.status}")
                    print(f"DEBUG: API Response body: {response_text}")
                    logger.info(f"API response received: {response.status}")
                    
                    if response.status == 201:
                        print("DEBUG: Registration successful")
                        logger.info("Registration successful")
                        await update.message.reply_text("Registration successful!")
                        # Auto-login process
                        print("DEBUG: Starting auto-login")
                        token = await authenticate_user(context.user_data['username'], context.user_data['password'])
                        if token:
                            chat_id = str(update.message.chat_id)
                            user_tokens = load_tokens()
                            user_tokens[chat_id] = {"access": token}
                            save_tokens(user_tokens)
                            context.user_data.clear()
                            print(f"DEBUG: Auto-login successful for user: {data['username']}")
                            logger.info(f"Auto-login successful for user: {data['username']}")
                            return await show_main_menu(update, context)
                        else:
                            print("DEBUG: Auto-login failed")
                            logger.error("Auto-login failed after successful registration")
                            await update.message.reply_text("Registration successful but login failed. Please use /start to login.")
                            return ConversationHandler.END
                    else:
                        error_msg = f"Registration failed. Server response: {response_text}"
                        print(f"DEBUG: {error_msg}")
                        logger.error(error_msg)
                        await update.message.reply_text(error_msg)
                        return REGISTER
                    
        except Exception as e:
            error_msg = f"Registration error: {str(e)}"
            print(f"DEBUG: Exception occurred: {error_msg}")
            logger.error(error_msg)
            await update.message.reply_text("An error occurred during registration. Please try again.")
            return REGISTER

