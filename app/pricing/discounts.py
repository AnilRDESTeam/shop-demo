"""Discount rule."""
from decimal import Decimal


def calculate_discount(customer: dict, subtotal: Decimal) -> tuple[Decimal, str | None]:
    """Return (discount_amount, label). The baseline shop has no promotions."""
    return Decimal("0.00"), None
