# Shop Demo (baseline)

A small, local-only online shop with a JSON API, a simple web UI and automated tests.
It is the **baseline** ("before") system for the Evidence Gate hackathon.

**Current baseline rules:** orders of **$50.00 or more ship free** (otherwise $5.99). There are **no discounts**.

## 1. Prerequisites

Python 3.11 or newer, Git. Check in PowerShell:

```powershell
python --version
git --version
```

## 2. First-time setup

```powershell
git clone https://github.com/AnilRDESTeam/shop-demo.git
cd shop-demo
powershell -ExecutionPolicy Bypass -File scripts\setup.ps1
```

Clone into a folder that is **not** synced by OneDrive (synced folders can lock `.venv` files).
On macOS/Linux use `scripts/setup.sh` instead.

## 3. Run the app

```powershell
powershell -ExecutionPolicy Bypass -File scripts\run.ps1
```

Open http://localhost:8080 and do this 5-step check:

1. Pick the customer **Ravi Returning** in the header.
2. Add **Hoodie** ($45) and **Coffee Mug** ($12) to the cart.
3. Open the cart: subtotal `$57.00`, shipping `$0.00`, "Free shipping" badge.
4. Click **Place order**.
5. The receipt shows order `ORD-0001`, payment `simulated`, and no discount row.

## 4. Run the tests

```powershell
powershell -ExecutionPolicy Bypass -File scripts\test.ps1   # unit + API tests
powershell -ExecutionPolicy Bypass -File scripts\e2e.ps1    # browser tests (own server on port 8099)
```

## 5. Reset data

```powershell
Invoke-RestMethod -Method Post http://localhost:8080/api/test/reset
```

Only works when `APP_MODE=test` (the default).

## 6. Project map

| Folder | What it does |
|---|---|
| `app/main.py` | API routes, error handlers, serves the UI |
| `app/config.py` | Constants (free-shipping threshold, fee) and settings |
| `app/pricing/` | Shipping, discounts and quote rules |
| `app/catalog/` | Products |
| `app/orders/` | In-memory orders |
| `app/customers/` | **HIGH-RISK**: customer data (fake only) |
| `app/payments/` | **HIGH-RISK**: simulated payments (no real provider) |
| `app/data/` | Seed JSON files |
| `app/static/` | Web UI (plain HTML, CSS, JS) |
| `tests/` | `unit/`, `api/`, `e2e/` tests |
| `scripts/` | Setup, run and test scripts (`.ps1` and `.sh`) |
| `docs/` | API reference and the build instructions |

API details: [docs/API.md](docs/API.md).

## 7. Troubleshooting

| Problem | Fix |
|---|---|
| Port already in use | `$env:PORT=8081` then run `scripts\run.ps1` again |
| `python` not found | Install Python 3.11+ and reopen PowerShell |
| "running scripts is disabled" | Use `powershell -ExecutionPolicy Bypass -File scripts\<name>.ps1` |
| Chromium download blocked | `$env:SHOP_BROWSER_CHANNEL='msedge'` (uses installed Edge), then run `scripts\e2e.ps1` |
| `/api/health` shows `"dirty": true` | You have uncommitted changes in the repo; commit or stash them |

## 8. Git workflow

Never commit to `main` directly. Create a branch, push it, and open a pull request:

```powershell
git checkout -b my-change
git add -A
git commit -m "feat: describe the change"
git push -u origin my-change
```
