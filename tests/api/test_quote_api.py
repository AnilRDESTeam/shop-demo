import pytest

RETURNING = "returning-customer-01"


def quote(client, items, customer=RETURNING):
    return client.post("/api/cart/quote", json={"customer_id": customer, "items": items})


def test_normal_quote(client):
    r = quote(client, [{"sku": "MUG-001", "qty": 2}])
    assert r.status_code == 200
    assert r.json() == {
        "customer_id": RETURNING,
        "items": [{"sku": "MUG-001", "name": "Coffee Mug", "unit_price": 12.0,
                   "qty": 2, "line_total": 24.0}],
        "subtotal": 24.0, "discount": 0.0, "discount_label": None,
        "shipping": 5.99, "total": 29.99, "currency": "USD",
        "rules_applied": ["standard_shipping"],
    }


def test_test_sku_at_threshold_ships_free(client):
    body = quote(client, [{"sku": "TEST-SKU", "qty": 1, "unit_price": 75.00}]).json()
    assert body["shipping"] == 0.0
    assert body["total"] == 75.0
    assert body["rules_applied"] == ["free_shipping"]


def test_test_sku_just_below_threshold_pays_shipping(client):
    body = quote(client, [{"sku": "TEST-SKU", "qty": 1, "unit_price": 74.99}]).json()
    assert body["shipping"] == 5.99
    assert body["total"] == 80.98


def test_discount_fields_are_empty(client):
    body = quote(client, [{"sku": "HOODIE-001", "qty": 1}], customer="new-customer-01").json()
    assert body["discount"] == 0.0
    assert body["discount_label"] is None


def test_unknown_sku_404(client):
    r = quote(client, [{"sku": "XYZ", "qty": 1}])
    assert r.status_code == 404
    assert r.json()["error"] == {"code": "UNKNOWN_SKU",
                                 "message": "Product 'XYZ' does not exist", "details": []}


@pytest.mark.parametrize("qty", [0, 11])
def test_qty_out_of_range_422(client, qty):
    r = quote(client, [{"sku": "MUG-001", "qty": qty}])
    assert r.status_code == 422
    assert r.json()["error"]["code"] == "VALIDATION_ERROR"


def test_unit_price_on_normal_sku_422(client):
    assert quote(client, [{"sku": "MUG-001", "qty": 1, "unit_price": 1.00}]).status_code == 422


def test_test_sku_without_price_422(client):
    assert quote(client, [{"sku": "TEST-SKU", "qty": 1}]).status_code == 422


@pytest.mark.parametrize("price", [0, -5, 10000.01, 1.234])
def test_bad_custom_price_422(client, price):
    r = quote(client, [{"sku": "TEST-SKU", "qty": 1, "unit_price": price}])
    assert r.status_code == 422


def test_empty_items_422(client):
    assert quote(client, []).status_code == 422


def test_too_many_lines_422(client):
    assert quote(client, [{"sku": "MUG-001", "qty": 1}] * 21).status_code == 422


def test_unknown_customer_404(client):
    r = quote(client, [{"sku": "MUG-001", "qty": 1}], customer="nobody")
    assert r.status_code == 404
    assert r.json()["error"]["code"] == "UNKNOWN_CUSTOMER"


def test_guest_can_quote(client):
    assert quote(client, [{"sku": "MUG-001", "qty": 1}], customer="guest").status_code == 200


def test_error_body_shape(client):
    error = quote(client, [{"sku": "MUG-001", "qty": 0}]).json()["error"]
    assert set(error) == {"code", "message", "details"}
    assert isinstance(error["details"], list)


def test_missing_customer_422(client):
    r = client.post("/api/cart/quote", json={"items": [{"sku": "MUG-001", "qty": 1}]})
    assert r.status_code == 422
