from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ContextTypes
from constants import DASHBOARD, MAIN_MENU, LOGIN_USERNAME, LOGIN_PASSWORD, REGISTER_USERNAME, REGISTER_EMAIL, REGISTER_PASSWORD, REGISTER_SEX, START_LOGIN, START_REGISTER
from utils.token_store import get_token, set_token
from .api import register_user, login_user
from utils.validators import validate_username, validate_email, validate_password, validate_sex
from modules.users.handlers import show_dashboard

async def handel_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle start command and login/register selection"""
    chat_id = update.effective_chat.id
    token = context.user_data.get("token") or get_token(chat_id)
    
    text = update.message.text
    print("handel_start text ---> " , text)
    
    if not token:
        if text == "Login":
            await update.message.reply_text("🔐 Please enter your username:", reply_markup=ReplyKeyboardRemove())
            return LOGIN_USERNAME
        elif text == "Register":
            await update.message.reply_text("📝 Please choose a username:", reply_markup=ReplyKeyboardRemove())
            return REGISTER_USERNAME
        else:
            # Show welcome message with login/register options
            welcome_text = "🏥 *Welcome to WellBe!*\n\n"
            welcome_text += "Your Complete Health Companion\n\n"
            welcome_text += "WellBe helps you track and manage:\n"
            welcome_text += "• 📅 Period & Cycle Tracking\n"
            welcome_text += "• 💊 Medication Management\n"
            welcome_text += "• 🏃 Fitness & Activity\n"
            welcome_text += "• 🍎 Nutrition & Meals\n"
            welcome_text += "• 😴 Sleep Monitoring\n"
            welcome_text += "• 🧘 Mental Health\n"
            welcome_text += "• 👥 Care Circle Support\n\n"
            welcome_text += "Please login or register to get started:"
            
            keyboard = [
                ["Login", "Register"]
            ]
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
            await update.message.reply_text(welcome_text, parse_mode="Markdown", reply_markup=reply_markup)
            
            from constants import START
            return START
    else:
        return await show_dashboard(update, context)


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