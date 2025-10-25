"""WellBe Health Dashboard - Main health interface"""
import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from constants import DASHBOARD, HEALTH_DASHBOARD, HEALTH_MODULES, START
from utils.token_store import get_token

logger = logging.getLogger(__name__)


async def show_health_dashboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show main WellBe health dashboard"""
    chat_id = update.effective_chat.id
    token = context.user_data.get("token") or get_token(chat_id)
    
    if not token:
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
    
    # Store chat_id in bot_data for notifications
    users = context.application.bot_data.setdefault("users", set())
    if chat_id not in users:
        users.add(chat_id)
        logger.info(f"Added chat_id {chat_id} to bot_data['users']")
    
    user = update.effective_user
    username = user.username or user.first_name or "User"
    
    # Get health summary (we'll enhance this later with actual data)
    health_summary = await get_health_summary(token)
    
    # Create welcome message
    welcome_text = f"🏥 *WellBe - Your Health Companion*\n\n"
    welcome_text += f"Welcome back, {username}!\n\n"
    welcome_text += "📊 *Today's Health Summary:*\n"
    welcome_text += health_summary
    
    # Main dashboard keyboard
    keyboard = [
        ["🩺 Health Modules", "📊 Health Analytics"],
        ["📅 Period Tracker", "💊 Medications"],
        ["👥 Care Circle", "🔔 Notifications"],
        ["⚙️ Settings", "ℹ️ About WellBe"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(
        welcome_text,
        parse_mode="Markdown",
        reply_markup=reply_markup
    )
    
    return HEALTH_DASHBOARD


async def show_health_modules(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show available health modules"""
    chat_id = update.effective_chat.id
    token = context.user_data.get("token") or get_token(chat_id)
    
    if not token:
        await update.message.reply_text("Please login first.")
        return DASHBOARD
    
    message_text = "🩺 *Health Modules*\n\n"
    message_text += "Choose a health module to manage:\n\n"
    message_text += "📅 *Period Tracker* - Track your menstrual cycle\n"
    message_text += "💊 *Medications* - Manage your medications\n"
    message_text += "🏃 *Fitness* - Track your activities (Coming Soon)\n"
    message_text += "🍎 *Nutrition* - Log your meals (Coming Soon)\n"
    message_text += "😴 *Sleep* - Monitor your sleep (Coming Soon)\n"
    message_text += "🧘 *Mental Health* - Track your mood (Coming Soon)\n"
    message_text += "🩸 *Vital Signs* - Monitor vitals (Coming Soon)\n"
    
    keyboard = [
        ["📅 Period Tracker", "💊 Medications"],
        ["🏃 Fitness", "🍎 Nutrition"],
        ["😴 Sleep", "🧘 Mental Health"],
        ["🩸 Vital Signs"],
        ["⬅️ Back to Dashboard"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(
        message_text,
        parse_mode="Markdown",
        reply_markup=reply_markup
    )
    
    return HEALTH_MODULES


async def show_about_wellbe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show information about WellBe"""
    message_text = "ℹ️ *About WellBe*\n\n"
    message_text += "🏥 *WellBe* is your complete health companion, helping you track and manage various aspects of your health in one place.\n\n"
    message_text += "*Features:*\n"
    message_text += "• 📅 Period Tracking & Predictions\n"
    message_text += "• 💊 Medication Management\n"
    message_text += "• 🏃 Fitness & Activity Tracking\n"
    message_text += "• 🍎 Nutrition & Meal Logging\n"
    message_text += "• 😴 Sleep Monitoring\n"
    message_text += "• 🧘 Mental Health & Mood Tracking\n"
    message_text += "• 🩸 Vital Signs Monitoring\n"
    message_text += "• 👥 Care Circle for Family Support\n"
    message_text += "• 🔔 Smart Health Notifications\n"
    message_text += "• 📊 Comprehensive Health Analytics\n\n"
    message_text += "*Version:* 2.0\n"
    message_text += "*Your health, simplified.* 💙"
    
    await update.message.reply_text(
        message_text,
        parse_mode="Markdown"
    )
    
    return HEALTH_DASHBOARD


async def get_health_summary(token: str) -> str:
    """Get user's health summary for dashboard"""
    # TODO: Fetch actual data from APIs
    # For now, return a placeholder
    summary = "• Period Tracker: Active\n"
    summary += "• Medications: No pending reminders\n"
    summary += "• Overall Health: Good 💚\n"
    
    return summary


async def handle_health_dashboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle health dashboard menu actions"""
    text = update.message.text
    
    if text == "🩺 Health Modules":
        return await show_health_modules(update, context)
    
    elif text == "📊 Health Analytics":
        from modules.analysis.handlers import show_cycle_analysis
        return await show_cycle_analysis(update, context)
    
    elif text == "📅 Period Tracker":
        from modules.periods.handlers import handler_period_menu
        return await handler_period_menu(update, context)
    
    elif text == "💊 Medications":
        await update.message.reply_text(
            "💊 *Medication Tracker*\n\n"
            "Coming soon! You'll be able to:\n"
            "• Add medications\n"
            "• Set reminders\n"
            "• Track adherence\n"
            "• Get refill alerts",
            parse_mode="Markdown"
        )
        return HEALTH_DASHBOARD
    
    elif text == "👥 Care Circle":
        from modules.users.partner_handler import start_partner_menu
        return await start_partner_menu(update, context)
    
    elif text == "🔔 Notifications":
        from modules.notifications.handlers import show_unread_notifications
        return await show_unread_notifications(update, context)
    
    elif text == "⚙️ Settings":
        from modules.users.handlers import handle_setting
        return await handle_setting(update, context)
    
    elif text == "ℹ️ About WellBe":
        return await show_about_wellbe(update, context)
    
    elif text == "⬅️ Back to Dashboard":
        return await show_health_dashboard(update, context)
    
    # Handle health module selections
    elif text in ["🏃 Fitness", "🍎 Nutrition", "😴 Sleep", "🧘 Mental Health", "🩸 Vital Signs"]:
        module_name = text.split()[1] if len(text.split()) > 1 else text
        await update.message.reply_text(
            f"{text} *Module*\n\n"
            f"Coming soon! This module is under development.\n\n"
            f"Stay tuned for updates! 🚀",
            parse_mode="Markdown"
        )
        return HEALTH_MODULES
    
    await update.message.reply_text("Please use the menu options.")
    return HEALTH_DASHBOARD
