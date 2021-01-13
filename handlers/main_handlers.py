from aiogram import types
from aiogram.types import CallbackQuery

from keyboards.inline.callback import gold_choice_callback
from keyboards.inline.gold_keyboard import gold_choice
from bot import get_data
from loader import dp


@dp.message_handler(commands=['start'])
async def start_message(message: types.Message):
    data_from_db = get_data()
    await message.answer(f"Цена одного грамма чистого золота 999 пробы (24K):\n"
                         f"The price of one gram of pure gold 999 (24 karat):\n"
                         f"₽ - {data_from_db['gr_999_rub']}\n"
                         f"$ - {data_from_db['gr_999_usd']}\n"
                         f"Какая проба Вас интересует?\n"
                         f"What gold are you interested in?",
                         reply_markup=gold_choice
                         )


@dp.callback_query_handler(gold_choice_callback.filter(metal='gold'))
async def gold_choice_message(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=60)
    data_from_db = get_data()
    gr_999_usd = data_from_db['gr_999_usd']
    selected_gold = callback_data.get('probe')
    key_from_db = f'gr_{selected_gold}_rub'
    price_rub = data_from_db[key_from_db]
    price_usd = round((gr_999_usd * (int(selected_gold) / 1000)), 2)
    await call.message.answer(f"Цена одного грамма золота {selected_gold} пробы:\n"
                              f"The price of one gram of {selected_gold} gold:\n"
                              f"₽ - {price_rub}\n"
                              f"$ - {price_usd}\n"
                              f"Какая проба Вас интересует?\n"
                              f"What gold are you interested in?",
                              reply_markup=gold_choice)
