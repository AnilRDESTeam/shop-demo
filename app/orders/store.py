"""In-memory order store. Orders are kept as JSON-ready dicts."""

_orders: dict = {}
_counter = 0


def reset_orders() -> None:
    global _counter
    _orders.clear()
    _counter = 0


def next_order_id() -> str:
    """Sequential IDs: ORD-0001, ORD-0002, ..."""
    global _counter
    _counter += 1
    return f"ORD-{_counter:04d}"


def save_order(order: dict) -> None:
    _orders[order["order_id"]] = order


def find_order(order_id: str) -> dict | None:
    return _orders.get(order_id)


def list_orders(customer_id: str | None = None) -> list[dict]:
    orders = list(_orders.values())
    if customer_id:
        orders = [o for o in orders if o["customer_id"] == customer_id]
    return orders
