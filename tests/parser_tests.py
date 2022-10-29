import pytest

from tests import test_cases
from parser import GoldValidation, DataPipeline


@pytest.mark.parametrize('value', test_cases.datapipeline_cases)
def test_datapipeline(value: set):
    value, xpath, url, expected_value = value
    data_pipeline = DataPipeline()
    result = data_pipeline.clear_value(value=value, url=url, xpath=xpath)
    assert expected_value == result


@pytest.mark.parametrize('value', test_cases.datavalidation_cases)
def test_datavalidation(value: dict):
    usd_prices = value.get('usd_prices')
    gold_prices = value.get('gold_prices')
    usd_price, gold_price = GoldValidation(usd_prices=usd_prices, gold_prices=gold_prices).get_valid_values()
    correct_usd, correct_gold = value.get('correct_values')
    assert usd_price == correct_usd
    assert gold_price == correct_gold
