from lib.price_calculator import PriceHandler


def test_compact_price():
    handler1 = PriceHandler(category='compact', days=1, used_mileage=10)
    assert handler1.calculate() == 50

    handler2 = PriceHandler(category='compact', days=1, used_mileage=20)
    assert handler2.calculate() == 50


def test_premium_price():
    handler = PriceHandler(category='premium', days=1, used_mileage=10)
    assert handler.calculate() == 160


def test_minivan_price():
    handler = PriceHandler(category='minivan', days=1, used_mileage=10)
    assert handler.calculate() == 235
