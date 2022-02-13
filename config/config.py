import os
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
TEST_BOT_TOKEN = os.getenv('TEST_BOT_TOKEN')
DB_FILENAME = os.getenv('DB_FILENAME')
VALUE_SQL_FILENAME = os.getenv('VALUE_DB')
USERS_SQL_FILENAME = os.getenv('USERS_DB')
GOLD_URL = os.getenv('GOLD_URL')
GOLD_URL2 = os.getenv('GOLD_URL2')
USD_URL = os.getenv('USD_URL')