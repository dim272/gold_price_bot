import pytest

from parser import DataValidation, DataPipeline

datapipeline_cases = [
    ('1650.1', 'some_xpath', 'some_url', 1650.1),
    ('1650,44', 'some_xpath', 'some_url', 1650.44),
    ('1650', 'some_xpath', 'some_url', 1650.0),
    ('       1699        ', 'some_xpath', 'some_url', 1699.0),
    ('ahlfasl aslkdjsdkj 1711,31<<dsadh swi', 'some_xpath', 'some_url', 1711.31),
    ('ahlfasl\n1690,12<<dsadh swi', 'some_xpath', 'some_url', 1690.12),
    ('ahlfasl\n0090,12<<dsadh swi', 'some_xpath', 'some_url', None),
    ('16561', 'some_xpath', 'some_url', None),
    ('165', 'some_xpath', 'some_url', None),
    ('165,23', 'some_xpath', 'some_url', None),
    ('kmweflkem kfmlke kfem', 'some_xpath', 'some_url', None),
    ('kmw1777556,22kfmem', 'some_xpath', 'some_url', None),
    ('kmw1777.5,6kfmem', 'some_xpath', 'some_url', None),
    ('kmw1777556kfmem', 'some_xpath', 'some_url', None),
    ('kmw17772,22kfmem', 'some_xpath', 'some_url', None),
    ('', 'some_xpath', 'some_url', None),
    (None, 'some_xpath', 'some_url', None),
]


@pytest.mark.parametrize('value', datapipeline_cases)
def test_datapipeline(value: set):
    value, xpath, url, expected_value = value
    data_pipeline = DataPipeline()
    result = data_pipeline.clear_value(value=value, url=url, xpath=xpath)
    assert expected_value == result


datavalidation_cases = [
    {'usd_prices': [61.7, 61.65, 61.68],
     'gold_prices': [('1[USD]', 1655.4), ('2[USD]', 1645.8), ('3[USD]', 1670.2),
                     ('1[RUB]', 3320.2), ('2[RUB]', 3450.5)],
     'correct_values': (61.7, 1655.4)},

    {'usd_prices': [1, 61.65, 12],
     'gold_prices': [('1[USD]', 7.4), ('2[USD]', 1645.8), ('3[USD]', 1670.2),
                     ('1[RUB]', 3320.2), ('2[RUB]', 3450.5)],
     'correct_values': (61.65, 1645.8)},

    {'usd_prices': [1, 88.65, 61.65],
     'gold_prices': [('1[USD]', 7.4), ('2[USD]', 1645.8), ('3[USD]', 1670.2),
                     ('1[RUB]', 3320.2), ('2[RUB]', 3450.5)],
     'correct_values': (61.65, 1645.8)},

    {'usd_prices': [1, 88.65, 36.65],
     'gold_prices': [('1[USD]', 7.4), ('2[USD]', 9999.8), ('3[USD]', 1670.2),
                     ('1[RUB]', 3320.2), ('2[RUB]', 3120.5)],
     'correct_values': (None, 1670.2)},

    {'usd_prices': [None, 188.65, 36.65],
     'gold_prices': [('1[USD]', 1640.4), ('2[USD]', None), ('3[USD]', 0),
                     ('1[RUB]', 33.2), ('2[RUB]', 3120.5)],
     'correct_values': (None, 1640.4)},

    {'usd_prices': [61.65, 60.5, 36.65],
     'gold_prices': [('1[USD]', None), ('2[USD]', None), ('3[USD]', 0),
                     ('1[RUB]', 3300.2), ('2[RUB]', 3120.5)],
     'correct_values': (None, 0)},

    {'usd_prices': [61.65, 60.5, 36.65],
     'gold_prices': [('1[USD]', None), ('2[USD]', None), ('3[USD]', None),
                     ('1[RUB]', 3300.2), ('2[RUB]', 3120.5)],
     'correct_values': (None, None)},

    {'usd_prices': [61.65, 60.5, 36.65],
     'gold_prices': [('1[USD]', None), ('2[USD]', None), ('3[USD]', None),
                     ('1[RUB]', None), ('2[RUB]', None)],
     'correct_values': (61.65, None)},
]


@pytest.mark.parametrize('value', datavalidation_cases)
def test_datavalidation(value: dict):
    usd_prices = value.get('usd_prices')
    gold_prices = value.get('gold_prices')
    usd_price, gold_price = DataValidation(usd_prices=usd_prices, gold_prices=gold_prices).choose_valid_values()
    correct_usd, correct_gold = value.get('correct_values')
    assert usd_price == correct_usd
    assert gold_price == correct_gold
