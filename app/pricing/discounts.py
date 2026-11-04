"""Discount rule."""
from decimal import Decimal

from app.config import WELCOME_DISCOUNT_LABEL, WELCOME_DISCOUNT_RATE
from app.money import to_money


def calculate_discount(customer: dict, subtotal: Decimal) -> tuple[Decimal, str | None]:
    """Return (discount_amount, label). Registered customers with no orders get 10% off."""
    if customer["type"] == "registered" and customer["order_count"] == 0:
        return to_money(subtotal * WELCOME_DISCOUNT_RATE), WELCOME_DISCOUNT_LABEL
    return Decimal("0.00"), None
