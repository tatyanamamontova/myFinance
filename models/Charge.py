from decimal import Decimal
from datetime import date


class Charge(object):

    def __init__(self, value, date_charge):
        self.value = Decimal(value)
        self.date = date(date_charge)
