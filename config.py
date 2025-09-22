import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
BASE_URL = os.getenv("BASE_URL", "https://api-period.shirpala.ir/")
WEB_APP_URL = os.getenv("WEB_APP_URL", "https://calendar.shirpala.ir/period_calendar")
BOT_TOKEN = os.getenv("BOT_TOKEN", "7016956457:AAHpK-nXYG1U7yYuCa8c6UrTO55QHxOtSuw")

# Bot settings
ADMIN_IDS = [123456789]  # Add your admin user IDs