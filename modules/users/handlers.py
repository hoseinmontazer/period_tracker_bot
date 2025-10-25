from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ContextTypes
from constants import DASHBOARD, LOGIN_USERNAME, MAIN_MENU, PROFILE_VIEW, PARTNER_MENU, ACCEPT_INVITATION, REMOVE_PARTNER, SETTINGS, START
from modules.users.partner_handler import start_partner_menu
from utils.helpers import format_profile_data
from utils.token_store import get_token
from .api import get_profile

async def show_dashboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show user dashboard"""
    # token = context.user_data.get("token")
    # username = context.user_data.get("username", "User")
    print("show_dashboard")
    chat_id = update.effective_chat.id
    token = context.user_data.get("token") or get_token(chat_id)
    
    if not token:
        print("token not aviable")
        keyboard = [
            ["Login", "Register"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
        await update.message.reply_text("🔐 Please login or register first:", reply_markup=reply_markup)
        return START 
    else:

        # Store chat_id in bot_data for daily suggestions
        users = context.application.bot_data.setdefault("users", set())
        if chat_id not in users:
            users.add(chat_id)
            print(f"Added chat_id {chat_id} to bot_data['users']")

        user = update.effective_user
        username = user.username  

        keyboard = [
            ["📅 Track Period", "📊 Cycle Analysis"],
            ["🔔 Notifications", "👥 Partner"],
            ["⚙️ Setting", "📋 Period History"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        
        await update.message.reply_text(
            f"🏠 Welcome back, {username}!",
            reply_markup=reply_markup
        )
        return DASHBOARD

async def handle_dashboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle dashboard actions"""
    text = update.message.text
    print("text ---> " , text)
    if text == "👤 My Profile":
        return await show_profile(update, context)
    elif text == "⚙️ Setting":
        return await handle_setting(update, context)
    elif text == "👥 Partner":
        return await start_partner_menu(update, context)
    elif text == "📅 Track Period":
        from modules.periods.handlers import handler_period_menu
        return await handler_period_menu(update, context)
    elif text == "➕ Add Period":
        from modules.periods.handlers import start_track_period
        return await start_track_period(update, context)
    elif text == "✍️ Edit Period":
        from modules.periods.edit_period import handel_start_edit_period 
        return await handel_start_edit_period(update, context)
    elif text == "🚪 Logout":
        from modules.users.logout import handle_logout_profile
        return await handle_logout_profile(update, context) 

    elif text == "🗑️ Delete Period":
        from modules.periods.delete_period import handel_start_delete_period
        return await handel_start_delete_period(update, context)
    elif text == "📊 Cycle Analysis":
        from modules.analysis.handlers import show_cycle_analysis
        return await show_cycle_analysis(update, context)
    elif text == "📋 Period History":
        from modules.periods.handlers import show_period_history
        return await show_period_history(update, context)
    elif text == "✍️ Edit Profile":
        from modules.users.edit_profile import handle_edit_profile
        return await handle_edit_profile(update, context)
    elif text == "🔔 Notifications":
        from modules.notifications.handlers import show_unread_notifications
        return await show_unread_notifications(update, context)
    elif text == "🔔 Notification Settings":
        from modules.notifications.handlers import show_notification_settings
        return await show_notification_settings(update, context)
    elif text == "💬 Partner Messages" or "View Conversation" in text or text == "✉️ Send Message" or text == "📋 All Messages" or text == "🔄 Refresh":
        from modules.notifications.messaging_handlers import handle_partner_message_menu
        return await handle_partner_message_menu(update, context)
    elif text == "⬅️ Back to Dashboard":
        from modules.users.handlers import show_dashboard
        return await show_dashboard(update, context)
    await update.message.reply_text("Please use the menu options.")
    return MAIN_MENU

async def show_profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show user profile"""
    chat_id = update.effective_chat.id
    token = context.user_data.get("token") or get_token(chat_id)
    
    if not token:
        await update.message.reply_text("Please login first.")
        return DASHBOARD
    
    await update.message.reply_chat_action(action="typing")
    profile_data = await get_profile(token)
    print("profile_data --- >",profile_data)
    if "detail" in profile_data:
        await update.message.reply_text("❌ Error loading profile.")
    else:
        formatted_profile = format_profile_data(profile_data)
        await update.message.reply_text(formatted_profile, parse_mode='Markdown')
    
    keyboard = [["⬅️ Back to Dashboard"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("Your profile ", reply_markup=reply_markup)
    return PROFILE_VIEW

async def handle_profile_view(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle profile view actions"""
    text = update.message.text
    
    if text == "⬅️ Back to Dashboard":
        return await show_dashboard(update, context)
    
    await update.message.reply_text("Please use the menu options.")
    return DASHBOARD

async def handle_setting(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show setting menu"""
    print("text ---> ")
    chat_id = update.effective_chat.id
    token = context.user_data.get("token") or get_token(chat_id)

    if not token:
        await update.message.reply_text("Please login first.")
        return DASHBOARD
        
    keyboard = [
        ["✍️ Edit Profile","👤 My Profile"],
        ["🔔 Notification Settings"],
        ["🚪 Logout"], 
        ["⬅️ Back to Dashboard"]
    ]

    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text("⚙️ Settings:", reply_markup=reply_markup)
    return DASHBOARD 