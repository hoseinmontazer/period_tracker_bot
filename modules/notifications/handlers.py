"""Telegram bot handlers for notifications"""
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from constants import DASHBOARD
from utils.token_store import get_token
from .api import (
    get_unread_notifications,
    get_notifications,
    mark_notification_read,
    mark_all_notifications_read,
    clear_old_notifications,
    get_notification_preferences,
    update_notification_preferences
)
from utils.helpers import format_notification_list, format_notification_preferences

logger = logging.getLogger(__name__)


async def show_notifications(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show all notifications"""
    chat_id = update.effective_chat.id
    token = context.user_data.get("token") or get_token(chat_id)

    if not token:
        await update.message.reply_text("Please login first.")
        return DASHBOARD

    await update.message.reply_chat_action(action="typing")
    
    response = await get_notifications(token)
    
    if "error" in response:
        await update.message.reply_text(f"❌ {response['error']}")
        return DASHBOARD
    
    notifications = response.get("results", [])
    count = response.get("count", 0)
    
    if count == 0:
        await update.message.reply_text("📭 No notifications yet.")
        return DASHBOARD
    
    formatted_text = format_notification_list(notifications, count)
    
    # Add action buttons
    keyboard = [
        [InlineKeyboardButton("✅ Mark All Read", callback_data="notif_mark_all")],
        [InlineKeyboardButton("🗑️ Clear Old", callback_data="notif_clear_old")],
        [InlineKeyboardButton("⬅️ Back", callback_data="notif_back")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        formatted_text,
        parse_mode="Markdown",
        reply_markup=reply_markup
    )
    
    return DASHBOARD


async def show_unread_notifications(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show unread notifications"""
    chat_id = update.effective_chat.id
    token = context.user_data.get("token") or get_token(chat_id)

    if not token:
        await update.message.reply_text("Please login first.")
        return DASHBOARD

    await update.message.reply_chat_action(action="typing")
    
    response = await get_unread_notifications(token)
    
    if "error" in response:
        await update.message.reply_text(f"❌ {response['error']}")
        return DASHBOARD
    
    notifications = response.get("data", [])
    count = response.get("count", 0)
    
    if count == 0:
        await update.message.reply_text("✅ No unread notifications!")
        return DASHBOARD
    
    formatted_text = format_notification_list(notifications, count, unread_only=True)
    
    # Add action buttons
    keyboard = [
        [InlineKeyboardButton("✅ Mark All Read", callback_data="notif_mark_all")],
        [InlineKeyboardButton("⬅️ Back", callback_data="notif_back")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        formatted_text,
        parse_mode="Markdown",
        reply_markup=reply_markup
    )
    
    return DASHBOARD


async def show_notification_settings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show notification preferences"""
    chat_id = update.effective_chat.id
    token = context.user_data.get("token") or get_token(chat_id)

    if not token:
        await update.message.reply_text("Please login first.")
        return DASHBOARD

    await update.message.reply_chat_action(action="typing")
    
    response = await get_notification_preferences(token)
    
    if "error" in response:
        await update.message.reply_text(f"❌ {response['error']}")
        return DASHBOARD
    
    preferences = response.get("data", {})
    formatted_text = format_notification_preferences(preferences)
    
    # Add toggle buttons for common settings
    keyboard = [
        [
            InlineKeyboardButton(
                f"{'✅' if preferences.get('period_started_alert') else '❌'} Period Alerts",
                callback_data="toggle_period_alert"
            )
        ],
        [
            InlineKeyboardButton(
                f"{'✅' if preferences.get('ovulation_alert') else '❌'} Ovulation Alerts",
                callback_data="toggle_ovulation_alert"
            )
        ],
        [
            InlineKeyboardButton(
                f"{'✅' if preferences.get('partner_period_alert') else '❌'} Partner Alerts",
                callback_data="toggle_partner_alert"
            )
        ],
        [InlineKeyboardButton("⚙️ Advanced Settings", callback_data="notif_advanced")],
        [InlineKeyboardButton("⬅️ Back", callback_data="notif_back")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        formatted_text,
        parse_mode="Markdown",
        reply_markup=reply_markup
    )
    
    return DASHBOARD


async def handle_notification_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle notification-related callback queries"""
    query = update.callback_query
    await query.answer()
    
    chat_id = update.effective_chat.id
    token = context.user_data.get("token") or get_token(chat_id)
    
    if not token:
        await query.edit_message_text("Please login first.")
        return DASHBOARD
    
    action = query.data
    
    if action == "notif_mark_all":
        response = await mark_all_notifications_read(token)
        if "error" in response:
            await query.edit_message_text(f"❌ {response['error']}")
        else:
            message = response.get("message", "All notifications marked as read")
            await query.edit_message_text(f"✅ {message}")
    
    elif action == "notif_clear_old":
        response = await clear_old_notifications(token)
        if "error" in response:
            await query.edit_message_text(f"❌ {response['error']}")
        else:
            message = response.get("message", "Old notifications cleared")
            await query.edit_message_text(f"✅ {message}")
    
    elif action == "notif_back":
        from modules.users.handlers import show_dashboard
        # Simulate a message to trigger dashboard
        update.message = query.message
        return await show_dashboard(update, context)
    
    elif action.startswith("toggle_"):
        # Handle preference toggles
        await handle_preference_toggle(update, context, action)
    
    elif action == "notif_advanced":
        await query.edit_message_text(
            "⚙️ *Advanced Notification Settings*\n\n"
            "To customize advanced settings like:\n"
            "• Notification time\n"
            "• Days before period reminder\n"
            "• Specific alert types\n\n"
            "Please use the web interface or contact support.",
            parse_mode="Markdown"
        )
    
    return DASHBOARD


async def handle_preference_toggle(update: Update, context: ContextTypes.DEFAULT_TYPE, action: str):
    """Toggle notification preferences"""
    query = update.callback_query
    chat_id = update.effective_chat.id
    token = context.user_data.get("token") or get_token(chat_id)
    
    # Map actions to preference keys
    preference_map = {
        "toggle_period_alert": "period_started_alert",
        "toggle_ovulation_alert": "ovulation_alert",
        "toggle_partner_alert": "partner_period_alert"
    }
    
    pref_key = preference_map.get(action)
    if not pref_key:
        return
    
    # Get current preferences
    response = await get_notification_preferences(token)
    if "error" in response:
        await query.answer(f"❌ {response['error']}", show_alert=True)
        return
    
    preferences = response.get("data", {})
    current_value = preferences.get(pref_key, True)
    
    # Toggle the value
    new_preferences = {pref_key: not current_value}
    
    # Update preferences
    update_response = await update_notification_preferences(token, new_preferences)
    if "error" in update_response:
        await query.answer(f"❌ {update_response['error']}", show_alert=True)
        return
    
    # Show success message
    status = "enabled" if not current_value else "disabled"
    await query.answer(f"✅ Notification {status}!", show_alert=True)
    
    # Refresh the settings view
    update.message = query.message
    await show_notification_settings(update, context)
