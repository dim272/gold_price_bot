import random
import logging
from typing import Optional

import requests
from lxml import html

from config.settings import GOLD_URLS, USD_URLS, USER_AGENTS

LOGGER = logging.getLogger(__name__)


class Parser:
    """ Returns the price of one OZ of gold in US dollars and the quote USD/RUB """
    gold_prices = list()
    usd_prices = list()

    def parse_values(self):
        # returns usd_price, gold_price
        for value_type in ['Gold', 'USD']:
            self.collect_values(value_type=value_type)

        if len(self.gold_prices) > 0 and len(self.usd_prices) > 0:
            return GoldValidation(usd_prices=self.usd_prices, gold_prices=self.gold_prices).get_valid_values()
        return None, None

    def collect_values(self, value_type: str) -> None:
        urls, result_list = self._check_value_type(value_type=value_type)
        if not urls or not result_list:
            return None

        data_pipe = DataPipeline()
        for source_name, source_info in urls:
            url, xpath = source_info
            r = self.get_request(url=url)
            value = self.get_value_from_request(req=r, xpath=xpath)
            result = data_pipe.clear_value(value=value, url=url, xpath=xpath)
            if result:
                result_list.append((source_info, result))

        LOGGER.log(level=20, msg=f'{value_type} values was parsed. {len(result_list)}/{len(urls)} values collects')

    def _check_value_type(self, value_type: str):
        if value_type == 'Gold':
            urls = GOLD_URLS
            result_list = self.gold_prices
        elif value_type == 'USD':
            urls = USD_URLS
            result_list = self.usd_prices
        else:
            LOGGER.log(level=40, msg=f'Value type error :: {value_type}')
            return None
        return urls, result_list

    def get_request(self, url: str) -> requests.Response:
        headers = {'User-Agent': random.choice(USER_AGENTS)}
        r = requests.get(url=url, headers=headers)
        return r

    def get_value_from_request(self, req: requests.Response, xpath: str) -> Optional[str]:
        tree = html.fromstring(req.content)
        return tree.xpath(xpath)


class DataPipeline:
    """
    1. Clears string from all characters except numbers and commas
    2. Converts the cleared string to a float or return None
    """

    def clear_value(self,  value: str, url: str = None, xpath: str = None):
        result_str = self.collect_numbers(value)
        return self.convert_to_float(value=result_str, source_url=url, xpath=xpath)

    def collect_numbers(self, value: str) -> Optional[str]:
        if not value:
            return None

        result = value
        for x in value:
            if not x.isdigit():
                if x in [',', '.']:
                    result = result.replace(',', '.')
                else:
                    result = result.replace(x, '')
        return result

    def convert_to_float(self, value: str, source_url: str, xpath: str) -> Optional[float]:
        error_text = "convert_to_float error:"

        if not value:
            LOGGER.log(level=40, msg=f'{error_text} value not found :: url = {source_url} :: xpath = {xpath}')
            return None

        if len(value.replace('.','')) > 6:
            LOGGER.log(level=40, msg=f'{error_text} value is very long :: value = {value} :: url = {source_url}')
            return None

        if value.count(',') > 1 or not value.replace('.','').isdigit():
            LOGGER.log(level=40, msg=f'{error_text} value is incorrect :: value = {value} :: url = {source_url}')
            return None

        try:
            value = float(value)
            if len(str(int(value))) != 4:
                value = None
        except ValueError as e:
            LOGGER.log(level=40, msg=f'{error_text} {e} :: {value} :: {source_url}')
            return None
        else:
            return value


class DataValidation:
    """ Sorts gold USD and RUB prices """

    def __init__(self, usd_prices: list, gold_prices: list):
        self.usd_prices = usd_prices
        self.gold = gold_prices
        self.gold_rub, self.gold_usd = self._sort_gold_prices()

    def _gold_prices_are_correct(self) -> bool:
        for prices in [self.gold_usd, self.gold_rub]:
            if [price for price in prices if price]:
                return True

    def _sort_gold_prices(self):
        gold_rub = list()
        gold_usd = list()
        for item in self.gold:
            source_name, value = item
            if '[USD]' in source_name:
                gold_usd.append(value)
            elif '[RUB]' in source_name:
                gold_rub.append(value)
            else:
                LOGGER.log(level=40, msg=f'Incorrect source name :: {source_name} :: {value}')
        return gold_rub, gold_usd


class USDValidation(DataValidation):
    """ Gets valid usd price """

    def __init__(self, usd_prices: list, gold_prices: list):
        super().__init__(usd_prices=usd_prices, gold_prices=gold_prices)
        self.usd_price = self._get_usd_price()

    def _get_usd_price(self) -> Optional[float]:
        if self._gold_prices_are_correct():
            price_top = self._get_top_usd_prices()
            if price_top:
                return self._get_top_price(top_price_dict=price_top)
            return None
        return self.usd_prices[0]

    def _get_top_usd_prices(self) -> Optional[dict]:
        price_top = {}
        for usd_price in self.usd_prices:
            if usd_price is None:
                continue
            price_point = self._check_usd_rub_prices(gold_usd=self.gold_usd, gold_rub=self.gold_rub,
                                                     usd_price=usd_price)
            if price_point > 0:
                if price_top.get(str(usd_price)):
                    price_top[str(usd_price)] = price_top[str(usd_price)] + price_point
                else:
                    price_top.update({str(usd_price): price_point})
        return price_top

    def _get_top_price(self, top_price_dict: dict) -> Optional[float]:
        try:
            result = sorted(top_price_dict.items(), reverse=True, key=lambda x: x[1])[0][0]
            return float(result)
        except [ValueError, TypeError, IndexError]:
            return None

    def _check_usd_rub_prices(self, gold_usd: list, gold_rub: list, usd_price: float) -> int:
        quote_point = 0
        for usd_gold_price in gold_usd:
            for rub_gold_price in gold_rub:
                if usd_gold_price is None or rub_gold_price is None:
                    continue
                if self._is_usd_price_correct(usd_price=usd_price, usd_gold_price=usd_gold_price,
                                              rub_gold_price=rub_gold_price):
                    quote_point += 1
        return quote_point

    def _is_usd_price_correct(self, usd_price: float, usd_gold_price: float, rub_gold_price: float) -> bool:
        difference = self._get_difference(num1=((usd_price * usd_gold_price) / 31.1), num2=rub_gold_price)
        if difference < rub_gold_price * 0.25:
            return True

    @staticmethod
    def _get_difference(num1, num2):
        if num2 > num1:
            num1, num2 = num2, num1
        return num1 - num2


class GoldValidation(USDValidation):
    """ Process valid gold price and get two correct values: USD price and Gold Price """

    def __init__(self, usd_prices: list, gold_prices: list):
        super().__init__(usd_prices=usd_prices, gold_prices=gold_prices)
        self.gold_price = self._get_gold_price()

    def get_valid_values(self) -> tuple[Optional[float], Optional[float]]:
        return self.usd_price, self.gold_price

    def _get_gold_price(self) -> Optional[float]:
        gold_usd_copy = [price for price in self.gold_usd if price is not None]
        if len(gold_usd_copy) > 2:
            mean = sum(gold_usd_copy) / len(gold_usd_copy)
            difference = self._get_difference(num1=mean, num2=gold_usd_copy[0])
            if difference > gold_usd_copy[0] * 0.025:
                self._exclude_gold_price_anomaly(gold_usd=gold_usd_copy)
            return gold_usd_copy[0]
        elif len(gold_usd_copy) == 2:
            if self.usd_price is None:
                return gold_usd_copy[0]
            return self._choose_usd_gold_price_by_rub_prices(usd_price=self.usd_price)
        elif len(gold_usd_copy) == 1:
            return gold_usd_copy[0]
        else:
            return None

    def _choose_usd_gold_price_by_rub_prices(self, usd_price: float) -> Optional[float]:
        gold_usd_copy = [price for price in self.gold_usd if price is not None]
        if len(gold_usd_copy) > 0:
            for usd_gold_price in gold_usd_copy:
                price_point = self._check_usd_rub_prices(gold_usd=gold_usd_copy, gold_rub=self.gold_rub,
                                                         usd_price=usd_price)
                if price_point > 0:
                    return usd_gold_price
        return None

    def _exclude_gold_price_anomaly(self, gold_usd: list[float]) -> None:
        def is_num1_anomaly(num1: float, num2: float) -> bool:
            difference = self._get_difference(num1=num1, num2=num2)
            if difference > num1 * 0.025:
                return True

        def found_next_check_num(ind: int):
            if ind + 2 <= len(gold_usd):
                return gold_usd[index + 2]
            elif ind - 1 >= 0:
                return gold_usd[index - 1]

        gold_usd_copy = gold_usd.copy()
        for index, price in enumerate(gold_usd_copy):
            if index+1 == len(gold_usd_copy):
                break

            if is_num1_anomaly(num1=price, num2=gold_usd_copy[index+1]):
                next_num = found_next_check_num(ind=index)
                if is_num1_anomaly(num1=price, num2=next_num):
                    anomaly = price
                else:
                    anomaly = next_num
                gold_usd.remove(anomaly)
