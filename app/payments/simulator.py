"""Payment SIMULATOR (HIGH-RISK area: payments).

THIS IS A SIMULATION. It never contacts a payment provider, never touches the
network and never handles card data. It only returns a fake reference number.
"""
from decimal import Decimal


def simulate_payment(order_id: str, total: Decimal) -> dict:
    """Pretend to charge `total` for `order_id`; always succeeds."""
    # ORD-0007 -> SIM-0007, so the reference is easy to match with the order
    number = order_id.split("-")[1]
    return {"status": "simulated", "reference": f"SIM-{number}"}
