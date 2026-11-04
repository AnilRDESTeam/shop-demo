from decimal import Decimal

import pytest

from app.pricing.quote import build_quote

CUSTOMER = {"id": "returning-customer-01", "type": "registered", "order_count": 3}


def test_line_totals_and_subtotal():
    q = build_quote(CUSTOMER, [{"sku": "MUG-001", "qty": 2}, {"sku": "NOTE-001", "qty": 1}])
    assert [line["line_total"] for line in q["items"]] == [Decimal("24.00"), Decimal("8.50")]
    assert q["subtotal"] == Decimal("32.50")


def test_total_formula_with_shipping():
    q = build_quote(CUSTOMER, [{"sku": "MUG-001", "qty": 1}])
    assert q["total"] == q["subtotal"] - q["discount"] + q["shipping"] == Decimal("17.99")


def test_rounding_pen_set_times_three():
    q = build_quote(CUSTOMER, [{"sku": "PEN-001", "qty": 3}])
    assert q["items"][0]["line_total"] == Decimal("14.97")


def test_rules_applied_standard_shipping():
    q = build_quote(CUSTOMER, [{"sku": "PEN-001", "qty": 1}])
    assert q["rules_applied"] == ["standard_shipping"]


def test_rules_applied_free_shipping():
    q = build_quote(CUSTOMER, [{"sku": "HOODIE-001", "qty": 1}, {"sku": "BAG-001", "qty": 1}, {"sku": "MUG-001", "qty": 1}])
    assert q["subtotal"] == Decimal("82.00")
    assert q["shipping"] == Decimal("0.00")
    assert q["rules_applied"] == ["free_shipping"]


def test_custom_price_sku_exact_threshold():
    q = build_quote(CUSTOMER, [{"sku": "TEST-SKU", "qty": 1, "unit_price": Decimal("75.00")}])
    assert q["shipping"] == Decimal("0.00")
    assert q["total"] == Decimal("75.00")


def test_unknown_sku_raises():
    with pytest.raises(KeyError):
        build_quote(CUSTOMER, [{"sku": "NOPE", "qty": 1}])
