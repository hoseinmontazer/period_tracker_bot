import aiohttp
from telegram.ext import CallbackContext, ConversationHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from config import BASE_URL
from languages import get_message
from menus import get_main_menu
from states import ACCEPT_INVITE_CODE, ACCEPT_REMOVE_CODE, LANGUAGE_SELECTION, MENU, PARTNER_MENU, PROFILE_MENU, REMOVE_PARTNER


async def start_partner_menu(update: Update, context: CallbackContext) -> int:
    print("start_partner_menu")
    """Start the partner menu."""
    lang = context.user_data.get('language', 'en')
    
    # Create partner menu keyboard
    partner_keyboard = [
        [
            get_message(lang, 'partner', 'add_partner'),
            get_message(lang, 'partner', 'view_partners')
        ],
        [
            get_message(lang, 'partner', 'get_invite_code'),
            get_message(lang, 'partner', 'accept_invite')
        ],
        [
            get_message(lang, 'partner', 'get_remove_code'),
            get_message(lang, 'partner', 'remove_partner'),
        ],
        [
                    get_message(lang, 'partner', 'send_message'),
        ],
        [
            get_message(lang, 'partner', 'back_to_main_menu')
        ]
    ]
        
    markup = ReplyKeyboardMarkup(
        partner_keyboard,
        one_time_keyboard=False,
        resize_keyboard=True
    )
    
    partner_text = get_message(lang, 'partner', 'partner_menu')
    await update.message.reply_text(partner_text, reply_markup=markup)
    return PARTNER_MENU

async def handle_partner_menu(update: Update, context: CallbackContext) -> int:
    print("handle_partner_menu")
    """Handle partner menu selections."""
    text = update.message.text
    lang = context.user_data.get('language', 'en')
    
    if text == get_message(lang, 'partner', 'add_partner'):
        await update.message.reply_text("Add Partner functionality is not implemented yet.")
        return PARTNER_MENU

    elif text == get_message(lang, 'partner', 'view_partners'):
        await update.message.reply_text("View Partners functionality is not implemented yet.")
        return PARTNER_MENU
    elif text == get_message(lang, 'partner', 'get_invite_code'):
        print("Fetching invite code...")
        chat_id = str(update.message.chat_id)
        user_tokens = context.bot_data.get('user_tokens', {})
        access_token = user_tokens.get(chat_id, {}).get('access')


        if not access_token:
            print("No access token found for user.")
            await update.message.reply_text(get_message(lang, 'errors', 'something_went_wrong'))
            return PARTNER_MENU  # not PROFILE_MENU, since this is inside partner

        headers = {"Authorization": f"Bearer {access_token}"}
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{BASE_URL}/api/user/invitation/",
                    headers=headers
                ) as response:
                    data = await response.json()

                    if response.status == 201 and "invitation_code" in data:
                        code = data.get("invitation_code")
                        expires = data.get("expires_in", 0) // 3600  # convert seconds → hours
                        msg = get_message(lang, 'partner', 'invite_code_success').format(
                            code=f"`{code}`",
                            hours=expires
                        )
                        await update.message.reply_text(msg, parse_mode='Markdown')
                    else:
                        print(f"Failed to fetch invite code: {data}")
                        # API returned error JSON with "message"
                        error_msg = data.get("message", get_message(lang, 'errors', 'something_went_wrong'))
                        await update.message.reply_text(error_msg)
        except Exception as e:
            print(f"Error removing partner: {e}")
            await update.message.reply_text(get_message(lang, 'errors', 'something_went_wrong'))
        
        return PARTNER_MENU

    elif text == get_message(lang, 'partner', 'accept_invite'):
        language_keyboard = [
            [get_message(lang, 'buttons', 'done')],
            [get_message(lang, 'settings', 'back_to_main_menu')]
        ]
        markup = ReplyKeyboardMarkup(
            language_keyboard,
            one_time_keyboard=False,
            resize_keyboard=True,
            selective=True
        )
        await update.message.reply_text(
            get_message(lang, 'partner', 'enter_invite_code'),
            reply_markup=markup
        )
        context.user_data['invite_code'] = None
        context.user_data['state'] = ACCEPT_INVITE_CODE  
        return ACCEPT_INVITE_CODE

    elif text == get_message(lang, 'partner', 'get_remove_code'):
        print("Fetching remove code...")
        chat_id = str(update.message.chat_id)
        user_tokens = context.bot_data.get('user_tokens', {})
        access_token = user_tokens.get(chat_id, {}).get('access')
        if not access_token:
            print("No access token found for user.")
            await update.message.reply_text(get_message(lang, 'errors', 'something_went_wrong'))
            return PARTNER_MENU

        headers = {"Authorization": f"Bearer {access_token}"}

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{BASE_URL}/api/user/partner/remove/",
                    headers=headers
                ) as response:
                    data = await response.json()
                    print(data)
                    # Show error message from API if exists
                    if "error" in data:
                        await update.message.reply_text(data["error"])
                    elif response.status in [200, 201]:
                        code = data.get("remove_code")
                        expires = data.get("expires_in", 0) // 3600  
                        msg = get_message(lang, 'partner', 'remove_code_success').format(
                            code=f"{code}",
                            hours=expires
                        )
                        await update.message.reply_text(msg)
                    else:
                        await update.message.reply_text(get_message(lang, 'errors', 'something_went_wrong'))

        except Exception as e:
            print(f"Error removing partner: {e}")
            await update.message.reply_text(get_message(lang, 'errors', 'something_went_wrong'))

        return PARTNER_MENU
      
    elif text == get_message(lang, 'partner', 'remove_partner'):
        language_keyboard = [
            [get_message(lang, 'buttons', 'done')],
            [get_message(lang, 'settings', 'back_to_main_menu')]
        ]
        markup = ReplyKeyboardMarkup(
            language_keyboard,
            one_time_keyboard=False,
            resize_keyboard=True,
            selective=True
        )
        await update.message.reply_text(
            get_message(lang, 'partner', 'enter_remove_code'),
            reply_markup=markup
        )
        context.user_data['remove_code'] = None
        context.user_data['state'] = ACCEPT_REMOVE_CODE  
        return ACCEPT_REMOVE_CODE
        
    elif text == get_message(lang, 'menu', 'back_to_main_menu'):
        # Return to main menu
        from menus import get_main_menu  # Import here to avoid circular import
        markup, menu_text = get_main_menu(lang)
        await update.message.reply_text(menu_text, reply_markup=markup)
        context.user_data['state'] = MENU
        return MENU
    
    else:
        await update.message.reply_text(get_message(lang, 'errors', 'invalid_option'))
        return PARTNER_MENU
    
async def handle_accept_invite_code(update: Update, context: CallbackContext) -> int:
    lang = context.user_data.get('language', 'en')
    text = update.message.text
    done_text = get_message(lang, 'buttons', 'done')
    back_text = get_message(lang, 'settings', 'back_to_main_menu')

    # Back button → return to Partner Menu
    if text == back_text:
        return await start_partner_menu(update, context)

    # User typing invite code → store it
    if text != done_text:
        current_code = context.user_data.get('invite_code')
        if current_code == text:
            # Already entered, ignore or remind user
            await update.message.reply_text(
                f"ℹ️ {get_message(lang, 'partner', 'invite_code_already_entered')}: {text}"
            )
        else:
            context.user_data['invite_code'] = text
            await update.message.reply_text(
                f"✅ {get_message(lang, 'partner', 'invite_code_entered')}: {text}"
            )
        return ACCEPT_INVITE_CODE


    # Done pressed → submit code
    code = context.user_data.get('invite_code')
    if not code:
        await update.message.reply_text(get_message(lang, 'partner', 'no_code_entered'))
        return ACCEPT_INVITE_CODE

    chat_id = str(update.message.chat_id)
    access_token = context.bot_data.get('user_tokens', {}).get(chat_id, {}).get('access')
    if not access_token:
        await update.message.reply_text(get_message(lang, 'errors', 'something_went_wrong'))
        return PARTNER_MENU

    headers = {"Authorization": f"Bearer {access_token}"}
    data = {"code_to_accept": code}

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{BASE_URL}/api/user/invitation/",
                headers=headers,
                json=data  # <-- use JSON, not form-data
            ) as response:
                resp_json = await response.json(content_type=None)

                if response.status in [200, 201]:
                    partner_name = resp_json.get("partner", "Unknown")
                    msg = get_message(lang, 'partner', 'invite_accept_success').format(
                        partner=partner_name
                    )
                    await update.message.reply_text(f"✅ {msg}")
                    # ✅ Reset state and clear invite code
                    context.user_data['state'] = MENU
                    context.user_data['invite_code'] = None

                    # ✅ After success → show main menu
                    markup, menu_text = get_main_menu(lang)
                    await update.message.reply_text(menu_text, reply_markup=markup)
                    return MENU

                elif response.status == 400:
                    error_list = resp_json.get("code_to_accept", ["Invalid or expired invitation code"])
                    await update.message.reply_text(f"❌ {error_list[0]}")
                    return ACCEPT_INVITE_CODE  # stay in code entry state

                else:
                    await update.message.reply_text(
                        f"❌ {get_message(lang, 'errors', 'something_went_wrong')} ({response.status})"
                    )

    except Exception as e:
        print(f"Error accepting invite: {e}")
        await update.message.reply_text(get_message(lang, 'errors', 'something_went_wrong'))

    # Default fallback → back to partner menu
    return await start_partner_menu(update, context)



async def handle_accept_remove_code(update: Update, context: CallbackContext) -> int:
    """Handle partner remove code input and submission."""
    print("handle_accept_remove_code")
    
    lang = context.user_data.get('language', 'en')
    text = update.message.text
    done_text = get_message(lang, 'buttons', 'done')
    back_text = get_message(lang, 'settings', 'back_to_main_menu')

    # Back button → return to Partner Menu
    if text == back_text:
        context.user_data['state'] = MENU
        context.user_data['remove_code'] = None
        return await start_partner_menu(update, context)

    # User typing remove code → store it
    if text != done_text:
        context.user_data['remove_code'] = text
        await update.message.reply_text(
            f"✅ {get_message(lang, 'partner', 'remove_code_entered')}: {text}"
        )
        return REMOVE_PARTNER

    # Done pressed → submit code
    remove_code = context.user_data.get('remove_code')
    if not remove_code:
        await update.message.reply_text(get_message(lang, 'partner', 'no_remove_code_entered'))
        return REMOVE_PARTNER

    chat_id = str(update.message.chat_id)
    access_token = context.bot_data.get('user_tokens', {}).get(chat_id, {}).get('access')
    if not access_token:
        await update.message.reply_text(get_message(lang, 'errors', 'something_went_wrong'))
        return PARTNER_MENU

    headers = {"Authorization": f"Bearer {access_token}"}
    data = {"remove_code": remove_code}

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{BASE_URL}/api/user/partner/remove/", headers=headers, data=data) as response:
                resp_json = await response.json(content_type=None)

                # ✅ Success
                if response.status in [200, 201]:
                    partner_name = resp_json.get("partner", "Unknown")
                    msg = get_message(lang, 'partner', 'partner_removed_success').format(partner=partner_name)
                    await update.message.reply_text(f"✅ {msg}")

                    # Reset state and remove_code
                    context.user_data['state'] = MENU
                    context.user_data['remove_code'] = None

                    # Show Partner Menu
                    return await start_partner_menu(update, context)

                # ❌ Invalid code
                elif response.status == 400:
                    error_list = resp_json.get("remove_code", ["Invalid or expired remove code"])
                    await update.message.reply_text(f"❌ {error_list[0]}")
                    return ACCEPT_REMOVE_CODE  # stay in remove code entry state

                # ❌ Other errors
                else:
                    await update.message.reply_text(
                        f"❌ {get_message(lang, 'errors', 'something_went_wrong')} ({response.status})"
                    )
                    # Return to partner menu
                    context.user_data['state'] = MENU
                    context.user_data['remove_code'] = None
                    return await start_partner_menu(update, context)

    except Exception as e:
        print(f"Error removing partner: {e}")
        await update.message.reply_text(get_message(lang, 'errors', 'something_went_wrong'))
        # Fallback → partner menu
        context.user_data['state'] = MENU
        context.user_data['remove_code'] = None
        return await start_partner_menu(update, context)


    # Return to Partner Menu after handling
    # from handlers.partner.partner import start_partner_menu
    # return await start_partner_menu(update, context)

