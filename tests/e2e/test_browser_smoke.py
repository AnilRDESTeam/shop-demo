"""Browser smoke test. Starts the real server on port 8099 and drives it with Playwright.

Run with: pytest -m e2e
Set SHOP_BROWSER_CHANNEL=msedge (or chrome) to use a browser already installed
on the laptop when the Chromium download is blocked.
"""
import os
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

import pytest
from playwright.sync_api import expect, sync_playwright

pytestmark = pytest.mark.e2e

PORT = 8099
BASE = f"http://127.0.0.1:{PORT}"
ROOT = Path(__file__).resolve().parents[2]


@pytest.fixture(scope="module")
def server():
    env = {**os.environ, "APP_MODE": "test", "PORT": str(PORT)}
    proc = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", str(PORT)],
        cwd=ROOT, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    try:
        for _ in range(50):   # wait up to ~10 s for the server
            try:
                urllib.request.urlopen(f"{BASE}/api/health", timeout=1)
                break
            except OSError:
                time.sleep(0.2)
        else:
            raise RuntimeError("Server did not start")
        yield BASE
    finally:
        proc.terminate()
        proc.wait(timeout=10)


@pytest.fixture
def page(server):
    urllib.request.urlopen(urllib.request.Request(f"{BASE}/api/test/reset", method="POST"))
    with sync_playwright() as p:
        channel = os.environ.get("SHOP_BROWSER_CHANNEL")
        browser = p.chromium.launch(channel=channel) if channel else p.chromium.launch()
        page = browser.new_page()
        yield page
        browser.close()


def tid(page, name):
    return page.get_by_test_id(name)


def test_free_shipping_and_receipt(page):
    page.goto(f"{BASE}/?customer=returning-customer-01")
    tid(page, "add-to-cart-MUG-001").click()
    tid(page, "add-to-cart-HOODIE-001").click()
    tid(page, "nav-cart").click()

    expect(tid(page, "cart-shipping")).to_have_text("$0.00")
    expect(tid(page, "cart-free-shipping-badge")).to_be_visible()

    tid(page, "place-order").click()
    expect(tid(page, "receipt-total")).to_have_text("$54.15")
    expect(tid(page, "receipt-discount-label")).to_have_text("Loyalty 5% off")
    expect(tid(page, "receipt-discount")).to_have_text("$2.85")


def test_standard_shipping_for_small_cart(page):
    page.goto(f"{BASE}/?customer=returning-customer-01")
    tid(page, "add-to-cart-PEN-001").click()
    tid(page, "nav-cart").click()

    expect(tid(page, "cart-shipping")).to_have_text("$5.99")
    expect(tid(page, "cart-free-shipping-badge")).to_have_count(0)
