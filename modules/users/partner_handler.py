from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ContextTypes
from constants import ACCEPT_REMOVE_CODE, DASHBOARD, MAIN_MENU, PROFILE_VIEW, PARTNER_MENU, ACCEPT_INVITATION, REMOVE_PARTNER
from utils.token_store import get_token
from .api import get_profile, get_invitation_code, generate_invitation_code, accept_invitation_code, remove_partner
from utils.helpers import format_profile_data

async def start_partner_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show partner menu"""
    chat_id = update.effective_chat.id
    token = context.user_data.get("token") or get_token(chat_id)
    print("start_partner_menu")
    if not token:
        await update.message.reply_text("Please login first.")
        return DASHBOARD
    keyboard = [
        ["🗓️ View Partner Cycle", "💬 Send Message to Partner"],
        ["🤝 Add Partner", "❌ Remove Partner"],
        ["⬅️ Back to Dashboard"]
    ]

    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text("👥 Partner Management:", reply_markup=reply_markup)
    return PARTNER_MENU

async def handle_partner_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle partner menu actions"""
    text = update.message.text
    chat_id = update.effective_chat.id
    token = context.user_data.get("token") or get_token(chat_id)
    
    if text == "📋 My Invitation Code":
        await update.message.reply_chat_action(action="typing")
        result = await get_invitation_code(token)
        print("resualt get_invitation_code code is : %s",result)
        if "invitation_code" in result:
            await update.message.reply_text(f"Your code: `{result['invitation_code']}`", parse_mode='Markdown')
        else:
            await update.message.reply_text("❌ No invitation code found.")
        
        return PARTNER_MENU
    
    elif text == "🎫 Generate New Code":
        await update.message.reply_chat_action(action="typing")
        result = await generate_invitation_code(token)
        print("resualt generate code is : %s",result)
        if "invitation_code" in result:
            await update.message.reply_text(f"New code: `{result['invitation_code']}`", parse_mode='Markdown')
        else:
            await update.message.reply_text("❌ Failed to generate code.")
        
        return PARTNER_MENU
    
    elif text == "🤝 Accept Invitation":
        await update.message.reply_text("Enter invitation code:", reply_markup=ReplyKeyboardRemove())
        return ACCEPT_INVITATION
    
    elif text == "❌ Remove Partner":
        keyboard = [
            ["❌ Remove Partner", "🎫 Get REMOVE Code"],
            ["⬅️ Back to Dashboard"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            
        await update.message.reply_text("❌ Remove Management:", reply_markup=reply_markup)
        return REMOVE_PARTNER
    
    elif text == "🤝 Add Partner":
        keyboard = [
            ["📋 My Invitation Code", "🎫 Generate New Code"],
            ["🤝 Accept Invitation"],
            ["⬅️ Back to Dashboard"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            
        await update.message.reply_text("Please use the menu options:", reply_markup=reply_markup)
        return PARTNER_MENU
    elif text == "💬 Send Message to Partner":
    
        await update.message.reply_text("We're working hard on this! You'll be able to message your partner soon.")
        return PARTNER_MENU
    elif text == "🗓️ View Partner Cycle":
        from modules.periods.handlers import show_partner_period_history
        return await show_partner_period_history(update, context)
    elif text == "⬅️ Back to Dashboard":
        from modules.users.handlers import show_dashboard
        return await show_dashboard(update, context)
    
    await update.message.reply_text("Please use the menu options.")
    return PARTNER_MENU

async def handle_accept_invitation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle invitation acceptance"""
    code = update.message.text.strip()
    chat_id = update.effective_chat.id
    token = context.user_data.get("token") or get_token(chat_id)
    print("code is %s", code)
    if not code:
        await update.message.reply_text("Please enter a valid code.")
        return ACCEPT_INVITATION
    
    await update.message.reply_chat_action(action="typing")
    result = await accept_invitation_code(token, code)
    print("resualt accept_invitation_code code is : %s",result)

    if result.get("message") == "Invitation code accepted successfully":
        partner_name = result.get("partner", "Partner")
        await update.message.reply_text(f"✅ Invitation accepted! Connected with {partner_name}.")
    elif "code_to_accept" in result:
        error_msg = result["code_to_accept"][0]
        await update.message.reply_text(f"❌ {error_msg}")
    else:
        await update.message.reply_text("❌ Failed to accept invitation.")
    
    return await start_partner_menu(update, context)



async def handle_remove_partner(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle partner removal"""
    text = update.message.text
    print(text)
    chat_id = update.effective_chat.id
    token = context.user_data.get("token") or get_token(chat_id)
    
    if  text == "🎫 Get REMOVE Code":
        await update.message.reply_chat_action(action="typing")
        code = None
        result = await remove_partner(token, code)
        print(result)
        if "remove_code" in result:
            # await update.message.reply_text("✅ Partner removed!")
            await update.message.reply_text(f"Your code: `{result['remove_code']}`", parse_mode='Markdown')

        else:
            await update.message.reply_text("❌ Failed to get remove partner.")
        
        return await start_partner_menu(update, context)
    
    elif text == "❌ Remove Partner":
        # code = update.message.text.strip()
        token = context.user_data.get("token")
        
        await update.message.reply_text("Please enter a valid code.")
        return ACCEPT_REMOVE_CODE
    
async def handel_accept_remove_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    code = update.message.text.strip()
    chat_id = update.effective_chat.id
    token = context.user_data.get("token") or get_token(chat_id)
    print("code is %s", code)
    if not code:
        await update.message.reply_text("Please enter a valid code.")
        return REMOVE_PARTNER
    
    await update.message.reply_chat_action(action="typing")
    result = await remove_partner(token, code)
    print(result)
    if "message" in result:
        await update.message.reply_text(f"✅ `{result['message']}`!")
    else:
        await update.message.reply_text("❌ Failed to remove partner.")
    
    return await start_partner_menu(update, context)
