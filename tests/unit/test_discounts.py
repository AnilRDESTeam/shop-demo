from decimal import Decimal

import pytest

from app.pricing.discounts import calculate_discount


@pytest.mark.parametrize("customer", [
    {"id": "new-customer-01", "type": "registered", "order_count": 0},
    {"id": "returning-customer-01", "type": "registered", "order_count": 3},
    {"id": "guest", "type": "guest", "order_count": 0},
])
def test_baseline_has_no_discount(customer):
    assert calculate_discount(customer, Decimal("100.00")) == (Decimal("0.00"), None)
