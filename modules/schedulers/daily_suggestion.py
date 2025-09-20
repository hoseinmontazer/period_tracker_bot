import json
from pathlib import Path
import logging
from modules.ai.api import get_suggestion
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)
USER_TOKENS_FILE = Path("./data/user_tokens.json")

async def daily_suggestion_callback(context: ContextTypes.DEFAULT_TYPE):
    """Send daily suggestions to all users."""
    logger.info("Running daily_suggestion_callback")

    # Load tokens from JSON
    if USER_TOKENS_FILE.exists():
        with open(USER_TOKENS_FILE, "r") as f:
            tokens = json.load(f)  # dict: {chat_id: token}
    else:
        tokens = {}
        logger.warning("No user_tokens.json found!")

    # Get users from bot_data (users who used /start)
    users = context.application.bot_data.get("users", set())

    for chat_id in users:
        token = tokens.get(str(chat_id))  # chat_id in JSON keys are strings
        if not token:
            logger.warning(f"No AI token for chat_id {chat_id}, skipping")
            continue

        try:
            data = await get_suggestion(token)
        except Exception as e:
            logger.error(f"Failed to fetch suggestion for {chat_id}: {e}")
            continue

        if data:
            label = data.get("label", "")
            suggestion = data.get("suggestion", "")
            logger.info(f"Sending suggestion to {chat_id}: {label}")
            try:
                await context.bot.send_message(
                    chat_id=chat_id,
                    text=f"💡 {label}\n{suggestion}"
                )
            except Exception as e:
                logger.error(f"Failed to send message to {chat_id}: {e}")
