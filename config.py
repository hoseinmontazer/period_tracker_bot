import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
BASE_URL = os.getenv("BASE_URL", "https://api-period.shirpala.ir/")
WEB_APP_URL = os.getenv("WEB_APP_URL", "https://calendar.shirpala.ir/period_calendar")
BOT_TOKEN = os.getenv("BOT_TOKEN", "7016956457:AAHpK-nXYG1U7yYuCa8c6UrTO55QHxOtSuw")

# Bot settings
ADMIN_IDS = [123456789]  # Add your admin user IDs

# WellBe App Configuration
APP_NAME = "WellBe"
APP_TAGLINE = "Your Complete Health Companion"
APP_VERSION = "2.0"

# Available Health Modules
HEALTH_MODULES = {
    "period_tracker": {"name": "Period Tracker", "emoji": "📅", "enabled": True},
    "medication": {"name": "Medications", "emoji": "💊", "enabled": True},
    "fitness": {"name": "Fitness", "emoji": "🏃", "enabled": False},  # Coming soon
    "nutrition": {"name": "Nutrition", "emoji": "🍎", "enabled": False},  # Coming soon
    "sleep": {"name": "Sleep", "emoji": "😴", "enabled": False},  # Coming soon
    "mental_health": {"name": "Mental Health", "emoji": "🧘", "enabled": False},  # Coming soon
    "vitals": {"name": "Vital Signs", "emoji": "🩸", "enabled": False}  # Coming soon
}