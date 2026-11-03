// Shop Demo UI: plain vanilla JS. The cart lives in a variable (no browser storage).
// Prices are NEVER calculated here; the summary always comes from POST /api/cart/quote.

let cart = [];          // [{ sku, qty }]
let products = [];
let customers = [];
let customerId = new URLSearchParams(location.search).get("customer") || "returning-customer-01";

const $ = (testid) => document.querySelector(`[data-testid="${testid}"]`);
const view = document.getElementById("view");
const money = (n) => "$" + Number(n).toFixed(2);
const esc = (s) => String(s).replace(/[&<>"']/g, (c) => `&#${c.charCodeAt(0)};`);

function showError(message) {
  const banner = $("error-banner");
  banner.textContent = message || "";
  banner.hidden = !message;
}

async function api(path, body) {
  const options = body ? { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) } : {};
  const res = await fetch(path, options);
  const data = await res.json();
  if (!res.ok) throw new Error(data.error ? data.error.message : "Request failed");
  return data;
}

// ---- cart helpers ----
function changeQty(sku, delta) {
  const line = cart.find((l) => l.sku === sku);
  if (!line) return;
  line.qty += delta;
  if (line.qty < 1) cart = cart.filter((l) => l.sku !== sku);
  if (line.qty > 10) line.qty = 10;   // server limit per line
  render();
}

function addToCart(sku) {
  const line = cart.find((l) => l.sku === sku);
  if (line) line.qty = Math.min(line.qty + 1, 10);
  else cart.push({ sku, qty: 1 });
  render();
}

// ---- views ----
function renderProducts() {
  view.innerHTML = '<div class="grid">' + products.map((p) => `
    <div class="card" data-testid="product-card-${p.sku}">
      <h3>${esc(p.name)}</h3>
      <p>${esc(p.description)}</p>
      <div class="price" data-testid="product-price-${p.sku}">${money(p.price)}</div>
      <button data-testid="add-to-cart-${p.sku}" data-sku="${p.sku}">Add to cart</button>
    </div>`).join("") + "</div>";
  view.querySelectorAll("button[data-sku]").forEach((b) => b.addEventListener("click", () => addToCart(b.dataset.sku)));
}

async function renderCart() {
  if (cart.length === 0) {
    view.innerHTML = '<div class="card" data-testid="cart-empty">Your cart is empty.</div>';
    return;
  }
  const quote = await api("/api/cart/quote", { customer_id: customerId, items: cart });
  const lines = quote.items.map((i) => `
    <div class="line" data-testid="cart-line-${i.sku}">
      <span class="name">${esc(i.name)} (${money(i.unit_price)})</span>
      <button class="secondary" data-testid="qty-decrease-${i.sku}" data-act="dec" data-sku="${i.sku}">-</button>
      <span class="qty" data-testid="qty-value-${i.sku}">${i.qty}</span>
      <button class="secondary" data-testid="qty-increase-${i.sku}" data-act="inc" data-sku="${i.sku}">+</button>
      <button class="secondary" data-testid="remove-${i.sku}" data-act="rm" data-sku="${i.sku}">Remove</button>
    </div>`).join("");
  const discountRow = quote.discount > 0 ? `
      <div data-testid="cart-discount-row"><span data-testid="cart-discount-label">${esc(quote.discount_label)}</span>
        <span data-testid="cart-discount">${money(quote.discount)}</span></div>` : "";
  const badge = quote.shipping === 0 ? '<span class="badge" data-testid="cart-free-shipping-badge">Free shipping</span>' : "";
  view.innerHTML = `<div class="card">${lines}
    <div class="summary">
      <div><span>Subtotal</span><span data-testid="cart-subtotal">${money(quote.subtotal)}</span></div>
      ${discountRow}
      <div><span>Shipping ${badge}</span><span data-testid="cart-shipping">${money(quote.shipping)}</span></div>
      <div class="total"><span>Total</span><span data-testid="cart-total">${money(quote.total)}</span></div>
    </div>
    <div class="actions"><button data-testid="place-order">Place order</button></div></div>`;
  view.querySelectorAll("button[data-act]").forEach((b) => b.addEventListener("click", () => {
    const sku = b.dataset.sku;
    if (b.dataset.act === "rm") { cart = cart.filter((l) => l.sku !== sku); render(); }
    else changeQty(sku, b.dataset.act === "inc" ? 1 : -1);
  }));
  $("place-order").addEventListener("click", placeOrder);
}

async function placeOrder() {
  try {
    const order = await api("/api/orders", { customer_id: customerId, items: cart });
    location.hash = "#/receipt/" + order.order_id;
  } catch (err) {
    showError(err.message);
  }
}

async function renderReceipt(orderId) {
  const o = await api("/api/orders/" + encodeURIComponent(orderId));
  const customer = customers.find((c) => c.id === o.customer_id);
  const lines = o.items.map((i) => `
    <div class="line" data-testid="receipt-line-${i.sku}">
      <span class="name">${esc(i.name)} x ${i.qty}</span><span>${money(i.line_total)}</span>
    </div>`).join("");
  const discountRow = o.discount > 0 ? `
      <div data-testid="receipt-discount-row"><span data-testid="receipt-discount-label">${esc(o.discount_label)}</span>
        <span data-testid="receipt-discount">${money(o.discount)}</span></div>` : "";
  view.innerHTML = `<div class="card"><h2>Receipt <span data-testid="receipt-order-id">${esc(o.order_id)}</span></h2>
    <p>Customer: <span data-testid="receipt-customer">${esc(customer ? customer.name : o.customer_id)}</span></p>
    ${lines}
    <div class="summary">
      <div><span>Subtotal</span><span data-testid="receipt-subtotal">${money(o.subtotal)}</span></div>
      ${discountRow}
      <div><span>Shipping</span><span data-testid="receipt-shipping">${money(o.shipping)}</span></div>
      <div class="total"><span>Total</span><span data-testid="receipt-total">${money(o.total)}</span></div>
      <div><span>Payment</span><span data-testid="receipt-payment-status">${esc(o.payment.status)}</span></div>
    </div>
    <div class="actions"><button data-testid="continue-shopping">Continue shopping</button></div></div>`;
  $("continue-shopping").addEventListener("click", () => { cart = []; location.hash = "#/"; });
}

async function render() {
  showError("");
  $("cart-count").textContent = cart.reduce((sum, l) => sum + l.qty, 0);
  const hash = location.hash || "#/";
  try {
    if (hash.startsWith("#/cart")) await renderCart();
    else if (hash.startsWith("#/receipt/")) await renderReceipt(hash.slice("#/receipt/".length));
    else renderProducts();
  } catch (err) {
    showError(err.message);
  }
}

async function start() {
  try {
    [products, customers] = await Promise.all([api("/api/products"), api("/api/customers")]);
  } catch (err) {
    showError(err.message);
    return;
  }
  const select = $("customer-select");
  select.innerHTML = customers.map((c) => `<option value="${c.id}">${esc(c.name)}</option>`).join("");
  if (!customers.some((c) => c.id === customerId)) customerId = "returning-customer-01";
  select.value = customerId;
  select.addEventListener("change", () => { customerId = select.value; render(); });
  window.addEventListener("hashchange", render);
  render();
}

start();
