from typing import Union

from settings import BASE_DAY_RENTAL, KILOMETER_PRICE, PREMIUM_BASE_DAY_COEFFICIENT, MINIVAN_BASE_DAY_COEFFICIENT, \
    MINIVAN_BASE_DISTANCE_COEFFICIENT


class PriceHandler:

    def __init__(self, category: str, days: int, used_mileage: float):
        self.category = category
        self.days = days
        self.used_mileage = used_mileage

    def calculate(self) -> Union[int, float]:
        return getattr(self, self.category.lower())()

    def compact(self) -> Union[int, float]:
        return BASE_DAY_RENTAL * self.days

    def premium(self) -> Union[int, float]:
        return BASE_DAY_RENTAL * self.days * PREMIUM_BASE_DAY_COEFFICIENT + \
               KILOMETER_PRICE * self.used_mileage

    def minivan(self) -> Union[int, float]:
        return BASE_DAY_RENTAL * self.days * MINIVAN_BASE_DAY_COEFFICIENT + \
               KILOMETER_PRICE * self.used_mileage * MINIVAN_BASE_DISTANCE_COEFFICIENT
