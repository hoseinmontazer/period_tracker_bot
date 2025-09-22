from telegram import ReplyKeyboardMarkup


def back_skip_keyboard():
    return ReplyKeyboardMarkup(
        [["⬅️ Back to Dashboard", "Skip"]],
        resize_keyboard=True
    )
