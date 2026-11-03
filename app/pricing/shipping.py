"""Shipping rule. The free-shipping threshold is checked here and nowhere else."""
from decimal import Decimal

from app.config import FREE_SHIPPING_THRESHOLD, STANDARD_SHIPPING_FEE


def calculate_shipping(subtotal: Decimal) -> Decimal:
    """Orders at or above the threshold ship free; others pay the standard fee."""
    if subtotal >= FREE_SHIPPING_THRESHOLD:
        return Decimal("0.00")
    return STANDARD_SHIPPING_FEE
