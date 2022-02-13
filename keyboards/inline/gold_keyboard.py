from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

CHOICE_SIGN = '🟡 '


def new_keyboard(active_button):
    GOLD_LIST = ['333', '375', '500', '585', '750', '850', '900', '958', '999']
    val_index = GOLD_LIST.index(active_button)
    GOLD_LIST[val_index] = CHOICE_SIGN + GOLD_LIST[val_index]

    keyboard = InlineKeyboardMarkup(

        inline_keyboard=[
            [
                InlineKeyboardButton(text=GOLD_LIST[0], callback_data='select:gold:gr_333_rub:333'),
                InlineKeyboardButton(text=GOLD_LIST[1], callback_data='select:gold:gr_375_rub:375'),
                InlineKeyboardButton(text=GOLD_LIST[2], callback_data='select:gold:gr_500_rub:500'),
            ],
            [
                InlineKeyboardButton(text=GOLD_LIST[3], callback_data='select:gold:gr_585_rub:585'),
                InlineKeyboardButton(text=GOLD_LIST[4], callback_data='select:gold:gr_750_rub:750'),
                InlineKeyboardButton(text=GOLD_LIST[5], callback_data='select:gold:gr_850_rub:850'),
            ],
            [
                InlineKeyboardButton(text=GOLD_LIST[6], callback_data='select:gold:gr_900_rub:900'),
                InlineKeyboardButton(text=GOLD_LIST[7], callback_data='select:gold:gr_958_rub:958'),
                InlineKeyboardButton(text=GOLD_LIST[8], callback_data='select:gold:gr_999_rub:999'), ]])

    return keyboard
