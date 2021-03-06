import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import CallbackQuery

import message
from keyboards.inline.callback import gold_choice_callback
from keyboards.inline.gold_keyboard import new_keyboard
from data import value_db, users_db
from config import config

logging.basicConfig(level=logging.ERROR,
                    filename='bot.log',
                    format='%(asctime)s %(name)s: %(levelname)s [%(process)d] %(message)s')
bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start_message(message: types.Message):
    gr_999_rub = round(value_db.read_value_db('gr_999_rub'))
    gr_999_usd = value_db.read_value_db('gr_999_usd')
    await message.answer(f'📈 Цена золота 999 пробы:\n'
                         f'{gr_999_rub} ₽ за грамм\n'
                         f'{gr_999_usd} $ за грамм\n'
                         f'Какая проба Вас интересует?\n',
                         reply_markup=new_keyboard('999')
                         )
    user = message.from_user
    users_db.check_user(user)


@dp.callback_query_handler(gold_choice_callback.filter(metal='gold'))
async def gold_choice_message(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=10)

    selected_gold = callback_data.get('probe')
    db_unit = callback_data.get('db_unit')

    m = message.Text(selected_gold, db_unit)
    text = m.get_message()

    await call.message.delete_reply_markup()
    await call.message.answer(text, reply_markup=new_keyboard(selected_gold))

    user = call.from_user
    users_db.check_user(user)
    users_db.increase_value_in_stat_db('clicks')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
