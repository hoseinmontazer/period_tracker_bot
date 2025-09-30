import logging
from pathlib import Path
from telegram.ext import ContextTypes
# Need to ensure these imports are present in the actual file:
from telegram import InlineKeyboardButton, InlineKeyboardMarkup 
from constants import WELLNESS_STRESS 

logger = logging.getLogger(__name__)
USER_TOKENS_FILE = Path("./data/user_tokens.json")

# --- Helper Function (Modified) ---
def generate_level_keyboard(max_level, include_zero=True, step=1):
    """Generates an Inline Keyboard for level selection (e.g., 0-5)."""
    
    options = []
    if include_zero:
        options.append(0)
    # Generate the list of numeric options (1 to max_level)
    options.extend([i * step for i in range(1, int(max_level / step) + 1)])
    
    # 1. Create a FLAT list of InlineKeyboardButtons
    flat_buttons = [InlineKeyboardButton(str(i), callback_data=str(i)) for i in options]
    
    # 2. Chunk the flat list into rows of 6
    rows = [flat_buttons[i:i + 6] for i in range(0, len(flat_buttons), 6)]
    
    # 3. Return the InlineKeyboardMarkup with the correct list of lists of buttons
    return InlineKeyboardMarkup(rows)

async def wellness_checkin_callback(context: ContextTypes.DEFAULT_TYPE):
    """Send the initial wellness check-in message to all users."""
    logger.info("Running wellness_checkin_callback")

    # This part should be safe now
    users = context.application.bot_data.get("users", set())

    # Initial Stress Level Keyboard (0-5)
    reply_markup = generate_level_keyboard(max_level=5)
    
    initial_text = "👋 Time for your daily wellness check-in.\nWhat is your **Stress Level** today? (0 = Low, 5 = High)"

    for chat_id in users:
        try:
            # Send the message
            sent_message = await context.bot.send_message(
                chat_id=chat_id,
                text=initial_text,
                reply_markup=reply_markup
            )
            # Set the user's state to WELLNESS_STRESS for the conversation to start
            context.application.user_data.setdefault(chat_id, {})['state'] = WELLNESS_STRESS
            logger.info(f"Sent wellness check-in to {chat_id} and set state.")
        except Exception as e:
            logger.error(f"Failed to send wellness check-in to {chat_id}: {e}")