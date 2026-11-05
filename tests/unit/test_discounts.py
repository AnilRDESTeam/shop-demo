from decimal import Decimal

import pytest

from app.pricing.discounts import calculate_discount

NEW = {"id": "new-customer-01", "type": "registered", "order_count": 0}
RETURNING = {"id": "returning-customer-01", "type": "registered", "order_count": 3}
GUEST = {"id": "guest", "type": "guest", "order_count": 0}


def test_returning_customer_gets_loyalty_discount():
    assert calculate_discount(RETURNING, Decimal("40.00")) == (Decimal("2.00"), "Loyalty 5% off")


def test_customer_with_exactly_one_previous_order_gets_discount():
    customer = {**NEW, "order_count": 1}
    assert calculate_discount(customer, Decimal("40.00"))[0] == Decimal("2.00")


@pytest.mark.parametrize("subtotal, expected", [
    ("10.10", "0.51"),   # 0.505 rounds up
    ("33.30", "1.67"),   # 1.665 rounds up
    ("10.00", "0.50"),
])
def test_discount_rounds_half_up(subtotal, expected):
    assert calculate_discount(RETURNING, Decimal(subtotal))[0] == Decimal(expected)


@pytest.mark.parametrize("customer", [NEW, GUEST])
def test_no_loyalty_discount_for_new_customers_and_guests(customer):
    assert calculate_discount(customer, Decimal("100.00")) == (Decimal("0.00"), None)
