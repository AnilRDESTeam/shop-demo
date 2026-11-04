from decimal import Decimal

import pytest

from app.pricing.shipping import calculate_shipping


@pytest.mark.parametrize("subtotal, expected", [
    ("0.01", "5.99"),
    ("49.99", "5.99"),
    ("50.00", "0.00"),
    ("74.99", "0.00"),
    ("75.00", "0.00"),
    ("75.01", "0.00"),
    ("120.00", "0.00"),
])
def test_shipping_threshold(subtotal, expected):
    assert calculate_shipping(Decimal(subtotal)) == Decimal(expected)
