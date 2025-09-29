import datetime
import logging
from pathlib import Path
from venv import logger
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update 
from telegram.ext import Application,ContextTypes, CommandHandler, MessageHandler, filters, ConversationHandler ,PicklePersistence, CallbackQueryHandler
from config import BOT_TOKEN
from constants import *

# Import handlers from modules
from modules.ai.feedback_handler import feedback_handler, text_feedback_handler
from modules.auth.handlers import handel_start, start_login, get_login_username, get_login_password, start_register, get_register_username, get_register_email, get_register_password, get_register_sex 
from modules.periods.delete_period import  handel_start_delete_period, start_delete_period
from modules.periods.edit_period import ask_edit_cycle, ask_edit_duration, ask_edit_end_date, ask_edit_medication, ask_edit_start_date, ask_edit_symptoms, start_edit_period
from modules.schedulers.daily_suggestion import daily_suggestion_callback
from modules.users.edit_profile import handle_cycle_length, handle_first_name, handle_last_name, handle_period_duration
from modules.users.handlers import handle_dashboard, show_dashboard, show_profile, handle_profile_view
from modules.users.partner_handler import  handel_accept_remove_code, start_partner_menu, handle_partner_menu, handle_accept_invitation, handle_remove_partner 
from modules.periods.handlers import handle_period_date, show_period_history, start_track_period, get_period_start, get_period_symptoms, get_period_medication
from modules.analysis.handlers import show_cycle_analysis
from utils.token_store import get_token



logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)






def main():
    data_dir = Path("./data")
    data_dir.mkdir(parents=True, exist_ok=True)
    # 1. Create a persistence object. This will store the state in a file named 'bot_data.pickle'
    persistence = PicklePersistence(filepath=data_dir / "bot_data.pickle")

    # 2. Pass the persistence object to the Application builder
    application = Application.builder().token(BOT_TOKEN).persistence(persistence).build()

    # 3. Add a unique name to your ConversationHandler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', show_dashboard)],
        states={
            MAIN_MENU: [MessageHandler(filters.TEXT & ~filters.COMMAND, show_dashboard)],
            START: [MessageHandler(filters.TEXT & ~filters.COMMAND, handel_start)],
            START_LOGIN: [MessageHandler(filters.TEXT & ~filters.COMMAND, start_login)],
            START_REGISTER: [MessageHandler(filters.TEXT & ~filters.COMMAND, start_register)],
            LOGIN_USERNAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_login_username)],
            LOGIN_PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_login_password)],
            REGISTER_USERNAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_register_username)],
            REGISTER_EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_register_email)],
            REGISTER_PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_register_password)],
            REGISTER_SEX: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_register_sex)],
            DASHBOARD: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_dashboard)],
            PROFILE_VIEW: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_profile_view)],
            PARTNER_MENU: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_partner_menu)],
            ACCEPT_INVITATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_accept_invitation)],
            ACCEPT_REMOVE_CODE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handel_accept_remove_code)],
            REMOVE_PARTNER : [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_remove_partner)],
            TRACK_PERIOD_START: [MessageHandler(filters.StatusUpdate.WEB_APP_DATA, handle_period_date),
                                 MessageHandler(filters.TEXT & ~filters.COMMAND, handle_period_date),
                                ],
            TRACK_PERIOD_SYMPTOMS: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_period_symptoms)],
            TRACK_PERIOD_MEDICATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_period_medication)],
            EDIT_FIRST_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_first_name)],
            EDIT_LAST_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_last_name)],
            EDIT_CYCLE_LENGTH: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_cycle_length)],
            EDIT_PERIOD_DURATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_period_duration)],
            START_DELETE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handel_start_delete_period)],
            CONFIRM_DELETE: [MessageHandler(filters.TEXT & ~filters.COMMAND, start_delete_period)],
            ASK_EDIT_PERIOD: [MessageHandler(filters.TEXT & ~filters.COMMAND, start_edit_period)],
            ASK_EDIT_START_DATE: [MessageHandler(filters.StatusUpdate.WEB_APP_DATA, ask_edit_start_date)
                                  ,MessageHandler(filters.TEXT & ~filters.COMMAND, ask_edit_start_date)
                                ],
            ASK_EDIT_END_DATE: [MessageHandler(filters.StatusUpdate.WEB_APP_DATA, ask_edit_end_date)
                                ,MessageHandler(filters.TEXT & ~filters.COMMAND, ask_edit_end_date)
                                ],
            ASK_EDIT_CYCLE: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_edit_cycle)],
            ASK_EDIT_DURATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_edit_duration)],
            ASK_EDIT_SYMPTOMS: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_edit_symptoms)],
            ASK_EDIT_MEDICATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_edit_medication)],
            FEEDBACK_TEXT: [MessageHandler(filters.TEXT & ~filters.COMMAND, text_feedback_handler)],



        },
        fallbacks=[
            CallbackQueryHandler(feedback_handler, pattern=r"^feedback:\d+:(true|false)$"),
            CommandHandler('cancel', lambda u, c: ConversationHandler.END)],
        name="my_conversation_handler",  # <--- Give it a unique name here
        persistent=True, # <--- Enable persistence for this handler
    )
    
    application.add_handler(conv_handler)

    
    # Optional: direct commands
    application.add_handler(CommandHandler('profile', show_profile))
    application.add_handler(CommandHandler('partner', start_partner_menu))
    application.add_handler(CommandHandler('history', show_period_history))
    application.add_handler(CommandHandler('track', start_track_period))
    application.add_handler(CommandHandler('analysis', show_cycle_analysis))
    # application.add_handler(CallbackQueryHandler(feedback_handler, pattern=r"^feedback:"))
    # application.add_handler(
    #     CallbackQueryHandler(feedback_handler, pattern=r"^feedback:\d+:(true|false)$")
    # )


    job_queue = application.job_queue
    if job_queue:
        # Run every day at 09:00
        job_queue.run_daily(
            daily_suggestion_callback,
            time=datetime.time(hour=9, minute=0, tzinfo=datetime.timezone.utc)  # adjust tz if needed
        )

        # Run every day at 21:00
        job_queue.run_daily(
            daily_suggestion_callback,
            time=datetime.time(hour=21, minute=0, tzinfo=datetime.timezone.utc)
        )
        job_queue.run_once(daily_suggestion_callback, when=0)
        logger.info("Scheduled jobs at 09:00 and 21:00")
    else:
        logger.warning("JobQueue not available")


    print("🤖 Period Tracker Bot is running...")
    application.run_polling()

if __name__ == '__main__':
    main()
