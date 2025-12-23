import os
from dotenv import load_dotenv
from datetime import datetime
import pytz

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
SECRET_TOKEN = os.getenv("SECRET_TOKEN")

TIMEZONE = pytz.timezone(os.getenv("TIMEZONE"))
OPEN_TIME = TIMEZONE.localize(
    datetime.strptime(os.getenv("OPEN_TIME"), "%Y-%m-%d %H:%M:%S")
)
