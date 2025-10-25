"""Notification scheduler for sending automated notifications"""
import json
import logging
from pathlib import Path
from datetime import datetime
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from .api import get_unread_notifications, mark_notification_read, get_unread_messages

logger = logging.getLogger(__name__)
USER_TOKENS_FILE = Path("./data/user_tokens.json")


# Emoji mapping for notification types
NOTIFICATION_EMOJIS = {
    "PERIOD_COMING": "🔴",
    "PERIOD_STARTED": "🩸",
    "PERIOD_LATE": "⚠️",
    "OVULATION_COMING": "🌸",
    "FERTILE_WINDOW": "💐",
    "PMS_PHASE": "😔",
    "SYMPTOM_REMINDER": "📝",
    "WELLNESS_REMINDER": "💪",
    "PARTNER_PERIOD": "💑",
    "PARTNER_PMS": "🤝"
}


async def send_notifications_callback(context: ContextTypes.DEFAULT_TYPE):
    """
    Scheduled job to check and send notifications to users.
    This runs periodically (e.g., every hour or at specific times).
    """
    logger.info("Running send_notifications_callback")

    # Load tokens from JSON
    if USER_TOKENS_FILE.exists():
        with open(USER_TOKENS_FILE, "r") as f:
            tokens = json.load(f)
    else:
        tokens = {}
        logger.warning("No user_tokens.json found!")

    # Get users from bot_data
    users = context.application.bot_data.get("users", set())

    for chat_id in users:
        token = tokens.get(str(chat_id))
        if not token:
            logger.warning(f"No token for chat_id {chat_id}, skipping")
            continue

        try:
            # Fetch unread notifications from API
            response = await get_unread_notifications(token)
            
            if "error" in response:
                logger.error(f"Error fetching notifications for {chat_id}: {response['error']}")
            else:
                notifications = response.get("data", [])
                count = response.get("count", 0)
                
                if count > 0:
                    # Send each notification
                    for notif in notifications:
                        await send_single_notification(context, chat_id, notif, token)
                else:
                    logger.info(f"No unread notifications for {chat_id}")
            
            # Also check for unread partner messages
            messages_response = await get_unread_messages(token)
            
            if "error" not in messages_response:
                messages = messages_response.get("messages", [])
                msg_count = messages_response.get("count", 0)
                
                if msg_count > 0:
                    # Send notification about unread messages
                    await send_message_notification(context, chat_id, msg_count, messages[0])
                    
        except Exception as e:
            logger.error(f"Failed to process notifications for {chat_id}: {e}")


async def send_single_notification(context: ContextTypes.DEFAULT_TYPE, chat_id: int, notification: dict, token: str):
    """Send a single notification to a user"""
    try:
        notif_type = notification.get("notification_type", "")
        title = notification.get("title", "Notification")
        message = notification.get("message", "")
        notif_id = notification.get("id")
        scheduled_time = notification.get("scheduled_time", "")
        
        # Get appropriate emoji
        emoji = NOTIFICATION_EMOJIS.get(notif_type, "🔔")
        
        # Format the notification message
        text = f"{emoji} *{title}*\n\n{message}"
        
        if scheduled_time:
            try:
                dt = datetime.fromisoformat(scheduled_time.replace('Z', '+00:00'))
                time_str = dt.strftime("%B %d, %Y at %I:%M %p")
                text += f"\n\n📅 Scheduled: {time_str}"
            except:
                pass
        
        # Create action buttons
        keyboard = [
            [
                InlineKeyboardButton("✅ Mark as Read", callback_data=f"notif_read:{notif_id}"),
                InlineKeyboardButton("📋 View All", callback_data="notif_view_all")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        # Send the notification
        await context.bot.send_message(
            chat_id=chat_id,
            text=text,
            parse_mode="Markdown",
            reply_markup=reply_markup
        )
        
        logger.info(f"Sent notification {notif_id} to {chat_id}")
        
    except Exception as e:
        logger.error(f"Failed to send notification {notification.get('id')} to {chat_id}: {e}")


async def check_and_send_immediate_notifications(context: ContextTypes.DEFAULT_TYPE, chat_id: int, token: str):
    """
    Check for immediate notifications after user actions (e.g., after logging a period).
    This can be called from handlers when needed.
    """
    try:
        response = await get_unread_notifications(token)
        
        if "error" in response:
            logger.error(f"Error fetching notifications: {response['error']}")
            return
        
        notifications = response.get("data", [])
        count = response.get("count", 0)
        
        if count == 0:
            return
        
        # Send only the most recent notification
        if notifications:
            latest_notif = notifications[0]
            await send_single_notification(context, chat_id, latest_notif, token)
            
    except Exception as e:
        logger.error(f"Failed to check immediate notifications: {e}")



async def send_message_notification(context: ContextTypes.DEFAULT_TYPE, chat_id: int, count: int, latest_message: dict):
    """Send notification about unread partner messages"""
    try:
        sender_name = latest_message.get("sender_name", "Your partner")
        message_preview = latest_message.get("message", "")[:50]
        
        if len(latest_message.get("message", "")) > 50:
            message_preview += "..."
        
        text = f"💬 *New Message from {sender_name}*\n\n"
        text += f"{message_preview}\n\n"
        
        if count > 1:
            text += f"_You have {count} unread messages_"
        
        # Create action buttons
        keyboard = [
            [
                InlineKeyboardButton("💬 View Messages", callback_data="view_messages"),
                InlineKeyboardButton("✉️ Reply", callback_data="reply_message")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        # Send the notification
        await context.bot.send_message(
            chat_id=chat_id,
            text=text,
            parse_mode="Markdown",
            reply_markup=reply_markup
        )
        
        logger.info(f"Sent message notification to {chat_id}")
        
    except Exception as e:
        logger.error(f"Failed to send message notification to {chat_id}: {e}")
