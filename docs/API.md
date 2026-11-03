# Shop Demo API

Base URL: `http://127.0.0.1:8080` (port from env `PORT`). All requests and responses are JSON.
Money amounts are JSON numbers (e.g. `5.99`, `57.0`).

## Errors

Every non-2xx response has this shape (including validation errors):

```json
{ "error": { "code": "UNKNOWN_SKU", "message": "Product 'XYZ' does not exist", "details": [] } }
```

| Code | Status |
|---|---|
| `VALIDATION_ERROR` | 422 |
| `UNKNOWN_SKU`, `UNKNOWN_CUSTOMER`, `ORDER_NOT_FOUND`, `PRODUCT_NOT_FOUND` | 404 |
| `FORBIDDEN_IN_MODE` | 403 |

## Endpoints

### GET /api/health
`{"status","app","version","mode","commit","dirty"}`. `commit` and `dirty` come from git (`"unknown"` / `null` if git fails).

```powershell
Invoke-RestMethod http://localhost:8080/api/health
curl.exe http://localhost:8080/api/health
```

### GET /api/products
The 6 visible products: `[{"sku","name","price","description"}]`. The hidden `TEST-SKU` is not listed.

```powershell
Invoke-RestMethod http://localhost:8080/api/products
```

### GET /api/products/{sku}
One product (hidden ones are found by exact SKU). 404 `PRODUCT_NOT_FOUND`.

```powershell
Invoke-RestMethod http://localhost:8080/api/products/HOODIE-001
```

### GET /api/customers and GET /api/customers/{id}
`[{"id","name","type","order_count"}]`. Personas: `new-customer-01`, `returning-customer-01`, `guest`. 404 `UNKNOWN_CUSTOMER`.

```powershell
Invoke-RestMethod http://localhost:8080/api/customers/returning-customer-01
```

### POST /api/cart/quote
Prices a cart without placing an order.

Request: `{"customer_id": "...", "items": [{"sku": "MUG-001", "qty": 2}]}`

- `items`: 1 to 20 lines; `qty` is an integer 1 to 10.
- `unit_price` is allowed (and required) **only** for `TEST-SKU`: greater than 0, at most 10000, max 2 decimals.
- Unknown SKU gives 404 `UNKNOWN_SKU`; unknown customer gives 404 `UNKNOWN_CUSTOMER`.

Response 200:

```json
{
  "customer_id": "returning-customer-01",
  "items": [ { "sku": "MUG-001", "name": "Coffee Mug", "unit_price": 12.0, "qty": 2, "line_total": 24.0 } ],
  "subtotal": 24.0, "discount": 0.0, "discount_label": null,
  "shipping": 5.99, "total": 29.99, "currency": "USD",
  "rules_applied": ["standard_shipping"]
}
```

Baseline rules: shipping is `0.00` when subtotal is 50.00 or more, else `5.99`; discount is always `0.00`.

```powershell
$body = '{"customer_id":"returning-customer-01","items":[{"sku":"TEST-SKU","qty":1,"unit_price":50.00}]}'
Invoke-RestMethod -Method Post -Uri http://localhost:8080/api/cart/quote -ContentType 'application/json' -Body $body
```

```powershell
curl.exe -X POST http://localhost:8080/api/cart/quote -H "Content-Type: application/json" -d "{\"customer_id\":\"guest\",\"items\":[{\"sku\":\"MUG-001\",\"qty\":2}]}"
```

### POST /api/orders
Same body as the quote. Returns **201** with all quote fields plus
`order_id` (`ORD-0001`, `ORD-0002`, ...), `created_at` and `payment` (`{"status":"simulated","reference":"SIM-0001"}`).
Payment is a simulation: no network, no real provider. Registered customers get `order_count` + 1; guests do not.

```powershell
$body = '{"customer_id":"returning-customer-01","items":[{"sku":"HOODIE-001","qty":1},{"sku":"MUG-001","qty":1}]}'
Invoke-RestMethod -Method Post -Uri http://localhost:8080/api/orders -ContentType 'application/json' -Body $body
```

### GET /api/orders/{order_id}
The order (same shape as the 201 body). 404 `ORDER_NOT_FOUND`.

```powershell
Invoke-RestMethod http://localhost:8080/api/orders/ORD-0001
```

### GET /api/orders?customer_id=...
List of orders; `customer_id` is an optional filter.

```powershell
Invoke-RestMethod "http://localhost:8080/api/orders?customer_id=guest"
```

### POST /api/test/reset
Restores customers, orders and the order counter to seed state. Returns `{"status":"reset"}`.
Allowed only when `APP_MODE=test` (the default); with `APP_MODE=demo` it returns 403 `FORBIDDEN_IN_MODE`.

```powershell
Invoke-RestMethod -Method Post http://localhost:8080/api/test/reset
```

### UI
`GET /` serves the web UI; assets are under `/static/...`.
