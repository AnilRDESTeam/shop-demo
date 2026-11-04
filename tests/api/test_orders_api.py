def order(client, customer="returning-customer-01", items=None):
    items = items or [{"sku": "HOODIE-001", "qty": 1}, {"sku": "BAG-001", "qty": 1}, {"sku": "MUG-001", "qty": 1}]
    return client.post("/api/orders", json={"customer_id": customer, "items": items})


def order_count(client, customer_id):
    return client.get(f"/api/customers/{customer_id}").json()["order_count"]


def test_create_order_201(client):
    r = order(client)
    assert r.status_code == 201
    body = r.json()
    assert body["order_id"] == "ORD-0001"
    assert body["total"] == 82.0
    assert body["shipping"] == 0.0
    assert body["created_at"].endswith("Z")


def test_order_ids_are_sequential(client):
    assert order(client).json()["order_id"] == "ORD-0001"
    assert order(client).json()["order_id"] == "ORD-0002"


def test_payment_is_simulated(client):
    payment = order(client).json()["payment"]
    assert payment == {"status": "simulated", "reference": "SIM-0001"}


def test_get_order_by_id(client):
    order(client)
    r = client.get("/api/orders/ORD-0001")
    assert r.status_code == 200
    assert r.json()["order_id"] == "ORD-0001"


def test_unknown_order_404(client):
    r = client.get("/api/orders/ORD-9999")
    assert r.status_code == 404
    assert r.json()["error"]["code"] == "ORDER_NOT_FOUND"


def test_registered_customer_order_count_increases(client):
    order(client, customer="returning-customer-01")
    assert order_count(client, "returning-customer-01") == 4


def test_guest_order_count_unchanged(client):
    order(client, customer="guest")
    assert order_count(client, "guest") == 0


def test_list_orders_filter_by_customer(client):
    order(client, customer="guest")
    order(client, customer="new-customer-01")
    assert len(client.get("/api/orders").json()) == 2
    only_guest = client.get("/api/orders", params={"customer_id": "guest"}).json()
    assert [o["customer_id"] for o in only_guest] == ["guest"]


def test_invalid_order_is_not_saved(client):
    r = order(client, items=[{"sku": "NOPE", "qty": 1}])
    assert r.status_code == 404
    assert client.get("/api/orders").json() == []
    assert order(client).json()["order_id"] == "ORD-0001"
