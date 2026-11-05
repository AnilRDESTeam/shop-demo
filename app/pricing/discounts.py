"""Discount rule."""
from decimal import Decimal

from app.config import LOYALTY_DISCOUNT_RATE, LOYALTY_LABEL
from app.money import to_money


def calculate_discount(customer: dict, subtotal: Decimal) -> tuple[Decimal, str | None]:
    """Return (discount_amount, label).

    Registered customers with at least one previous order get the loyalty discount.
    New customers and guests get none.
    """
    if customer["type"] == "registered" and customer["order_count"] >= 1:
        return to_money(subtotal * LOYALTY_DISCOUNT_RATE), LOYALTY_LABEL
    return Decimal("0.00"), None
