import logging
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import Application,ContextTypes, CommandHandler, MessageHandler, filters, ConversationHandler
from config import BOT_TOKEN
from constants import *

# Import handlers from modules
from modules.auth.handlers import start_login, get_login_username, get_login_password, start_register, get_register_username, get_register_email, get_register_password, get_register_sex 
from modules.users.handlers import handle_dashboard, show_dashboard, show_profile, handle_profile_view
from modules.users.partner_handler import  start_partner_menu, handle_partner_menu, handle_accept_invitation, handle_remove_partner 
from modules.periods.handlers import handle_period_date, show_period_history, start_track_period, get_period_start, get_period_symptoms, get_period_medication
from modules.analysis.handlers import show_cycle_analysis
from utils.token_store import get_token

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)





def main():
    application = Application.builder().token(BOT_TOKEN).build()



    
    # application.add_handler(CommandHandler('testweb', test_webapp))
    # application.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, handle_webapp_data))

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', show_dashboard)],
        states={
            MAIN_MENU: [MessageHandler(filters.TEXT & ~filters.COMMAND, show_dashboard)],
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
            REMOVE_PARTNER: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_remove_partner)],
            TRACK_PERIOD_START: [MessageHandler(filters.StatusUpdate.WEB_APP_DATA, handle_period_date)],  # ← FIXED
            TRACK_PERIOD_SYMPTOMS: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_period_symptoms)],
            TRACK_PERIOD_MEDICATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_period_medication)],
        },
        fallbacks=[CommandHandler('cancel', lambda u, c: ConversationHandler.END)]
    )
    
    application.add_handler(conv_handler)
    
    # Optional: direct commands
    application.add_handler(CommandHandler('profile', show_profile))
    application.add_handler(CommandHandler('partner', start_partner_menu))
    application.add_handler(CommandHandler('history', show_period_history))
    application.add_handler(CommandHandler('track', start_track_period))
    application.add_handler(CommandHandler('analysis', show_cycle_analysis))
    
    print("🤖 Period Tracker Bot is running...")
    application.run_polling()

if __name__ == '__main__':
    main()
