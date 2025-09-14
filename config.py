import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
BASE_URL = os.getenv("BASE_URL", "https://api-period.shirpala.ir/")
BOT_TOKEN = os.getenv("BOT_TOKEN", "7527376290:AAFdYSSYJfOj1hZNsxM92U3v64yzfa3gd3U")

# Bot settings
ADMIN_IDS = [123456789]  # Add your admin user IDs