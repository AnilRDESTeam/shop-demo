"""Money helpers. Money is always Decimal inside Python; floats only at the API edge."""
from decimal import Decimal, ROUND_HALF_UP

CENT = Decimal("0.01")


def to_money(value) -> Decimal:
    """Convert anything number-like to a Decimal rounded to 2 places (half up)."""
    # str() first so floats like 0.1 do not bring binary rounding noise
    return Decimal(str(value)).quantize(CENT, rounding=ROUND_HALF_UP)


def money_to_float(value: Decimal) -> float:
    """Turn a Decimal into a JSON number, e.g. Decimal('57.00') -> 57.0."""
    return float(value)
