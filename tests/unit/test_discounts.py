from decimal import Decimal

import pytest

from app.pricing.discounts import calculate_discount

NEW = {"id": "new-customer-01", "type": "registered", "order_count": 0}


@pytest.mark.parametrize("customer", [
    {"id": "returning-customer-01", "type": "registered", "order_count": 3},
    {"id": "guest", "type": "guest", "order_count": 0},
])
def test_no_discount_for_returning_or_guest(customer):
    assert calculate_discount(customer, Decimal("100.00")) == (Decimal("0.00"), None)


def test_welcome_discount_for_new_registered_customer():
    assert calculate_discount(NEW, Decimal("100.00")) == (Decimal("10.00"), "Welcome 10%")


def test_welcome_discount_rounds_half_up_to_cent():
    # 10% of 24.95 = 2.495 -> 2.50
    assert calculate_discount(NEW, Decimal("24.95"))[0] == Decimal("2.50")
