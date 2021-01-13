import os
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
DB_FILENAME = os.getenv('DB_FILENAME')
GOLD_URL = os.getenv('GOLD_URL')
GOLD_URL2 = os.getenv('GOLD_URL2')
USD_URL = os.getenv('USD_URL')