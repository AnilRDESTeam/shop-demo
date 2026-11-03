def test_lists_three_personas(client):
    customers = client.get("/api/customers").json()
    assert [c["id"] for c in customers] == ["new-customer-01", "returning-customer-01", "guest"]


def test_get_customer_by_id(client):
    c = client.get("/api/customers/returning-customer-01").json()
    assert c == {"id": "returning-customer-01", "name": "Ravi Returning",
                 "type": "registered", "order_count": 3}


def test_unknown_customer_404(client):
    r = client.get("/api/customers/nobody")
    assert r.status_code == 404
    assert r.json()["error"]["code"] == "UNKNOWN_CUSTOMER"
