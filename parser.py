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
    usd_quotes = list()

    def collect_values(self, value_type: str) -> None:
        urls, result_list = self._check_value_type(value_type=value_type)
        if not urls or not result_list:
            return None

        for source_name, source_info in urls:
            url, xpath = source_info
            r = self.get_request(url=url)
            value = self.get_value_from_request(req=r, xpath=xpath)
            result = DataPipeline(value=value, url=url, xpath=xpath)()
            if result:
                result_list.append((source_info, result))

        LOGGER.log(level=20, msg=f'{value_type} values was parsed. {len(result_list)}/{len(urls)} values collects')

    def _check_value_type(self, value_type: str) -> Optional[dict, list]:
        if value_type == 'Gold':
            urls = GOLD_URLS
            result_list = self.gold_prices
        elif value_type == 'USD':
            urls = USD_URLS
            result_list = self.usd_quotes
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
        result = tree.xpath(xpath)
        return result


class DataPipeline:
    """
    1. Clears string from all characters except numbers and commas
    2. Converts the cleared string to a float or return None
    """

    def __init__(self, value: str, url: str, xpath: str,):
        self.value = value
        self.url = url
        self.xpath = xpath

    def __call__(self,  *args, **kwargs):
        result_str = self.collect_numbers(self.value)
        result_float = self.convert_to_float(value=result_str, source_url=self.url, xpath=self.xpath)
        return result_float

    def collect_numbers(self, value: str) -> Optional[str]:
        if not value:
            return None

        result = value
        for x in value:
            if not x.isdigit():
                if x in [',', '.']:
                    result.replace(',', '.')
                else:
                    result.replace(x, '')
        return result

    def convert_to_float(self, value: str, source_url: str, xpath: str) -> Optional[float]:
        error_text = "convert_to_float error:"

        if not value:
            LOGGER.log(level=40, msg=f'{error_text} value not found :: url = {source_url} :: xpath = {xpath}')
            return None

        if len(value) > 7:
            LOGGER.log(level=40, msg=f'{error_text} value is very long :: value = {value} :: url = {source_url}')
            return None

        if value.count(',') > 1 or not value.replace('.','').isdigit():
            LOGGER.log(level=40, msg=f'{error_text} value is incorrect :: value = {value} :: url = {source_url}')
            return None

        try:
            value = float(value)
        except ValueError as e:
            LOGGER.log(level=40, msg=f'{error_text} {e} :: {value} :: {source_url}')
            return None
        else:
            return value


class DataValidation:
    """ Determines a valid value from the list by comparing with other values """
    pass
