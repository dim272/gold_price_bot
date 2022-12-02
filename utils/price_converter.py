from typing import Optional

from utils.data_utils import LOGGER


class PriceConverter:

    def __init__(self, usd: float, gold: float):
        self.usd = usd
        self.gold = gold

    def _get_gr_usd(self) -> float:
        # 1 gram 999 in USD
        return round(float(self.gold / 31.1), 2)

    def _get_gr_rub(self) -> int:
        # 1 gram 999 in RUB
        return int((self.gold * self.usd) / 31.1)

    def _convert_prices(self, _999_rub) -> Optional[dict]:
        result = {}
        probes = [958, 900, 850, 750, 585, 500, 375, 333]
        for probe in probes:
            try:
                price = round(_999_rub / 1000 * probe, 2)
            except:
                continue
            result[f'gr_{probe}_rub'] = price

        if len(result) != len(probes):
            LOGGER.log(40, f'A gold probe was missed during _convert_prices :: {result}')

        return result

    def convert(self) -> Optional[dict]:
        gr_999_rub = self._get_gr_rub()

        data_massive = {
            'usd': self.usd,
            'oz_usd': self.gold,
            'gr_999_usd': self._get_gr_usd(),
            'gr_999_rub': gr_999_rub,
            **self._convert_prices(_999_rub=gr_999_rub)
        }
        return data_massive
