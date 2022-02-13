from datetime import date, datetime
from data import value_db


class Text:
    def __init__(self, probe, db_unit):
        self.__probe = probe
        self.__unit = db_unit

    def get_message(self):
        today = datetime.today()
        day_of_week = date.weekday(today)
        usd = value_db.read_value_db('usd')
        price_rub = round(value_db.read_value_db(self.__unit))
        price_usd = round((price_rub / usd), 2)

        if day_of_week == 5:
            message = (f"📈 Цена золота {self.__probe} пробы:\n"
                       f"{price_rub} ₽ за грамм\n"
                       f"{price_usd} $ за грамм\n"
                       f"Сегодня суббота, биржа закрыта\n"
                       f"Цены будут обновлены в понедельник")
        elif day_of_week == 6:
            message = (f"📈 Цена золота {self.__probe} пробы:\n"
                       f"{price_rub} ₽ за грамм\n"
                       f"{price_usd} $ за грамм\n"
                       f"Сегодня воскресенье, биржа закрыта\n"
                       f"Цены будут обновлены в понедельник")
        else:
            message = (f"📈 Цена золота {self.__probe} пробы:\n"
                       f"{price_rub} ₽ за грамм\n"
                       f"{price_usd} $ за грамм")

        return message
