from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ContextTypes
from constants import MAIN_MENU, LOGIN_USERNAME, LOGIN_PASSWORD, REGISTER_USERNAME, REGISTER_EMAIL, REGISTER_PASSWORD, REGISTER_SEX, START_LOGIN, START_REGISTER
from utils.token_store import set_token
from .api import register_user, login_user
from utils.validators import validate_username, validate_email, validate_password, validate_sex
from modules.users.handlers import show_dashboard

async def handel_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "Login":
        return START_LOGIN
    elif text == "Register":
        return START_REGISTER




async def start_login(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start login process"""
    await update.message.reply_text("🔐 Please enter your username:", reply_markup=ReplyKeyboardRemove())
    return LOGIN_USERNAME

async def get_login_username(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get username for login"""
    username = update.message.text.strip()
    
    if not validate_username(username):
        await update.message.reply_text("Invalid username. Please try again.")
        return LOGIN_USERNAME
    
    context.user_data["username"] = username
    await update.message.reply_text("Now please enter your password:")
    return LOGIN_PASSWORD

async def get_login_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get password and login"""
    password = update.message.text
    username = context.user_data.get("username")
    chat_id = update.effective_chat.id
    
    await update.message.reply_chat_action(action="typing")
    result = await login_user(username, password)
    
    if "access" in result:
        token = result["access"]
        context.user_data["token"] = token
        set_token(chat_id, token)

        await update.message.reply_text("✅ Login successful!")
        return await show_dashboard(update, context)
    else:
        error_msg = result.get("detail", "Login failed")
        await update.message.reply_text(f"❌ {error_msg}")
        return MAIN_MENU

async def start_register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start registration process"""
    await update.message.reply_text("📝 Please choose a username:", reply_markup=ReplyKeyboardRemove())
    return REGISTER_USERNAME

async def get_register_username(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get username for registration"""
    username = update.message.text.strip()
    
    if not validate_username(username):
        await update.message.reply_text("Invalid username. Please try again.")
        return REGISTER_USERNAME
    
    context.user_data["username"] = username
    await update.message.reply_text("Now please enter your email:")
    return REGISTER_EMAIL

async def get_register_email(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get email for registration"""
    email = update.message.text.strip()
    
    if not validate_email(email):
        await update.message.reply_text("Invalid email. Please try again.")
        return REGISTER_EMAIL
    
    context.user_data["email"] = email
    await update.message.reply_text("Now please choose a password:")
    return REGISTER_PASSWORD

async def get_register_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get password for registration"""
    password = update.message.text.strip()
    
    if not validate_password(password):
        await update.message.reply_text("Password doesn't meet requirements. Please try again.")
        return REGISTER_PASSWORD
    
    context.user_data["password"] = password
    
    keyboard = [["Male", "Female", "Other"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("Please select your sex:", reply_markup=reply_markup)
    return REGISTER_SEX

async def get_register_sex(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get sex and complete registration"""
    sex = update.message.text.strip().lower()
    
    if not validate_sex(sex):
        keyboard = [["Male", "Female", "Other"]]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text("Please select a valid option:", reply_markup=reply_markup)
        return REGISTER_SEX
    
    username = context.user_data.get("username")
    email = context.user_data.get("email")
    password = context.user_data.get("password")
    
    await update.message.reply_chat_action(action="typing")
    result = await register_user(username, password, email, sex)
    
    if "id" in result:
        await update.message.reply_text("✅ Registration successful! You can now login.")
        return MAIN_MENU
    else:
        error_msg = result.get("detail", "Registration failed")
        await update.message.reply_text(f"❌ {error_msg}")
        return MAIN_MENU