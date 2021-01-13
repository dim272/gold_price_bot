from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

gold_choice = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='333 (9K)', callback_data='select:gold:333'),
            InlineKeyboardButton(text='375 (10K)', callback_data='select:gold:375'),
            InlineKeyboardButton(text='500 (12K)', callback_data='select:gold:500'),
        ],
        [
            InlineKeyboardButton(text='585 (14K)', callback_data='select:gold:585'),
            InlineKeyboardButton(text='750 (18K)', callback_data='select:gold:750'),
            InlineKeyboardButton(text='850 (20K)', callback_data='select:gold:850'),
        ],
        [
            InlineKeyboardButton(text='900 (21K)', callback_data='select:gold:900'),
            InlineKeyboardButton(text='958 (22K)', callback_data='select:gold:958'),
            InlineKeyboardButton(text='999 (24K)', callback_data='select:gold:999'),
        ]
    ]
)
