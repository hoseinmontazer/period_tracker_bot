import os

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
BASE_URL = "https://api-period.shirpala.ir/"
TOKEN_FILE = "user_tokens.json"
PERIODS_API = f"{BASE_URL}api/periods/"
