"""Telegram bot handlers for partner messaging"""
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from constants import DASHBOARD, PARTNER_MESSAGE_INPUT
from utils.token_store import get_token
from .api import (
    send_partner_message,
    get_conversation_with_partner,
    get_unread_messages,
    get_all_messages
)
from utils.helpers import format_message_list, format_conversation

logger = logging.getLogger(__name__)


async def show_partner_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show partner messages menu"""
    chat_id = update.effective_chat.id
    token = context.user_data.get("token") or get_token(chat_id)

    if not token:
        await update.message.reply_text("Please login first.")
        return DASHBOARD

    await update.message.reply_chat_action(action="typing")
    
    # Get unread messages count
    unread_response = await get_unread_messages(token)
    unread_count = 0
    if "error" not in unread_response:
        unread_count = unread_response.get("count", 0)
    
    # Create menu
    keyboard = [
        [f"💬 View Conversation ({unread_count} unread)" if unread_count > 0 else "💬 View Conversation"],
        ["✉️ Send Message"],
        ["📋 All Messages"],
        ["⬅️ Back to Dashboard"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    message_text = "💬 *Partner Messages*\n\n"
    if unread_count > 0:
        message_text += f"You have {unread_count} unread message(s)!\n\n"
    message_text += "Choose an option:"
    
    await update.message.reply_text(
        message_text,
        parse_mode="Markdown",
        reply_markup=reply_markup
    )
    
    return DASHBOARD


async def show_conversation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show conversation with partner"""
    chat_id = update.effective_chat.id
    token = context.user_data.get("token") or get_token(chat_id)

    if not token:
        await update.message.reply_text("Please login first.")
        return DASHBOARD

    await update.message.reply_chat_action(action="typing")
    
    # Get partner info from user profile
    from modules.users.api import get_profile
    profile = await get_profile(token)
    
    if "error" in profile or "detail" in profile:
        await update.message.reply_text("❌ Failed to load profile. Please try again.")
        return DASHBOARD
    
    partners = profile.get("partners", [])
    if not partners:
        await update.message.reply_text("❌ You don't have any partners linked yet.")
        return DASHBOARD
    
    # Get first partner (assuming one partner for now)
    partner = partners[0]
    # API returns 'partner_user_id' not 'id'
    partner_id = partner.get("partner_user_id") or partner.get("id")
    partner_name = partner.get("username", "Partner")
    
    if not partner_id:
        await update.message.reply_text("❌ Partner ID not found. Please try again.")
        return DASHBOARD
    
    # Get conversation
    response = await get_conversation_with_partner(token, partner_id)
    
    if "error" in response:
        await update.message.reply_text(f"❌ {response['error']}")
        return DASHBOARD
    
    messages = response.get("messages", [])
    count = response.get("count", 0)
    
    if count == 0:
        await update.message.reply_text(
            f"💬 *Conversation with {partner_name}*\n\n"
            "No messages yet. Start the conversation!",
            parse_mode="Markdown"
        )
    else:
        formatted_text = format_conversation(messages, partner_name, count)
        await update.message.reply_text(
            formatted_text,
            parse_mode="Markdown"
        )
    
    # Show action buttons
    keyboard = [
        ["✉️ Send Message"],
        ["🔄 Refresh"],
        ["⬅️ Back"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "What would you like to do?",
        reply_markup=reply_markup
    )
    
    return DASHBOARD


async def start_send_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start sending a message to partner"""
    chat_id = update.effective_chat.id
    token = context.user_data.get("token") or get_token(chat_id)

    if not token:
        await update.message.reply_text("Please login first.")
        return DASHBOARD

    # Get partner info
    from modules.users.api import get_profile
    profile = await get_profile(token)
    
    if "error" in profile or "detail" in profile:
        await update.message.reply_text("❌ Failed to load profile.")
        return DASHBOARD
    
    partners = profile.get("partners", [])
    if not partners:
        await update.message.reply_text("❌ You don't have any partners linked yet.")
        return DASHBOARD
    
    partner = partners[0]
    partner_name = partner.get("username", "Partner")
    # API returns 'partner_user_id' not 'id'
    partner_id = partner.get("partner_user_id") or partner.get("id")
    
    if not partner_id:
        await update.message.reply_text("❌ Partner ID not found. Please link a partner first.")
        return DASHBOARD
    
    # Store partner info in context
    context.user_data["message_partner_id"] = partner_id
    context.user_data["message_partner_name"] = partner_name
    
    keyboard = [["❌ Cancel"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(
        f"✉️ *Send Message to {partner_name}*\n\n"
        "Type your message below:",
        parse_mode="Markdown",
        reply_markup=reply_markup
    )
    
    return PARTNER_MESSAGE_INPUT


async def handle_message_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle message input from user"""
    text = update.message.text
    
    if text == "❌ Cancel":
        await update.message.reply_text("Message cancelled.")
        from modules.users.handlers import show_dashboard
        return await show_dashboard(update, context)
    
    chat_id = update.effective_chat.id
    token = context.user_data.get("token") or get_token(chat_id)
    
    partner_id = context.user_data.get("message_partner_id")
    partner_name = context.user_data.get("message_partner_name", "Partner")
    
    if not partner_id:
        await update.message.reply_text("❌ Partner information not found.")
        from modules.users.handlers import show_dashboard
        return await show_dashboard(update, context)
    
    await update.message.reply_chat_action(action="typing")
    
    # Send message
    response = await send_partner_message(token, partner_id, text)
    
    if "error" in response:
        await update.message.reply_text(f"❌ {response['error']}")
    else:
        await update.message.reply_text(
            f"✅ Message sent to {partner_name}!\n\n"
            f"💬 Your message: {text}"
        )
    
    # Clear context
    context.user_data.pop("message_partner_id", None)
    context.user_data.pop("message_partner_name", None)
    
    # Return to dashboard
    from modules.users.handlers import show_dashboard
    return await show_dashboard(update, context)


async def show_all_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show all messages (sent and received)"""
    chat_id = update.effective_chat.id
    token = context.user_data.get("token") or get_token(chat_id)

    if not token:
        await update.message.reply_text("Please login first.")
        return DASHBOARD

    await update.message.reply_chat_action(action="typing")
    
    response = await get_all_messages(token)
    
    if "error" in response:
        await update.message.reply_text(f"❌ {response['error']}")
        return DASHBOARD
    
    messages = response if isinstance(response, list) else []
    
    if not messages:
        await update.message.reply_text("📭 No messages yet.")
        return DASHBOARD
    
    formatted_text = format_message_list(messages)
    await update.message.reply_text(
        formatted_text,
        parse_mode="Markdown"
    )
    
    return DASHBOARD


async def handle_partner_message_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle partner message menu actions"""
    text = update.message.text
    
    if "View Conversation" in text:
        return await show_conversation(update, context)
    elif text == "✉️ Send Message":
        return await start_send_message(update, context)
    elif text == "📋 All Messages":
        return await show_all_messages(update, context)
    elif text == "🔄 Refresh":
        return await show_conversation(update, context)
    elif text == "⬅️ Back" or text == "⬅️ Back to Dashboard":
        from modules.users.handlers import show_dashboard
        return await show_dashboard(update, context)
    
    return DASHBOARD
