from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ContextTypes
from constants import DASHBOARD, MAIN_MENU, PROFILE_VIEW, PARTNER_MENU, ACCEPT_INVITATION, REMOVE_PARTNER
from modules.users.partner_handler import start_partner_menu
from utils.helpers import format_profile_data
from utils.token_store import get_token
from .api import get_profile

async def show_dashboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show user dashboard"""
    # token = context.user_data.get("token")
    # username = context.user_data.get("username", "User")

    chat_id = update.effective_chat.id
    token = context.user_data.get("token") or get_token(chat_id)
    
    if not token:
        keyboard = [
            ["Login", "Register"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
        await update.message.reply_text("🔐 Please login or register first:", reply_markup=reply_markup)
        return MAIN_MENU  
    else:
        username = context.user_data.get("username", "User")
        keyboard = [
            ["📅 Track Period", "📊 Cycle Analysis"],
            ["👤 My Profile", "👥 Partner"],
            ["📋 Period History"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        
        await update.message.reply_text(
            f"🏠 Welcome back, {username}!",
            reply_markup=reply_markup
        )
        return DASHBOARD

async def handle_dashboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle dashboard actions"""
    text = update.message.text
    print("text" , text)
    if text == "👤 My Profile":
        return await show_profile(update, context)
    elif text == "👥 Partner":
        return await start_partner_menu(update, context)
    elif text == "📅 Track Period":
        from modules.periods.handlers import start_track_period
        return await start_track_period(update, context)
    elif text == "📊 Cycle Analysis":
        from modules.analysis.handlers import show_cycle_analysis
        return await show_cycle_analysis(update, context)
    elif text == "📋 Period History":
        from modules.periods.handlers import show_period_history
        return await show_period_history(update, context)
    
    await update.message.reply_text("Please use the menu options.")
    return DASHBOARD

async def show_profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show user profile"""
    chat_id = update.effective_chat.id
    token = context.user_data.get("token") or get_token(chat_id)
    
    if not token:
        await update.message.reply_text("Please login first.")
        return DASHBOARD
    
    await update.message.reply_chat_action(action="typing")
    profile_data = await get_profile(token)
    
    if "detail" in profile_data:
        await update.message.reply_text("❌ Error loading profile.")
    else:
        formatted_profile = format_profile_data(profile_data)
        await update.message.reply_text(formatted_profile, parse_mode='Markdown')
    
    keyboard = [["⬅️ Back to Dashboard"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("What would you like to do?", reply_markup=reply_markup)
    return PROFILE_VIEW

async def handle_profile_view(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle profile view actions"""
    text = update.message.text
    
    if text == "⬅️ Back to Dashboard":
        return await show_dashboard(update, context)
    
    await update.message.reply_text("Please use the menu options.")
    return PROFILE_VIEW

# async def start_partner_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     """Show partner menu"""
#     chat_id = update.effective_chat.id
#     token = context.user_data.get("token") or get_token(chat_id)
    
#     if not token:
#         await update.message.reply_text("Please login first.")
#         return DASHBOARD
    
#     keyboard = [
#         ["📋 My Invitation Code", "🎫 Generate New Code"],
#         ["🤝 Accept Invitation", "❌ Remove Partner"],
#         ["⬅️ Back to Dashboard"]
#     ]
#     reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
#     await update.message.reply_text("👥 Partner Management:", reply_markup=reply_markup)
#     return PARTNER_MENU

# async def handle_partner_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     """Handle partner menu actions"""
#     text = update.message.text
#     chat_id = update.effective_chat.id
#     token = context.user_data.get("token") or get_token(chat_id)
    
#     if text == "📋 My Invitation Code":
#         await update.message.reply_chat_action(action="typing")
#         result = await get_invitation_code(token)
        
#         if "code" in result:
#             await update.message.reply_text(f"Your code: `{result['code']}`", parse_mode='Markdown')
#         else:
#             await update.message.reply_text("❌ No invitation code found.")
        
#         return PARTNER_MENU
    
#     elif text == "🎫 Generate New Code":
#         await update.message.reply_chat_action(action="typing")
#         result = await generate_invitation_code(token)
        
#         if "code" in result:
#             await update.message.reply_text(f"New code: `{result['code']}`", parse_mode='Markdown')
#         else:
#             await update.message.reply_text("❌ Failed to generate code.")
        
#         return PARTNER_MENU
    
#     elif text == "🤝 Accept Invitation":
#         await update.message.reply_text("Enter invitation code:", reply_markup=ReplyKeyboardRemove())
#         return ACCEPT_INVITATION
    
#     elif text == "❌ Remove Partner":
#         await update.message.reply_text("Enter partner code to remove:", reply_markup=ReplyKeyboardRemove())
#         return REMOVE_PARTNER
    
#     elif text == "⬅️ Back to Dashboard":
#         return await show_dashboard(update, context)
    
#     await update.message.reply_text("Please use the menu options.")
#     return PARTNER_MENU

# async def handle_accept_invitation(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     """Handle invitation acceptance"""
#     code = update.message.text.strip()
#     token = context.user_data.get("token")
    
#     if not code:
#         await update.message.reply_text("Please enter a valid code.")
#         return ACCEPT_INVITATION
    
#     await update.message.reply_chat_action(action="typing")
#     result = await accept_invitation_code(token, code)
    
#     if "detail" in result:
#         await update.message.reply_text("✅ Partner connected!")
#     else:
#         await update.message.reply_text("❌ Failed to accept invitation.")
    
#     return await start_partner_menu(update, context)

# async def handle_remove_partner(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     """Handle partner removal"""
#     code = update.message.text.strip()
#     token = context.user_data.get("token")
    
#     if not code:
#         await update.message.reply_text("Please enter a valid code.")
#         return REMOVE_PARTNER
    
#     await update.message.reply_chat_action(action="typing")
#     result = await remove_partner(token, code)
    
#     if "detail" in result:
#         await update.message.reply_text("✅ Partner removed!")
#     else:
#         await update.message.reply_text("❌ Failed to remove partner.")
    
#     return await start_partner_menu(update, context)