# languages.py

# پیام‌ها برای زبان انگلیسی و فارسی
MESSAGES = {
    'en': {
        'welcome': {
            'bot': "Welcome! This bot helps you track and analyze your periods.",
            "choose_option": "Please choose one of the options:",
            "start": "Welcome to the bot!"
        },
        'auth': {
            'register': "Register",
            'login': "Login",
            "enter_username": "Please enter your username:",
            "enter_password": "Please enter your password:",
            "login_failed": "Username or password is incorrect."


        },
        'menu': {
            'main': "Main Menu:",
            'track_period': "📅 Track Period",
            'view_history': "📖 View History",
            'cycle_analysis': "📊 Cycle Analysis",
            'add_new_cycle': "➕ Add New Cycle",
            'partner_menu': "👥 Partner Menu"
        },
        "cycle": {
            "enter_start_date": "Please enter the start date of your cycle (YYYY-MM-DD):",
            "cycle_added": "Cycle added successfully!",
            "add_failed": "Failed to add cycle"
        },
        'settings': {
            'menu': "⚙️ Settings"
        },
        'errors': {
            'operation_cancelled': "Operation cancelled."
        }

    },
    'fa': {
        'welcome': {
            'bot': "خوش آمدید! این ربات به شما کمک می‌کند سیکل‌های قاعدگی خود را ثبت و تحلیل کنید.",
             "start": "به ربات خوش آمدید!" ,
            "choose_option": "لطفاً یکی از گزینه‌ها را انتخاب کنید:"
        },
        'auth': {
            'register': "ثبت‌نام",
            'login': "ورود",
            "enter_username": "نام کاربری خود را وارد کنید:",
            "enter_password": "لطفاً رمز عبور خود را وارد کنید:",
            "login_failed": "نام کاربری یا رمز عبور اشتباه است."
        },
        'menu': {
            'main': "منوی اصلی:",
            'track_period': "📅 ثبت دوره",
            'view_history': "📖 مشاهده تاریخچه",
            'cycle_analysis': "📊 تحلیل سیکل",
            'add_new_cycle': "➕ اضافه کردن سیکل جدید",
            'partner_menu': "👥 منوی شریک"
        },
        'settings': {
            'menu': "⚙️ تنظیمات"
        },
        'errors': {
            'operation_cancelled': "عملیات لغو شد."
        }
    }
}
SYMPTOM_OPTIONS = {
    'en': [
        ['Cramps', 'Headache', 'Fatigue'],
        ['Bloating', 'Mood Swings', 'Acne'],
        ['Back Pain', 'Breast Tenderness'],
        ['Write Custom Symptoms', 'Done']
    ],
    'fa': [
        ['گرفتگی', 'سردرد', 'خستگی'],
        ['نفخ', 'تغییرات خلقی', 'جوش'],
        ['کمر درد', 'حساسیت سینه'],
        ['نوشتن علائم سفارشی', 'پایان']
    ]
}

MEDICATION_OPTIONS = {
    'en': [
        ['Ibuprofen', 'Acetaminophen'],
        ['Birth Control Pills', 'Pain Relievers'],
        ['Write Custom Medication', 'Done']
    ],
    'fa': [
        ['ایبوپروفن', 'استامینوفن'],
        ['قرص‌های ضد بارداری', 'مسکن'],
        ['نوشتن داروی سفارشی', 'پایان']
    ]
}

def get_message(lang: str, section: str, key: str) -> str:
    if lang not in MESSAGES:
        lang = 'en'
    return MESSAGES[lang].get(section, {}).get(key, f"[Missing message: {section}.{key}]")

