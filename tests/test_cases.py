datapipeline_cases = [
    ('1650.1', 'some_xpath', 'some_url', 1650.1),
    ('1650,44', 'some_xpath', 'some_url', 1650.44),
    ('1650', 'some_xpath', 'some_url', 1650.0),
    ('       1699        ', 'some_xpath', 'some_url', 1699.0),
    ('ahlfasl aslkdjsdkj 1711,31<<dsadh swi', 'some_xpath', 'some_url', 1711.31),
    ('ahlfasl\n1690,12<<dsadh swi', 'some_xpath', 'some_url', 1690.12),
    ('ahlfasl\n0090,12<<dsadh swi', 'some_xpath', 'some_url', 90.12),
    ('16561', 'some_xpath', 'some_url', None),
    ('165', 'some_xpath', 'some_url', 165),
    ('165,23', 'some_xpath', 'some_url', 165.23),
    ('kmweflkem kfmlke kfem', 'some_xpath', 'some_url', None),
    ('kmw1777556,22kfmem', 'some_xpath', 'some_url', None),
    ('kmw1777.5,6kfmem', 'some_xpath', 'some_url', None),
    ('kmw1777556kfmem', 'some_xpath', 'some_url', None),
    ('kmw17772,22kfmem', 'some_xpath', 'some_url', None),
    ('', 'some_xpath', 'some_url', None),
    (None, 'some_xpath', 'some_url', None),
]

datavalidation_cases = [
    {'usd_prices': [('1', 61.7), ('2', 61.65), ('3', 61.68)],
     'gold_prices': [('1[USD]', 1655.4), ('2[USD]', 1645.8), ('3[USD]', 1670.2),
                     ('1[RUB]', 3320.2), ('2[RUB]', 3450.5)],
     'correct_values': (61.7, 1655.4)},

    {'usd_prices': [('1', 1), ('2', 61.65), ('3', 12)],
     'gold_prices': [('1[USD]', 7.4), ('2[USD]', 1645.8), ('3[USD]', 1670.2),
                     ('1[RUB]', 3320.2), ('2[RUB]', 3450.5)],
     'correct_values': (61.65, 1645.8)},

    {'usd_prices': [('1', 1), ('2', 88.65), ('3', 61.65)],
     'gold_prices': [('1[USD]', 7.4), ('2[USD]', 1645.8), ('3[USD]', 1670.2),
                     ('1[RUB]', 3320.2), ('2[RUB]', 3450.5)],
     'correct_values': (61.65, 1645.8)},

    {'usd_prices': [('1', 1), ('2', 88.65), ('3', 36.65)],
     'gold_prices': [('1[USD]', 7.4), ('2[USD]', 9999.8), ('3[USD]', 1670.2),
                     ('1[RUB]', 3320.2), ('2[RUB]', 3120.5)],
     'correct_values': (None, 1670.2)},

    {'usd_prices': [('1', None), ('2', 188.65), ('3', 36.65)],
     'gold_prices': [('1[USD]', 1640.4), ('2[USD]', None), ('3[USD]', 0),
                     ('1[RUB]', 33.2), ('2[RUB]', 3120.5)],
     'correct_values': (None, 1640.4)},

    {'usd_prices': [('1', 61.65), ('2', 60.65), ('3', 36.65)],
     'gold_prices': [('1[USD]', None), ('2[USD]', None), ('3[USD]', 0),
                     ('1[RUB]', 3300.2), ('2[RUB]', 3120.5)],
     'correct_values': (None, 0)},

    {'usd_prices': [('1', 61.65), ('2', 60.5), ('3', 36.65)],
     'gold_prices': [('1[USD]', None), ('2[USD]', None), ('3[USD]', None),
                     ('1[RUB]', 3300.2), ('2[RUB]', 3120.5)],
     'correct_values': (None, None)},

    {'usd_prices': [('1', 61.65), ('2', 60.5), ('3', 36.65)],
     'gold_prices': [('1[USD]', None), ('2[USD]', None), ('3[USD]', None),
                     ('1[RUB]', None), ('2[RUB]', None)],
     'correct_values': (61.65, None)},
]

gr_usd_cases = [
    ((61.77, 1775.5), 57.09)
]

gr_rub_cases = [
    ((61.77, 1775.5), 3526)
]

convert_prices_cases = [
    (
        (61.77, 1775.5),
        {
            'gr_958_rub': 3377.91,
            'gr_900_rub': 3173.4,
            'gr_850_rub': 2997.1,
            'gr_750_rub': 2644.5,
            'gr_585_rub': 2062.71,
            'gr_500_rub': 1763.0,
            'gr_375_rub': 1322.25,
            'gr_333_rub': 1174.16,
        }
    )
]

convert_cases = [
    (
        (61.77, 1775.5),
        {
            'usd': 61.77,
            'oz_usd': 1775.5,
            'gr_999_usd': 57.09,
            'gr_999_rub': 3526,
            'gr_958_rub': 3377.91,
            'gr_900_rub': 3173.4,
            'gr_850_rub': 2997.1,
            'gr_750_rub': 2644.5,
            'gr_585_rub': 2062.71,
            'gr_500_rub': 1763.0,
            'gr_375_rub': 1322.25,
            'gr_333_rub': 1174.16,
        }
    )
]
