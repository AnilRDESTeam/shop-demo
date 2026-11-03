# Baseline Shop App — One-Shot Build Instructions (for Claude CLI)

> **Project:** Evidence Gate hackathon (4–5 Nov 2026) — this file builds the **baseline demo app** only.
> **Target:** working app on GitHub `main`, tagged `baseline-v1.0`, by **Tue 3 Nov 2026, 18:00 IST**.
> **Owner:** Anil (team lead). **Builder:** Claude (Sonnet 5.5) via Claude CLI.

---

## PART A — For Anil (human): how to use this file

1. Install on your laptop (company-approved method): **Python 3.12** (3.11–3.13 OK), **Git**, **VS Code**, **Claude CLI**.
   Check in PowerShell:
   ```powershell
   python --version
   git --version
   claude --version
   ```
2. GitHub repository (already created, empty): **https://github.com/AnilRDESTeam/shop-demo**
   - Clone/remote URL: `https://github.com/AnilRDESTeam/shop-demo.git`
   - Before building, set it to **Private**: GitHub → repo → Settings → General → Danger Zone → Change visibility → Private. Then add T1 and T2 as collaborators (Settings → Collaborators).
3. Create the project folder and put this file in it:
   ```powershell
   mkdir C:\Users\anikumar\Desktop\HackathonProjects\shop-demo
   cd C:\Users\anikumar\Desktop\HackathonProjects\shop-demo
   # copy Baseline-Shop-Build-Instructions.md into this folder (keep the same name)
   ```
   Final layout on your laptop (the Gate repo will sit next to it later):
   ```
   C:\Users\anikumar\Desktop\HackathonProjects\
   ├── shop-demo\          <- this build
   └── evidence-gate\      <- created later for the Gate
   ```
4. Start Claude CLI **in that folder** (`cd` into it first, then run `claude`) and paste this prompt:
   ```text
   Read Baseline-Shop-Build-Instructions.md completely before doing anything. Then execute PART B
   end to end, phase by phase, running the checks after each phase.
   Project folder: C:\Users\anikumar\Desktop\HackathonProjects\shop-demo (build here, not in a subfolder).
   GitHub remote URL: https://github.com/AnilRDESTeam/shop-demo.git
   Stop and ask me only for the items listed in "B13. When to stop and ask".
   At the end, give me the final report described in B12.
   ```
5. Approve commands as Claude asks. Expected time: 1.5–3 hours including fixes.
6. When done, follow **PART C** to verify yourself, then share the repo with the team.

---

## PART B — Instructions for the AI builder

### B1. Mission

Build a **small, deterministic, local-only online shop** ("Shop Demo") with a JSON API, a simple web UI, and a full automated test suite. It is the **baseline** ("before") version of a system that a quality gate will later test. Two future changes will be made by a *different* AI during the hackathon, so this baseline must **not** contain them:

- SHOP-101 (future): first-order "Welcome 10%" discount — **do NOT implement**.
- SHOP-102 (future): free-shipping threshold $50 → $75 — **do NOT implement**. Baseline threshold is **$50**.

### B2. Ground rules (read carefully)

1. **The team is beginner level.** Write simple, readable code with short comments explaining *why*. Prefer plain functions over clever abstractions. Keep each module under ~150 lines.
2. **Windows first.** The team uses Windows 11 + PowerShell. All scripts must work in PowerShell. Also provide bash equivalents.
3. **Local only and safe.** Bind to `127.0.0.1`. No outbound network calls at runtime. No real payments, no emails, no real customer data, no secrets.
4. **Deterministic.** Fixed seed data, in-memory state, a reset endpoint. Same input → same output.
5. **No frameworks in the browser.** Plain HTML + CSS + vanilla JS. No CDN links (must work offline).
6. **Money uses `Decimal`** in Python with `ROUND_HALF_UP` to 2 decimals. Convert to JSON numbers only at the API boundary (e.g. `5.99`, `57.0`, `0.0`). Tools compare with a ±0.005 tolerance, so `0.0` and `0.00` are equal.
7. **Follow this spec exactly.** Do not add features not listed. Field names, routes, and `data-testid` values are a **contract** — other tools depend on them.
8. Run tests after every phase. If something fails 3 times in a row, stop and report.
9. Commit after each phase with a clear message (format: `feat: ...`, `test: ...`, `docs: ...`, `chore: ...`).

### B3. Tech stack

| Part | Choice |
|---|---|
| Language | Python 3.12 (3.11–3.13 OK) |
| Web framework | FastAPI + Uvicorn |
| Validation | Pydantic v2 |
| Tests | pytest + FastAPI `TestClient` (needs `httpx`) |
| Browser smoke test | Playwright for Python (sync API), **no** pytest-playwright plugin |
| Frontend | static `index.html`, `app.js`, `styles.css` served by FastAPI |
| Storage | in-memory Python dicts loaded from JSON seed files |

`requirements.txt` (runtime): `fastapi`, `uvicorn[standard]`, `pydantic`.
`requirements-dev.txt`: `-r requirements.txt`, `pytest`, `httpx`, `playwright`.
After installing, **pin the exact installed versions** (`==`) in both files.

### B4. Folder structure (create exactly this)

```
shop-demo/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app: routes, error handlers, static files
│   ├── config.py               # constants + env settings (PORT, APP_MODE)
│   ├── models.py               # Pydantic request/response models
│   ├── money.py                # Decimal helpers: to_money(), money_to_float()
│   ├── gitinfo.py              # current git commit + dirty flag (for /api/health)
│   ├── catalog/
│   │   ├── __init__.py
│   │   └── products.py         # load products, find by SKU
│   ├── pricing/
│   │   ├── __init__.py
│   │   ├── shipping.py         # calculate_shipping(subtotal)
│   │   ├── discounts.py        # calculate_discount(customer, subtotal) -> baseline: none
│   │   └── quote.py            # build_quote(customer, items) -> full price breakdown
│   ├── customers/              # HIGH-RISK area (customer data) - fake data only
│   │   ├── __init__.py
│   │   └── store.py
│   ├── payments/               # HIGH-RISK area (payments) - simulated only
│   │   ├── __init__.py
│   │   └── simulator.py
│   ├── orders/
│   │   ├── __init__.py
│   │   └── store.py
│   ├── data/
│   │   ├── products.json
│   │   └── customers.json
│   └── static/
│       ├── index.html
│       ├── app.js
│       └── styles.css
├── tests/
│   ├── conftest.py
│   ├── unit/
│   │   ├── test_shipping.py
│   │   ├── test_discounts.py
│   │   └── test_quote.py
│   ├── api/
│   │   ├── test_health_api.py
│   │   ├── test_products_api.py
│   │   ├── test_customers_api.py
│   │   ├── test_quote_api.py
│   │   ├── test_orders_api.py
│   │   └── test_reset_api.py
│   └── e2e/
│       └── test_browser_smoke.py
├── scripts/
│   ├── setup.ps1   setup.sh
│   ├── run.ps1     run.sh
│   ├── test.ps1    test.sh
│   └── e2e.ps1     e2e.sh
├── docs/
│   └── API.md
├── pytest.ini
├── requirements.txt
├── requirements-dev.txt
├── .gitignore
├── .editorconfig
├── README.md
├── AGENTS.md                   # rules for OpenAI-based assistants working in this repo
└── CLAUDE.md                   # rules for Claude working in this repo (same content as AGENTS.md)
```

Do **not** create `.evidence-gate/` or `requirements/` folders — the team adds them on 4 Nov.

### B5. Business rules (baseline — exact)

All constants live in `app/config.py`:

```python
from decimal import Decimal
FREE_SHIPPING_THRESHOLD = Decimal("50.00")   # orders at or above this ship free
STANDARD_SHIPPING_FEE   = Decimal("5.99")
CURRENCY = "USD"
MAX_QTY_PER_LINE = 10
```

| Rule | Baseline behaviour |
|---|---|
| Line total | `unit_price × qty`, rounded to 2 dp |
| Subtotal | sum of line totals |
| Shipping | `0.00` if `subtotal >= 50.00`, else `5.99` |
| Discount | always `0.00`, `discount_label` = `null` (no promotions exist yet) |
| Total | `subtotal − discount + shipping` |
| `rules_applied` | `["free_shipping"]` when shipping is 0, else `["standard_shipping"]` |

`app/pricing/discounts.py` must contain:

```python
def calculate_discount(customer: dict, subtotal: Decimal) -> tuple[Decimal, str | None]:
    """Return (discount_amount, label). The baseline shop has no promotions."""
    return Decimal("0.00"), None
```

`app/pricing/shipping.py` must expose `calculate_shipping(subtotal: Decimal) -> Decimal` and use the constants from `config.py`. Keep the threshold logic in **one place only**.

### B6. Seed data

`app/data/products.json` — exactly these 7 items:

| sku | name | price | hidden |
|---|---|---|---|
| MUG-001 | Coffee Mug | 12.00 | false |
| TSHIRT-001 | Logo T-Shirt | 20.00 | false |
| NOTE-001 | Notebook | 8.50 | false |
| BAG-001 | Tote Bag | 25.00 | false |
| PEN-001 | Pen Set | 4.99 | false |
| HOODIE-001 | Hoodie | 45.00 | false |
| TEST-SKU | Test item (custom price) | 0.00 | **true** |

Each product: `{"sku", "name", "price", "description", "hidden", "custom_price_allowed"}`. Only `TEST-SKU` has `custom_price_allowed: true`. Hidden products never appear in the UI or in `GET /api/products`. `TEST-SKU` exists so automated checks can create an exact subtotal (e.g. 74.99).

`app/data/customers.json` — exactly these 3 test personas (fake):

| id | name | type | order_count |
|---|---|---|---|
| new-customer-01 | Nina New | registered | 0 |
| returning-customer-01 | Ravi Returning | registered | 3 |
| guest | Guest Shopper | guest | 0 |

### B7. API specification (exact)

Base URL: `http://127.0.0.1:8080` (port from env `PORT`, default `8080`). All JSON.

**Error format** for every non-2xx response (including validation errors — add exception handlers so FastAPI's default 422 body is replaced):

```json
{ "error": { "code": "UNKNOWN_SKU", "message": "Product 'XYZ' does not exist", "details": [] } }
```

Codes: `VALIDATION_ERROR` (422), `UNKNOWN_SKU` (404), `UNKNOWN_CUSTOMER` (404), `ORDER_NOT_FOUND` (404), `PRODUCT_NOT_FOUND` (404), `FORBIDDEN_IN_MODE` (403).

#### 1. `GET /api/health`
```json
{ "status": "ok", "app": "shop-demo", "version": "1.0.0", "mode": "test",
  "commit": "a41c9e2", "dirty": false }
```
`commit` = output of `git rev-parse --short HEAD` in the repo root; `dirty` = `git status --porcelain` is non-empty. Compute on each call (cache max 2 s). If git fails: `"commit": "unknown", "dirty": null`. This lets the quality gate detect "server is running different code than the branch I'm checking".

#### 2. `GET /api/products`
List of visible products: `[{"sku","name","price","description"}]` (6 items, no `TEST-SKU`).

#### 3. `GET /api/products/{sku}`
One product (hidden ones included only if requested by exact SKU). 404 `PRODUCT_NOT_FOUND`.

#### 4. `GET /api/customers` and `GET /api/customers/{id}`
`[{"id","name","type","order_count"}]`. 404 `UNKNOWN_CUSTOMER`.

#### 5. `POST /api/cart/quote` — price a cart without placing an order
Request:
```json
{ "customer_id": "returning-customer-01",
  "items": [ { "sku": "MUG-001", "qty": 2 } ] }
```
Rules:
- `customer_id` required; must exist (`guest` is valid).
- `items` required, 1–20 lines; `qty` integer 1–10.
- `unit_price` is **only allowed (and required) for `TEST-SKU`**; must be > 0 and ≤ 10000 with max 2 decimals. Sending `unit_price` for any other SKU → 422. `TEST-SKU` without `unit_price` → 422.
- Unknown SKU → 404 `UNKNOWN_SKU`.

Response 200:
```json
{
  "customer_id": "returning-customer-01",
  "items": [ { "sku": "MUG-001", "name": "Coffee Mug", "unit_price": 12.00, "qty": 2, "line_total": 24.00 } ],
  "subtotal": 24.00,
  "discount": 0.00,
  "discount_label": null,
  "shipping": 5.99,
  "total": 29.99,
  "currency": "USD",
  "rules_applied": ["standard_shipping"]
}
```
Example the gate will use later: `{"customer_id":"returning-customer-01","items":[{"sku":"TEST-SKU","qty":1,"unit_price":50.00}]}` → `shipping: 0.00`, `total: 50.00`.

#### 6. `POST /api/orders` — place an order (payment is simulated)
Same request body as quote. Response **201**: all quote fields plus
```json
{ "order_id": "ORD-0001", "created_at": "2026-11-04T10:00:00Z",
  "payment": { "status": "simulated", "reference": "SIM-0001" } }
```
- Order IDs are sequential `ORD-0001`, `ORD-0002`, … (reset by `/api/test/reset`).
- For `registered` customers, increment `order_count` by 1. Do **not** increment for `guest`.
- Call `app/payments/simulator.simulate_payment(order_id, total)`: returns `{"status":"simulated","reference":"SIM-000N"}`. No network, no real provider. Comment clearly that this is a simulation.

#### 7. `GET /api/orders/{order_id}` → the order (201 body shape, status 200). 404 `ORDER_NOT_FOUND`.
#### 8. `GET /api/orders?customer_id=...` → list of orders (optional filter).

#### 9. `POST /api/test/reset`
Restores customers, orders and the order counter to seed state. Returns `{"status":"reset"}`.
Allowed only when env `APP_MODE=test` (the default). If `APP_MODE=demo` → 403 `FORBIDDEN_IN_MODE`.

Also serve the UI: `GET /` → `app/static/index.html`; static assets under `/static/...`.
Write all of this in `docs/API.md` with copy-paste PowerShell examples using `Invoke-RestMethod` and `curl.exe`.

### B8. Web UI specification

Single page `index.html` with hash routing. Clean, simple CSS (cards, a header bar, readable fonts). No frameworks, no browser storage (cart lives in a JS variable).

**Header (always visible)**
- Title "Shop Demo".
- Customer selector `<select data-testid="customer-select">` filled from `GET /api/customers`. Initial value from URL query `?customer=<id>` if present, else `returning-customer-01`. Changing it re-quotes the cart.
- Link to cart `data-testid="nav-cart"` with item count `data-testid="cart-count"`.
- Error banner `data-testid="error-banner"` (hidden unless an API call fails; shows the error message).

**`#/` — Products**
- Card per product `data-testid="product-card-{SKU}"`, showing name, price `data-testid="product-price-{SKU}"` (format `$12.00`), button **Add to cart** `data-testid="add-to-cart-{SKU}"` (adds qty 1 or increments).

**`#/cart` — Cart**
- Empty state `data-testid="cart-empty"`.
- Line per item `data-testid="cart-line-{SKU}"` with `qty-decrease-{SKU}`, `qty-value-{SKU}`, `qty-increase-{SKU}`, `remove-{SKU}`.
- Summary always comes from `POST /api/cart/quote` (never compute prices in JS):
  - `cart-subtotal`
  - `cart-discount-row` — rendered **only if discount > 0**, containing `cart-discount-label` and `cart-discount`
  - `cart-shipping` (always the amount, e.g. `$0.00`) and a separate badge `cart-free-shipping-badge` ("Free shipping") shown only when shipping is 0
  - `cart-total`
- Button **Place order** `data-testid="place-order"` → `POST /api/orders` → navigate to `#/receipt/{order_id}`.

**`#/receipt/{order_id}` — Receipt** (loads from `GET /api/orders/{id}`, so deep links work)
- `receipt-order-id`, `receipt-customer`, line per item `receipt-line-{SKU}`
- `receipt-subtotal`, `receipt-discount-row` (only if discount > 0) with `receipt-discount-label` and `receipt-discount`, `receipt-shipping`, `receipt-total`, `receipt-payment-status`
- Button **Continue shopping** `data-testid="continue-shopping"` → clears cart, goes to `#/`.

**Rule for amount elements:** elements with money `data-testid`s contain **only** the formatted amount, e.g. `$5.99` (no extra words), so automated tools can read them.

### B9. Tests (required)

`pytest.ini`:
```ini
[pytest]
testpaths = tests
markers =
    e2e: browser tests that start the server (run with: pytest -m e2e)
addopts = -m "not e2e" -q
```

`tests/conftest.py`: a `client` fixture (FastAPI `TestClient`) that calls `POST /api/test/reset` before each test.

Minimum tests (write more if useful; target ~35):

| File | Must cover |
|---|---|
| unit/test_shipping.py | parametrized: 0.01→5.99, 49.99→5.99, 50.00→0.00, 50.01→0.00, 120.00→0.00 |
| unit/test_discounts.py | baseline returns `(0.00, None)` for new, returning and guest customers |
| unit/test_quote.py | line totals; subtotal sum; total formula; rounding (`PEN-001` × 3 = 14.97); `rules_applied` values |
| api/test_health_api.py | status ok; keys `commit`, `dirty`, `mode`, `version` present |
| api/test_products_api.py | 6 visible products; `TEST-SKU` not listed; get by SKU; 404 |
| api/test_customers_api.py | 3 personas; get by id; 404 |
| api/test_quote_api.py | normal quote; TEST-SKU 50.00 → free; TEST-SKU 49.99 → 5.99; discount fields are 0 and null; unknown SKU 404; qty 0 → 422; qty 11 → 422; `unit_price` on MUG-001 → 422; TEST-SKU without price → 422; unknown customer 404; error body shape |
| api/test_orders_api.py | create 201 with `ORD-0001`; get by id; 404; `order_count` +1 for registered; unchanged for guest; payment status `simulated` |
| api/test_reset_api.py | reset restores counts and order numbering; 403 when `APP_MODE=demo` (use monkeypatch) |
| e2e/test_browser_smoke.py | marked `@pytest.mark.e2e`; fixture starts uvicorn as a subprocess on port **8099** with `APP_MODE=test`, waits for `/api/health`, stops it after. Test: open `http://127.0.0.1:8099/?customer=returning-customer-01`, add `MUG-001` and `HOODIE-001`, open cart, assert `cart-shipping` = `$0.00` and badge visible (57.00 ≥ 50), place order, assert `receipt-total` = `$57.00`, assert `receipt-discount-row` is absent. Second test: `PEN-001` only → `cart-shipping` = `$5.99`. |

Browser for e2e: default Playwright Chromium. If env `SHOP_BROWSER_CHANNEL` is set (e.g. `msedge` or `chrome`), launch with `channel=<value>` to use the browser already installed on the laptop (fallback when the Chromium download is blocked by the corporate network).

### B10. Scripts

Scripts call the venv's Python directly (`.venv\Scripts\python.exe`), so nobody needs to "activate" the venv (activation is often blocked by PowerShell policy).

| Script | Does |
|---|---|
| `scripts/setup.ps1` | create `.venv` if missing; `pip install -r requirements-dev.txt`; try `python -m playwright install chromium` — if it fails, print a friendly message: "Chromium download blocked. Set `$env:SHOP_BROWSER_CHANNEL='msedge'` to use Edge instead." and continue |
| `scripts/run.ps1` | start `uvicorn app.main:app --host 127.0.0.1 --port <PORT or 8080> --reload`; print "Open http://localhost:8080" |
| `scripts/test.ps1` | run `pytest` (unit + API) |
| `scripts/e2e.ps1` | run `pytest -m e2e` |

Users run them as: `powershell -ExecutionPolicy Bypass -File scripts\setup.ps1`. Provide matching `.sh` files using `.venv/bin/python`.

`.gitignore` must include: `.venv/`, `__pycache__/`, `*.pyc`, `.pytest_cache/`, `out/`, `.env`, `test-results/`, `playwright-report/`, `*.log`.

### B11. Repository docs

**README.md** (written for beginners, Windows first):
1. What this is (2 lines) + current baseline rules ($50 free shipping, no discounts).
2. Prerequisites + version checks.
3. First-time setup: `git clone https://github.com/AnilRDESTeam/shop-demo.git`, `cd shop-demo`, `powershell -ExecutionPolicy Bypass -File scripts\setup.ps1`. Recommend cloning into a folder that is **not** synced by OneDrive (synced folders can lock `.venv` files).
4. Run: `scripts\run.ps1` → open http://localhost:8080 → a 5-step manual check (pick customer, add Hoodie + Mug, see free shipping, place order, see receipt).
5. Run tests: `scripts\test.ps1`, `scripts\e2e.ps1`.
6. Reset data: `Invoke-RestMethod -Method Post http://localhost:8080/api/test/reset`.
7. Project map (which folder does what; mark `app/payments` and `app/customers` as **high-risk**).
8. Troubleshooting table: port in use (`$env:PORT=8081`), `python` not found, execution policy, Chromium download blocked, "commit shows dirty".
9. Git workflow for the team (never commit to `main` directly; branch → push → PR).

**AGENTS.md** and **CLAUDE.md** (same content): rules for any AI assistant editing this repo —
- Money uses `Decimal`; pricing rules live only in `app/pricing/` and constants in `app/config.py`.
- Never rename API fields, routes or `data-testid` values (they are a contract).
- `app/payments/` and `app/customers/` are high-risk: change only when the task explicitly requires it.
- Always run `scripts\test.ps1` before committing; add/adjust tests with every behaviour change.
- No network calls, no real payment or email code, no secrets.

### B12. Build phases (do in order; check and commit after each)

| Phase | Work | Check before commit |
|---|---|---|
| 0 | Work directly in `C:\Users\anikumar\Desktop\HackathonProjects\shop-demo` (the folder containing this file; do not create a nested `shop-demo` folder). `git init -b main`; `.gitignore`, `.editorconfig`; create venv; install deps; pin versions. Keep `Baseline-Shop-Build-Instructions.md` in the repo under `docs/` (move it there in phase 5). | `python -c "import fastapi"` works |
| 1 | `config.py`, `money.py`, seed JSON, catalog, customers store, pricing (shipping, discounts, quote) + unit tests | `pytest tests/unit` green |
| 2 | `models.py`, `main.py` routes, error handlers, orders, payments simulator, reset, health/gitinfo + API tests | `pytest` green |
| 3 | UI (`index.html`, `app.js`, `styles.css`) with every `data-testid` from B8 | start server, `curl.exe http://127.0.0.1:8080/` returns HTML; `/api/products` returns 6 items |
| 4 | e2e test + scripts | `pytest -m e2e` green (if Chromium blocked, try `SHOP_BROWSER_CHANNEL=msedge`; if both fail, report it — do not fake a pass) |
| 5 | README, docs/API.md, AGENTS.md, CLAUDE.md | read-through: every command in README actually works |
| 6 | Final full run: `scripts\test.ps1` and `scripts\e2e.ps1`; ensure `git status` clean | all green |
| 7 | Push: `git remote add origin https://github.com/AnilRDESTeam/shop-demo.git`; `git push -u origin main`; `git tag -a baseline-v1.0 -m "Baseline shop: $50 free shipping, no discounts"`; `git push origin baseline-v1.0` | `git ls-remote --tags origin` shows the tag |

Never force-push. Never change the repo's visibility yourself. Before the first push, ask Anil to confirm the repo is set to **Private**. Do not commit `.venv`, `out/` or secrets.

**Final report to Anil** (print at the end):
- what was built (one paragraph), number of tests passed (unit+API, e2e), commit SHA, tag, repo URL
- exact commands to run the app and tests
- anything that did not work (e.g. Chromium download) and the workaround used
- any deviation from this spec, with reason

### B13. When to stop and ask Anil

- Before the first push: confirm with Anil that https://github.com/AnilRDESTeam/shop-demo is Private.
- Push fails due to authentication (Anil may need to sign in to GitHub in the pop-up window).
- A required tool is missing (Python < 3.11, Git).
- Playwright cannot launch any browser (Chromium download blocked **and** Edge/Chrome channel fails).
- Anything in this spec seems contradictory.

### B14. Must NOT build

Login/auth, database, Docker, real payments, emails, admin pages, product images from the internet, discounts/promotions, a $75 threshold, CI pipelines, `.evidence-gate/` folder, `requirements/` folder, any analytics or telemetry.

---

## PART C — Anil's acceptance checklist (do this yourself after the build)

- [ ] https://github.com/AnilRDESTeam/shop-demo shows `main` with all folders above, tag `baseline-v1.0`, and the **Private** badge.
- [ ] Fresh clone test:
  ```powershell
  cd $env:TEMP
  git clone https://github.com/AnilRDESTeam/shop-demo.git shop-demo-check
  cd shop-demo-check
  powershell -ExecutionPolicy Bypass -File scripts\setup.ps1
  powershell -ExecutionPolicy Bypass -File scripts\run.ps1     # then open http://localhost:8080
  ```
- [ ] Manual: customer "Ravi Returning", add Hoodie ($45) + Mug ($12) → cart shows subtotal `$57.00`, shipping `$0.00`, "Free shipping" badge, total `$57.00`.
- [ ] Manual: Pen Set only → shipping `$5.99`.
- [ ] Place order → receipt shows `ORD-0001`, payment "simulated", no discount row.
- [ ] `Invoke-RestMethod http://localhost:8080/api/health` shows the same commit as `git rev-parse --short HEAD`.
- [ ] PowerShell quote check returns shipping 0 at exactly 50:
  ```powershell
  $body = '{"customer_id":"returning-customer-01","items":[{"sku":"TEST-SKU","qty":1,"unit_price":50.00}]}'
  Invoke-RestMethod -Method Post -Uri http://localhost:8080/api/cart/quote -ContentType 'application/json' -Body $body
  ```
- [ ] `scripts\test.ps1` all green; `scripts\e2e.ps1` all green.
- [ ] Add both teammates as collaborators (Write access) on the repo.
- [ ] Each teammate clones and renders the app locally by **3 Nov 18:00 IST**.
