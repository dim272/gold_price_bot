import pytest

from tests import test_cases

from utils.price_converter import PriceConverter


class TestDataConverter:

    # TODO: more cases

    @pytest.mark.parametrize('value', test_cases.gr_usd_cases)
    def test_get_gr_usd(self, value):
        values, expected_value = value
        usd, gold = values
        converter = PriceConverter(usd=usd, gold=gold)
        result = converter._get_gr_usd()
        assert expected_value == result

    @pytest.mark.parametrize('value', test_cases.gr_rub_cases)
    def test_get_gr_rub(self, value):
        values, expected_value = value
        usd, gold = values
        converter = PriceConverter(usd=usd, gold=gold)
        result = converter._get_gr_rub()
        assert expected_value == result

    @pytest.mark.parametrize('value', test_cases.convert_prices_cases)
    def test_convert_prices(self, value):
        values, expected_value = value
        usd, gold = values
        converter = PriceConverter(usd=usd, gold=gold)
        _999 = converter._get_gr_rub()
        result = converter._convert_prices(_999_rub=_999)
        assert expected_value == result

    @pytest.mark.parametrize('value', test_cases.convert_cases)
    def test_convert(self, value):
        values, expected_value = value
        usd, gold = values
        converter = PriceConverter(usd=usd, gold=gold)
        result = converter.convert()
        assert expected_value == result
