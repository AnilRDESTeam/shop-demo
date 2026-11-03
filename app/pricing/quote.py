"""Builds the full price breakdown for a cart. No JSON or HTTP in here."""
from decimal import Decimal

from app.catalog.products import find_product
from app.config import CURRENCY
from app.money import to_money
from app.pricing.discounts import calculate_discount
from app.pricing.shipping import calculate_shipping


def build_quote(customer: dict, items: list[dict]) -> dict:
    """items: [{"sku", "qty", "unit_price" (only for custom-price SKUs)}].

    Returns amounts as Decimal; the API layer converts them to numbers.
    Raises KeyError(sku) if a SKU does not exist.
    """
    lines = []
    subtotal = Decimal("0.00")
    for item in items:
        product = find_product(item["sku"])
        if product is None:
            raise KeyError(item["sku"])
        unit_price = to_money(item.get("unit_price") or product["price"])
        line_total = to_money(unit_price * item["qty"])
        subtotal += line_total
        lines.append({
            "sku": product["sku"],
            "name": product["name"],
            "unit_price": unit_price,
            "qty": item["qty"],
            "line_total": line_total,
        })

    discount, label = calculate_discount(customer, subtotal)
    shipping = calculate_shipping(subtotal)
    total = to_money(subtotal - discount + shipping)

    return {
        "customer_id": customer["id"],
        "items": lines,
        "subtotal": subtotal,
        "discount": discount,
        "discount_label": label,
        "shipping": shipping,
        "total": total,
        "currency": CURRENCY,
        "rules_applied": ["free_shipping"] if shipping == 0 else ["standard_shipping"],
    }
