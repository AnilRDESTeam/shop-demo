"""Constants and environment settings. All pricing constants live here."""
import os
from decimal import Decimal

APP_NAME = "shop-demo"
APP_VERSION = "1.0.0"

FREE_SHIPPING_THRESHOLD = Decimal("50.00")   # orders at or above this ship free
STANDARD_SHIPPING_FEE = Decimal("5.99")
WELCOME_DISCOUNT_RATE = Decimal("0.10")   # first-order discount for registered customers
WELCOME_DISCOUNT_LABEL = "Welcome 10%"
CURRENCY = "USD"
MAX_QTY_PER_LINE = 10
MAX_LINES_PER_CART = 20
MAX_CUSTOM_PRICE = Decimal("10000")
CUSTOM_PRICE_SKU = "TEST-SKU"   # the only SKU that accepts a custom unit_price


def get_mode() -> str:
    """Read APP_MODE on every call so tests can change it with monkeypatch."""
    return os.environ.get("APP_MODE", "test")


def get_port() -> int:
    return int(os.environ.get("PORT", "8080"))
