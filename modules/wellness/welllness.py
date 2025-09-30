from telegram.ext import ConversationHandler, ContextTypes
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from utils.token_store import get_token
from modules.wellness.api import send_wellness
from constants import (
    WELLNESS_STRESS, WELLNESS_SLEEP, WELLNESS_MOOD, WELLNESS_ENERGY,
    WELLNESS_PAIN, WELLNESS_EXERCISE, WELLNESS_NUTRITION, WELLNESS_CAFFEINE,
    WELLNESS_ALCOHOL, WELLNESS_SMOKING, WELLNESS_ANXIETY, WELLNESS_FOCUS,
    WELLNESS_NOTES, WELLNESS_CONFIRM, DASHBOARD
)

# ----------------- Keyboard Helpers -----------------
def generate_level_keyboard(max_level, include_zero=True, step=1, prefix=""):
    options = []
    if include_zero:
        options.append(0)
    options.extend([i * step for i in range(1, int(max_level / step) + 1)])
    buttons = [InlineKeyboardButton(str(i), callback_data=f"{prefix}{i}") for i in options]
    rows = [buttons[i:i+6] for i in range(0, len(buttons), 6)]
    return InlineKeyboardMarkup(rows)

def generate_sleep_keyboard():
    buttons = [InlineKeyboardButton(str(h), callback_data=f"sl_{h}") for h in range(13)]
    rows = [buttons[i:i+6] for i in range(0, len(buttons), 6)]
    return InlineKeyboardMarkup(rows)


# ----------------- Conversation Flow -----------------
async def start_wellness(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["wellness_data"] = {}
    await update.message.reply_text(
        "👋 Let’s start your daily wellness check.\n\n😬 What is your **Stress Level** today? (0 = Low, 5 = High)",
        reply_markup=generate_level_keyboard(5, prefix="st_")
    )
    return WELLNESS_STRESS


async def get_stress(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data["wellness_data"]["stress_level"] = int(query.data.replace("st_", ""))

    await query.message.reply_text(
        f"✅ Stress Level saved: {context.user_data['wellness_data']['stress_level']}\n\n😴 How many **hours did you sleep** last night?",
        reply_markup=generate_sleep_keyboard()
    )
    return WELLNESS_SLEEP


async def get_sleep(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data["wellness_data"]["sleep_hours"] = int(query.data.replace("sl_", ""))

    await query.message.reply_text(
        f"✅ Sleep saved: {context.user_data['wellness_data']['sleep_hours']}h\n\n😊 What is your **Mood Level** today? (0 = Low, 5 = High)",
        reply_markup=generate_level_keyboard(5, prefix="md_")
    )
    return WELLNESS_MOOD


async def get_mood(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data["wellness_data"]["mood_level"] = int(query.data.replace("md_", ""))

    await query.message.reply_text(
        "⚡ What is your **Energy Level**? (0 = Exhausted, 10 = Maximum)",
        reply_markup=generate_level_keyboard(10, prefix="en_")
    )
    return WELLNESS_ENERGY


async def get_energy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data["wellness_data"]["energy_level"] = int(query.data.replace("en_", ""))

    await query.message.reply_text(
        "🤕 What is your **Pain Level**? (0 = None, 5 = Severe)",
        reply_markup=generate_level_keyboard(5, prefix="pa_")
    )
    return WELLNESS_PAIN


async def get_pain(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data["wellness_data"]["pain_level"] = int(query.data.replace("pa_", ""))

    await query.message.reply_text(
        "🏃 How many **Exercise Minutes** today? (0,15,30,45,60,90+)",
        reply_markup=generate_level_keyboard(90, step=15, prefix="ex_")
    )
    return WELLNESS_EXERCISE


async def get_exercise(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data["wellness_data"]["exercise_minutes"] = int(query.data.replace("ex_", ""))

    await query.message.reply_text(
        "🥗 How was your **Nutrition Quality**? (1 = Poor, 5 = Excellent)",
        reply_markup=generate_level_keyboard(5, include_zero=False, prefix="nu_")
    )
    return WELLNESS_NUTRITION


async def get_nutrition(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data["wellness_data"]["nutrition_quality"] = int(query.data.replace("nu_", ""))

    await query.message.reply_text(
        "☕ How many **Caffeine** servings today? (0-5)",
        reply_markup=generate_level_keyboard(5, prefix="ca_")
    )
    return WELLNESS_CAFFEINE


async def get_caffeine(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data["wellness_data"]["caffeine_intake"] = int(query.data.replace("ca_", ""))

    await query.message.reply_text(
        "🍷 How many **Alcohol** servings today? (0-5)",
        reply_markup=generate_level_keyboard(5, prefix="al_")
    )
    return WELLNESS_ALCOHOL


async def get_alcohol(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data["wellness_data"]["alcohol_intake"] = int(query.data.replace("al_", ""))

    await query.message.reply_text(
        "🚬 Rate your **Smoking/Exposure** (0 = None, 5 = Heavy)",
        reply_markup=generate_level_keyboard(5, prefix="sm_")
    )
    return WELLNESS_SMOKING


async def get_smoking(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data["wellness_data"]["smoking"] = int(query.data.replace("sm_", ""))

    await query.message.reply_text(
        "😟 What is your **Anxiety Level**? (0 = None, 5 = Severe)",
        reply_markup=generate_level_keyboard(5, prefix="an_")
    )
    return WELLNESS_ANXIETY


async def get_anxiety(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data["wellness_data"]["anxiety_level"] = int(query.data.replace("an_", ""))

    await query.message.reply_text(
        "🎯 What is your **Focus Level**? (0 = Distracted, 5 = Highly Focused)",
        reply_markup=generate_level_keyboard(5, prefix="fo_")
    )
    return WELLNESS_FOCUS


async def get_focus(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data["wellness_data"]["focus_level"] = int(query.data.replace("fo_", ""))

    await query.message.reply_text(
        "📝 Final step: Do you have any **Notes**? (Type text, or 'None' to skip)"
    )
    return WELLNESS_NOTES


async def get_notes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text.strip().lower() != "none":
        context.user_data["wellness_data"]["notes"] = text

    data = context.user_data["wellness_data"]
    summary = "\n".join([f"- {k.replace('_',' ').title()}: {v}" for k,v in data.items()])

    keyboard = [[
        InlineKeyboardButton("✅ Submit", callback_data="submit"),
        InlineKeyboardButton("❌ Cancel", callback_data="cancel"),
    ]]
    await update.message.reply_text(
        f"📋 Review your data:\n{summary}\n\nSubmit or Cancel?",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    return WELLNESS_CONFIRM


async def confirm_submission(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "submit":
        chat_id = update.effective_chat.id
        token = context.user_data.get("token") or get_token(chat_id)

        if not token:
            await query.message.reply_text("❌ Error: No token found. Please log in again.")
            return ConversationHandler.END

        response = await send_wellness(token, **context.user_data["wellness_data"])

        if response.get("error"):
            await query.message.reply_text(f"❌ Submission failed: {response['error']}")
        else:
            await query.message.reply_text("✅ Wellness data submitted successfully!")
    else:
        await query.message.reply_text("🚫 Submission cancelled.")

    context.user_data.pop("wellness_data", None)
    return DASHBOARD
