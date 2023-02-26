SIM_LENGTH = 50

INIT_POPS: int = 50
INIT_LABOUR_RATIO: float = 0.8
INIT_FUNDS_PER_POP: float = 10.00

EMPLOYMENT_RATE: float = 0.9
EQUILIBRIUM_CLEARANCE_RATE: float = 0.8
SAVINGS_RATE: float = 0.5
INVESTMENT_RATE: float = 0.75
DIVIDEND_RATE: float = 0.1

UNPROFITABLE_MONTH_LIMIT: int = 6

NUM_GOOD_TYPES: int = 3

TYPE_LABOUR: int = 0
TYPE_PRODUCE: int = 1
TYPE_SERVICES: int = 2

DICT_GOOD_TYPES = {
    TYPE_LABOUR: "Labour",
    TYPE_PRODUCE: "Produce",
    TYPE_SERVICES: "Services"
}

LABOUR_PER_POP: int = 10
DICT_INIT_AVG_PRICES = {
    TYPE_LABOUR: 1.00,
    TYPE_PRODUCE: 1.00,
    TYPE_SERVICES: 1.00
}
PP_PER_LABOUR = 5.0
LABOUR_SCALE_FACTOR = 12.0
CAPITAL_SCALE_FACTOR = 1.0

DICT_GOOD_PP_COST = {
    TYPE_LABOUR: -1.0,
    TYPE_PRODUCE: 0.5,
    TYPE_SERVICES: 0.5
}

PRICE_FLOOR = 0.1

INIT_PRICE_MAX_SPREAD = 0.1

DICT_PREFERENCE_MEAN = {
    TYPE_LABOUR: 0.0,
    TYPE_PRODUCE: 1.0,
    TYPE_SERVICES: 1.0
}

DICT_PREFERENCE_STD_DEV = {
    TYPE_LABOUR: 0.0,
    TYPE_PRODUCE: 0.1,
    TYPE_SERVICES: 0.1
}

DECISION_ID_INDEX = 0
DECISION_GOOD_TYPE_INDEX = 1
DECISION_FIRM_EXISTS_INDEX = 2
DECISION_PRICE_INDEX = 3