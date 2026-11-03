"""FastAPI app: routes, error handlers and static files."""
from datetime import datetime, timezone
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException

from app import config
from app.catalog.products import find_product, list_visible_products
from app.customers import store as customers
from app.gitinfo import get_git_info
from app.models import CartRequest
from app.money import money_to_float
from app.orders import store as orders
from app.payments.simulator import simulate_payment
from app.pricing.quote import build_quote

STATIC_DIR = Path(__file__).resolve().parent / "static"

app = FastAPI(title="Shop Demo", version=config.APP_VERSION)


class ApiError(Exception):
    """An error that becomes {"error": {"code", "message", "details"}}."""

    def __init__(self, status: int, code: str, message: str, details: list | None = None):
        self.status, self.code, self.message, self.details = status, code, message, details or []


def error_response(status: int, code: str, message: str, details: list | None = None):
    body = {"error": {"code": code, "message": message, "details": details or []}}
    return JSONResponse(status_code=status, content=body)


@app.exception_handler(ApiError)
async def handle_api_error(request: Request, exc: ApiError):
    return error_response(exc.status, exc.code, exc.message, exc.details)


@app.exception_handler(RequestValidationError)
async def handle_validation_error(request: Request, exc: RequestValidationError):
    # Replace FastAPI's default 422 body with our error format
    details = [
        {"field": ".".join(str(p) for p in e["loc"] if p != "body"), "message": e["msg"]}
        for e in exc.errors()
    ]
    return error_response(422, "VALIDATION_ERROR", "Request validation failed", details)


@app.exception_handler(StarletteHTTPException)
async def handle_http_error(request: Request, exc: StarletteHTTPException):
    code = {404: "NOT_FOUND", 405: "METHOD_NOT_ALLOWED"}.get(exc.status_code, "HTTP_ERROR")
    return error_response(exc.status_code, code, str(exc.detail))


def public_product(p: dict) -> dict:
    return {"sku": p["sku"], "name": p["name"], "price": money_to_float(p["price"]),
            "description": p["description"]}


def quote_to_json(q: dict) -> dict:
    """Convert Decimal amounts to JSON numbers (only done here, at the API edge)."""
    out = dict(q)
    for key in ("subtotal", "discount", "shipping", "total"):
        out[key] = money_to_float(q[key])
    out["items"] = [
        {**line, "unit_price": money_to_float(line["unit_price"]),
         "line_total": money_to_float(line["line_total"])}
        for line in q["items"]
    ]
    return out


def price_cart(body: CartRequest) -> dict:
    customer = customers.find_customer(body.customer_id)
    if customer is None:
        raise ApiError(404, "UNKNOWN_CUSTOMER", f"Customer '{body.customer_id}' does not exist")
    items = [item.model_dump() for item in body.items]
    for item in items:
        if find_product(item["sku"]) is None:
            raise ApiError(404, "UNKNOWN_SKU", f"Product '{item['sku']}' does not exist")
    return quote_to_json(build_quote(customer, items))


@app.get("/api/health")
def health():
    return {"status": "ok", "app": config.APP_NAME, "version": config.APP_VERSION,
            "mode": config.get_mode(), **get_git_info()}


@app.get("/api/products")
def get_products():
    return [public_product(p) for p in list_visible_products()]


@app.get("/api/products/{sku}")
def get_product(sku: str):
    product = find_product(sku)
    if product is None:
        raise ApiError(404, "PRODUCT_NOT_FOUND", f"Product '{sku}' does not exist")
    return public_product(product)


@app.get("/api/customers")
def get_customers():
    return customers.list_customers()


@app.get("/api/customers/{customer_id}")
def get_customer(customer_id: str):
    customer = customers.find_customer(customer_id)
    if customer is None:
        raise ApiError(404, "UNKNOWN_CUSTOMER", f"Customer '{customer_id}' does not exist")
    return customer


@app.post("/api/cart/quote")
def quote_cart(body: CartRequest):
    return price_cart(body)


@app.post("/api/orders", status_code=201)
def place_order(body: CartRequest):
    quote = price_cart(body)
    order_id = orders.next_order_id()
    payment = simulate_payment(order_id, quote["total"])   # simulation only
    order = {**quote, "order_id": order_id, "payment": payment,
             "created_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}
    orders.save_order(order)
    customers.increment_order_count(body.customer_id)
    return order


@app.get("/api/orders")
def get_orders(customer_id: str | None = None):
    return orders.list_orders(customer_id)


@app.get("/api/orders/{order_id}")
def get_order(order_id: str):
    order = orders.find_order(order_id)
    if order is None:
        raise ApiError(404, "ORDER_NOT_FOUND", f"Order '{order_id}' does not exist")
    return order


@app.post("/api/test/reset")
def reset():
    if config.get_mode() != "test":
        raise ApiError(403, "FORBIDDEN_IN_MODE", "Reset is only allowed when APP_MODE=test")
    customers.reset_customers()
    orders.reset_orders()
    return {"status": "reset"}


@app.get("/", include_in_schema=False)
def index():
    return FileResponse(STATIC_DIR / "index.html")


app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
