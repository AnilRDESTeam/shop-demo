def test_health_ok(client):
    r = client.get("/api/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"
    assert r.json()["app"] == "shop-demo"


def test_health_has_required_keys(client):
    body = client.get("/api/health").json()
    for key in ("commit", "dirty", "mode", "version"):
        assert key in body


def test_health_mode_defaults_to_test(client):
    assert client.get("/api/health").json()["mode"] == "test"
