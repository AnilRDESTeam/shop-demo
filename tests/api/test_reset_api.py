def place(client):
    return client.post("/api/orders", json={
        "customer_id": "returning-customer-01", "items": [{"sku": "MUG-001", "qty": 1}]})


def test_reset_restores_counts_and_numbering(client):
    place(client)
    assert client.get("/api/customers/returning-customer-01").json()["order_count"] == 4

    r = client.post("/api/test/reset")
    assert r.status_code == 200
    assert r.json() == {"status": "reset"}

    assert client.get("/api/customers/returning-customer-01").json()["order_count"] == 3
    assert client.get("/api/orders").json() == []
    assert place(client).json()["order_id"] == "ORD-0001"


def test_reset_forbidden_in_demo_mode(client, monkeypatch):
    monkeypatch.setenv("APP_MODE", "demo")
    r = client.post("/api/test/reset")
    assert r.status_code == 403
    assert r.json()["error"]["code"] == "FORBIDDEN_IN_MODE"
