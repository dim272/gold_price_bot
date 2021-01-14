import logging

from aiogram import Bot, Dispatcher
from config import BOT_TOKEN

logging.basicConfig(filename='bot.log',
                    format='%(asctime)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S')
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)