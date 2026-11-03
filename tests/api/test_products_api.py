def test_lists_six_visible_products(client):
    products = client.get("/api/products").json()
    assert len(products) == 6
    assert set(products[0]) == {"sku", "name", "price", "description"}


def test_test_sku_is_not_listed(client):
    skus = [p["sku"] for p in client.get("/api/products").json()]
    assert "TEST-SKU" not in skus


def test_get_product_by_sku(client):
    r = client.get("/api/products/HOODIE-001")
    assert r.status_code == 200
    assert r.json()["price"] == 45.0


def test_hidden_product_found_by_exact_sku(client):
    assert client.get("/api/products/TEST-SKU").status_code == 200


def test_unknown_product_404(client):
    r = client.get("/api/products/NOPE")
    assert r.status_code == 404
    assert r.json()["error"]["code"] == "PRODUCT_NOT_FOUND"
