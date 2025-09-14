from telegram import Update
from telegram.ext import ContextTypes
from constants import DASHBOARD
from utils.token_store import get_token
from .api import cycle_analysis
from utils.helpers import format_analysis_data




async def show_cycle_analysis(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show cycle analysis"""
    chat_id = update.effective_chat.id
    token = context.user_data.get("token") or get_token(chat_id)

    if not token:
        await update.message.reply_text("Please login first.")
        return DASHBOARD

    await update.message.reply_chat_action(action="typing")
    analysis = await cycle_analysis(token)

    if analysis and analysis.get("status") == "success" and "data" in analysis:
        formatted_data = format_analysis_data(analysis)
        await update.message.reply_text(formatted_data, parse_mode="Markdown")
    else:
        await update.message.reply_text("❌ Not enough data for analysis.")

    return DASHBOARD
