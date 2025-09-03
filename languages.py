# languages.py

MESSAGES = {
    'en': {
        'buttons': {
            'done': 'Done',
            'cancel': 'Cancel',
            'write_custom_symptoms': 'Write Custom Symptoms',
            'write_custom_medication': 'Write Custom Medication',
            'back_to_menu': '🏠 Back to Main Menu'
        },
        'cycle': {
            'select_symptoms': "Please select your symptoms:",
            'custom_symptoms': "Please write your custom symptoms:",
            'select_medications': "Please select your medications:",
            'custom_medication': "Please write your custom medication:",
            'added_item': "✅ Added: {item}\nCurrent {title}: {current}",
            'save_success': "Cycle saved successfully ✅",
            'save_failed': "Failed to save cycle. Please try again.",
            'cancelled': "Operation cancelled.",
            'select_date': "Please select the start date of your cycle:"
        },
        'cycle_analysis': {
            'header' :"📊 *Cycle Analysis*\n\n",
            'menu': "Cycle Analysis Menu",
            'view_analysis': "View Analysis",
            'back_to_main_menu': "🏠 Back to Main Menu",
            'feature_coming_soon': "This feature is coming soon!",
            'average_cycle': "Average Cycle",
            'regularity_score': "Regularity Score",
            'prediction_reliability': "Prediction Reliability",
            'next_predicted_date': "Next Predicted Date",
            'cycle_variations': "Cycle Variations"

        },
        'partner': {
            'partner_request_sent': "✅ Partner request sent to {email}.",
            'no_partners': "You have no partners.",
            'partners_list': "👥 *Your Partners:*\n\n{partners}",
            'remove_partner_prompt': "Please select a partner to remove:",
            'partner_removed': "✅ Partner {username} has been removed.",
            'no_partners_to_remove': "You have no partners to remove.",
            'add_partner': "Add Partner",
            'view_partners': "View Partners",
            'remove_partner': "Remove Partner",
            'get_invite_code': "Get Invite Code",
            'invite_code_success': "Your invite code is: `{code}`\nIt expires in {hours} hours.",
            'remove_code_success': "Your Remove code is: `{code}`\nIt expires in {hours} hours.",
            'accept_invite': "Accept Invite",
            'enter_invite_code': "Please enter the invite code you received from your partner:",
            'enter_remove_code': "Please enter the remove code you received:",
            'get_remove_code': "Get Remove Code",
            'send_message': "Send Message",
            'no_code_enterd': "no code enterd",
            'invite_code_entered':"invite code enterd",
            'remove_code_entered':"remove code enterd",
            "invite_accept_success": "Invitation code accepted successfully! Partner: {partner}",
            "partner_removed_success": "Removed code accepted successfully! Partner Removed: {partner}",
            "invite_accept_success_generic": "Invitation code accepted successfully!",
            'back_to_main_menu': "🏠 Back to Main Menu",
            'partner_menu': "Partner Menu"
        },
        'menu': {
            'main': "Main Menu",
            'track_period': "Track Period",
            'view_history': "View History",
            'cycle_analysis': "Cycle Analysis",
            'add_new_cycle': "➕ Add New Cycle",
            'partner_menu': "👥 Partner Menu",
            'back_to_main_menu': '🏠 Back to Main Menu'
        },
        'settings': {
            'menu': '⚙️ Settings Menu',
            'choose_language': '🌐 Change Language',
            'select_language': 'Please select your language:',
            'language_changed': 'Language changed successfully!',
            'cancelled': 'Settings cancelled.',
            'language': 'Language',
            'notifications': 'Notifications',
            'profile': 'Profile',
            'privacy': 'Privacy',
            'help': 'Help',
            'back_to_main_menu': '🏠 Back to Main Menu',
            'EN': 'English',
            'FA': 'فارسی',
        },
        'history': {
            'cycle_id': '🔹 **Cycle ID:**',
            'start_date': '🟢 Start:',
            'predicted_end': '🔮 Predicted End:',
            'actual_end': '✅ Actual End:',
            'medication': '💊 Medication:',
            'symptoms': '⚡ Symptoms:',
            'ongoing': 'ongoing',
            'none': 'None',
            'separator': '-------------------------'
        },
        'Profile': {
            'menu': 'Profile',
            'view_profile': 'View Profile',
            'edit_profile': 'Edit Profile',
            'back_to_main_menu': '🏠 Back to Main Menu',
            'feature_coming_soon': 'This feature is coming soon!'
        },
        'errors': {
            'invalid_option': 'Invalid option. Please try again.',
            'something_went_wrong': 'Something went wrong. Please try again later.',
            'operation_cancelled': 'Operation cancelled.'
        }

    },
    'fa': {
        'buttons': {
            'done': 'پایان',
            'cancel': 'لغو',
            'write_custom_symptoms': 'نوشتن علائم سفارشی',
            'write_custom_medication': 'نوشتن داروی سفارشی',
            'back_to_menu': '🏠 بازگشت به منوی اصلی'

        },
        'cycle': {
            'select_symptoms': "لطفاً علائم خود را انتخاب کنید:",
            'custom_symptoms': "لطفاً علائم سفارشی خود را وارد کنید:",
            'select_medications': "لطفاً داروهای خود را انتخاب کنید:",
            'custom_medication': "لطفاً داروی سفارشی خود را وارد کنید:",
            'added_item': "✅ اضافه شد: {item}\nموجودی فعلی {title}: {current}",
            'save_success': "دوره با موفقیت ذخیره شد ✅",
            'save_failed': "ذخیره دوره موفقیت آمیز نبود. لطفاً دوباره تلاش کنید.",
            'cancelled': "عملیات لغو شد.",
            'select_date': "لطفاً تاریخ شروع دوره خود را انتخاب کنید:"
        },
        'cycle_analysis': {
            'header':"📊 *تحلیل دوره*\n\n",
            'menu': "منوی تحلیل دوره",
            'view_analysis': "مشاهده تحلیل",
            'back_to_main_menu': "🏠 بازگشت به منوی اصلی",
            'feature_coming_soon': "این ویژگی به زودی اضافه خواهد شد!",
            'average_cycle': "میانگین دوره",
            'regularity_score': "امتیاز منظم بودن",
            'prediction_reliability': "قابلیت اطمینان پیش‌بینی",
            'next_predicted_date': "تاریخ پیش‌بینی‌شده بعدی",
            'cycle_variations': "تغییرات دوره"
        },
        'partners':{

        },
        'menu': {
            'main': "منوی اصلی",
            'track_period': "ثبت دوره",
            'view_history': "مشاهده تاریخچه",
            'cycle_analysis': "تحلیل دوره",
            'add_new_cycle': "➕ افزودن دوره جدید",
            'partner_menu': "منوی همسر"
        },
        'settings': {
            'menu': '⚙️ منوی تنظیمات',
            'choose_language': '🌐 تغییر زبان',
            'select_language': 'لطفا زبان خود را انتخاب کنید:',
            'language_changed': 'زبان با موفقیت تغییر کرد!',
            'cancelled': 'تنظیمات لغو شد.',
            'language': 'زبان',
            'notifications': 'اعلان‌ها',
            'profile': 'پروفایل',
            'privacy': 'حریم خصوصی',
            'help': 'راهنما',
            'back': 'بازگشت',
            'back_to_main_menu': '🏠 بازگشت به منوی اصلی', 
            'EN': 'English',
            'FA': 'فارسی',
        },
        'history': {
            'cycle_id': '🔹 **شناسه دوره:**',
            'start_date': '🟢 شروع:',
            'predicted_end': '🔮 پایان پیش‌بینی‌شده:',
            'actual_end': '✅ پایان واقعی:',
            'medication': '💊 دارو:',
            'symptoms': '⚡ علائم:',
            'ongoing': 'در حال انجام',
            'none': 'هیچ',
            'separator': '-------------------------'
        },
        'errors': {
            'invalid_option': 'گزینه نامعتبر. لطفاً دوباره تلاش کنید.'
        }
    }
}

SYMPTOM_OPTIONS = {
    'en': [
        ['Cramps', 'Headache', 'Fatigue'],
        ['Bloating', 'Mood Swings', 'Acne'],
        ['Back Pain', 'Breast Tenderness'],
        ['Write Custom Symptoms']
    ],
    'fa': [
        ['گرفتگی', 'سردرد', 'خستگی'],
        ['نفخ', 'تغییرات خلقی', 'جوش'],
        ['کمر درد', 'حساسیت سینه'],
        ['نوشتن علائم سفارشی', ]
    ]
}

MEDICATION_OPTIONS = {
    'en': [
        ['Ibuprofen', 'Naproxen', 'Paracetamol'],
        ['Magnesium', 'Vitamin B1', 'Omega-3'],
        ['Write Custom Medication']
    ],
    'fa': [
        ['ایبوپروفن', 'ناپروکسن', 'استامینوفن'],
        ['منیزیم', 'ویتامین B1', 'امگا ۳'],
        ['نوشتن داروی سفارشی']
    ]
}


def get_message(lang: str, section: str, key: str, **kwargs) -> str:
    if lang not in MESSAGES:
        lang = 'en'
    msg_template = MESSAGES[lang].get(section, {}).get(key, f"[Missing message: {section}.{key}]")
    if kwargs:
        return msg_template.format(**kwargs)
    return msg_template

