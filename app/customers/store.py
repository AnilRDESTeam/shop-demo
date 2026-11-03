"""In-memory customer store (HIGH-RISK area: customer data). Fake data only."""
import copy
import json
from pathlib import Path

_DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "customers.json"

_customers: dict = {}


def reset_customers() -> None:
    """Restore customers (including order_count) to the seed file."""
    with open(_DATA_FILE, encoding="utf-8") as f:
        rows = json.load(f)
    _customers.clear()
    for row in rows:
        _customers[row["id"]] = copy.deepcopy(row)


def list_customers() -> list[dict]:
    return list(_customers.values())


def find_customer(customer_id: str) -> dict | None:
    return _customers.get(customer_id)


def increment_order_count(customer_id: str) -> None:
    """Registered customers get +1 per order. Guests are not counted."""
    customer = _customers[customer_id]
    if customer["type"] == "registered":
        customer["order_count"] += 1


reset_customers()
