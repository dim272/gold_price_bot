import aiohttp
import asyncio
import random
from typing import Optional

from lxml import html

from config.settings import GOLD_URLS, USD_URLS, USER_AGENTS
from utils.data_utils import DataPipeline, GoldValidation, LOGGER


class Parser:
    """ Returns the price of one OZ of gold in US dollars and the quote USD/RUB """
    gold_prices = list()
    usd_prices = list()

    def parse_values(self):
        # returns usd_price, gold_price
        for value_type in ['Gold', 'USD']:
            urls, result_list = self._check_value_type(value_type=value_type)
            asyncio.run(self.collect_values(urls=urls, result_list=result_list))
            LOGGER.log(level=30, msg=f'{value_type} values was parsed. {len(result_list)}/{len(urls)} values collects')

        if len(self.gold_prices) > 0 and len(self.usd_prices) > 0:
            return GoldValidation(usd_prices=self.usd_prices, gold_prices=self.gold_prices).get_valid_values()
        return None, None

    async def collect_values(self, urls: Optional[dict], result_list: list) -> None:
        if not urls or result_list is None:
            return None

        data_pipe = DataPipeline()

        async with aiohttp.ClientSession() as session:
            for source_name, source_info in urls.items():
                url, xpath = source_info
                async with session.get(url=url, headers={'User-Agent': random.choice(USER_AGENTS)}) as r:
                    value = await self._get_value_from_request(req=r, xpath=xpath)
                    result = data_pipe.clear_value(value=value, url=url, xpath=xpath)
                    if result:
                        result_list.append((source_name, result))

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

    async def _get_value_from_request(self, req: aiohttp.ClientSession.request, xpath: str) -> Optional[str]:
        tree = html.fromstring(await req.text())
        return tree.xpath(xpath)
