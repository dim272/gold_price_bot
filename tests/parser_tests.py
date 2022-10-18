import pytest

from parser import  DataValidation

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
]


class TestDataValidation:
    @pytest.mark.parametrize('value', datavalidation_cases)
    def test_case(self, value: dict):
        usd_prices = value.get('usd_prices')
        gold_prices = value.get('gold_prices')
        usd_price, gold_price = DataValidation(usd_prices=usd_prices, gold_prices=gold_prices).choose_valid_values()
        correct_usd, correct_gold = value.get('correct_values')
        assert usd_price == correct_usd
        assert gold_price == correct_gold
