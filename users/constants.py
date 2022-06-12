BOOST_TYPE_NAME_TO_NUMBER = {
    'casual': 0,
    'auto': 1,
}

BOOST_TYPE_CHOICES = {
    (BOOST_TYPE_NAME_TO_NUMBER['casual'], 'casual'),
    (BOOST_TYPE_NAME_TO_NUMBER['auto'], 'auto'),
}

BOOST_TYPE_VALUES = {
    BOOST_TYPE_NAME_TO_NUMBER['casual']: {
        'click_power_scale': 1,
        'auto_click_power_scale': 0,
        'price_scale': 5,

    },
    BOOST_TYPE_NAME_TO_NUMBER['auto']: {
        'click_power_scale': 0,
        'auto_click_power_scale': 1,
        'price_scale': 25,
    },
}


BOOST_VALUES_NAME_TO_NUMBER = {
    'first': 1,
    'second': 2,
    'third': 3,
    'four': 4,
    'fifth': 5,
}
BOOST_VALUES_CHOICES = {
    (BOOST_VALUES_NAME_TO_NUMBER['first'], 'first'),
    (BOOST_VALUES_NAME_TO_NUMBER['second'], 'second'),
    (BOOST_VALUES_NAME_TO_NUMBER['third'], 'third'),
    (BOOST_VALUES_NAME_TO_NUMBER['four'], 'four'),
    (BOOST_VALUES_NAME_TO_NUMBER['fifth'], 'fifth'),
}

CASUAL_BOOSTS_VALUES = {
    BOOST_VALUES_NAME_TO_NUMBER['first']: {
        'boost_number': 1,
        'need_level': 2,
        'base_click_power': 1,
        'base_price': 13,
        'price_scale': 1.35,
    },
    BOOST_VALUES_NAME_TO_NUMBER['second']: {
        'boost_number': 2,
        'need_level': 3,
        'base_click_power': 8,
        'base_price': 100,
        'price_scale': 1.7,
    },
    BOOST_VALUES_NAME_TO_NUMBER['third']: {
        'boost_number': 3,
        'need_level': 4,
        'click_power_scale': 50,
        'base_price': 11000,
        'price_scale': 1.25,
    },
    BOOST_VALUES_NAME_TO_NUMBER['four']: {
        'boost_number': 4,
        'need_level': 5,
        'click_power_scale': 300,
        'base_price': 150000,
        'price_scale': 1.3,
    },
    BOOST_VALUES_NAME_TO_NUMBER['fifth']: {
        'boost_number': 5,
        'need_level': 6,
        'click_power_scale': 1500,
        'base_price': 1300000,
        'price_scale': 1.3,
    },
    6: {
        'click_power_scale': 32,
        'base_price': 10,
    },
    7: {
        'click_power_scale': 32,
        'base_price': 10,
    },
    8: {
        'click_power_scale': 32,
        'base_price': 10,
    },
    9: {
        'click_power_scale': 32,
        'base_price': 10,
    },
    10: {
        'click_power_scale': 32,
        'base_price': 10,
    },
}
