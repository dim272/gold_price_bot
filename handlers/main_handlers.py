from aiogram import types
from aiogram.types import CallbackQuery

from keyboards.inline.callback import gold_choice_callback
from keyboards.inline.gold_keyboard import new_keyboard
from bot import get_data
from loader import dp


@dp.message_handler(commands=['start'])
async def start_message(message: types.Message):
    data_from_db = get_data()
    await message.answer(f'📈 Цена золота 999 пробы:\n'
                         f'{data_from_db["gr_999_rub"]} ₽ за грамм\n'
                         f'{data_from_db["gr_999_usd"]} $ за грамм\n'
                         f'Какая проба Вас интересует?\n',
                         reply_markup=new_keyboard('999')
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
    await call.message.answer(f"📈 Цена золота {selected_gold} пробы:\n"
                              f"{price_rub} ₽ за грамм\n"
                              f"{price_usd} $ за грамм\n"
                              f"Какая проба Вас интересует?\n",
                              reply_markup=new_keyboard(selected_gold))
