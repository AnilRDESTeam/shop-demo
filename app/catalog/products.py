"""Product catalog, loaded once from the seed JSON file."""
import json
from decimal import Decimal
from pathlib import Path

_DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "products.json"


def _load() -> dict:
    with open(_DATA_FILE, encoding="utf-8") as f:
        rows = json.load(f)
    products = {}
    for row in rows:
        row["price"] = Decimal(row["price"])   # keep money as Decimal
        products[row["sku"]] = row
    return products


_PRODUCTS = _load()


def list_visible_products() -> list[dict]:
    """Hidden products (TEST-SKU) are never listed."""
    return [p for p in _PRODUCTS.values() if not p["hidden"]]


def find_product(sku: str) -> dict | None:
    """Find by exact SKU. Hidden products are found too."""
    return _PRODUCTS.get(sku)
