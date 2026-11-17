import { request } from './http.js';
import { element, button, errorMessage } from './common.js';
import { createCartQueue } from './cart-queue.js';

const session = crypto.randomUUID();
const $ = (id) => document.getElementById(id);
const groups = [['month-offers', 'Month offers'], ['best-sellers', 'Best sellers'], ['home', 'Home']];
let cart = null;
let generation = 0;
let pages = {};
const enqueueCart = createCartQueue();

function runCart(operation) {
  return enqueueCart(async () => {
    await operation();
    updateCount();
    renderCart();
  });
}

function notice(message, error = false) {
  $('notice').hidden = !message;
  $('notice').className = error ? 'notice error' : 'notice';
  $('notice').textContent = message;
}
function showError(error) {
  const code = error.code || 'NETWORK_ERROR';
  const message = `${code}: ${errorMessage(code, error.message)}`;
  notice(message, true);
  if ($('details').open) {
    let alert = $('details-content').querySelector('[role=alert]');
    if (!alert) {
      alert = element('p', 'notice error');
      alert.setAttribute('role', 'alert');
      $('details-content').append(alert);
    }
    alert.textContent = message;
  }
}
function placeholder() { return element('div', 'placeholder', 'Product image'); }
function money(price, currency) { return `${price} ${currency}`; }
function view(name) {
  $('browse-view').hidden = name !== 'browse';
  $('cart-view').hidden = name !== 'cart';
  $('browse-link').classList.toggle('active', name === 'browse');
  $('cart-link').classList.toggle('active', name === 'cart');
}
function params(block, tag) {
  const query = new URLSearchParams({ block, items: 20 });
  const category = $('category').value, selectedTag = tag || $('tag').value;
  if (category) query.set('category', category);
  if (selectedTag) query.set('tag', selectedTag);
  if ($('search').value.trim()) query.set('name', $('search').value.trim());
  query.set('sort', $('sort').value || 'name:asc');
  return query;
}
function productCard(product) {
  const card = element('article', 'product-card');
  card.append(placeholder());
  const content = element('div', 'card-content');
  content.append(element('h3', '', product.name), element('p', 'price', money(product.unitPrice, product.currency.code)), button('See details →', () => details(product.code), 'text-button'));
  card.append(content);
  return card;
}
async function renderGroup(container, key, title, currentGeneration) {
  const block = pages[key] || 1;
  const result = await request(`/products?${params(block, key === 'results' ? '' : key)}`);
  if (currentGeneration !== generation) return;
  const section = element('section', 'product-section');
  section.append(element('div', 'section-heading', title));
  const grid = element('div', 'product-grid');
  result.products.forEach((product) => grid.append(productCard(product)));
  section.append(grid);
  if (!result.products.length) section.append(element('p', 'muted', 'No products found.'));
  const pagination = element('div', 'pagination');
  const previous = button('← Previous', () => { pages[key] = block - 1; loadProducts(); });
  previous.disabled = block <= 1;
  const next = button('Next →', () => { pages[key] = block + 1; loadProducts(); });
  next.disabled = block * result.items >= result.total;
  pagination.append(previous, element('span', '', `Page ${block} of ${Math.max(1, Math.ceil(result.total / result.items))} · ${result.total} products`), next);
  section.append(pagination);
  container.append(section);
}
async function loadProducts() {
  const currentGeneration = ++generation;
  const container = $('products');
  container.replaceChildren(element('p', 'muted', 'Loading products…'));
  const filtered = $('category').value || $('tag').value || $('sort').value || $('search').value.trim();
  const target = document.createDocumentFragment();
  try {
    const sections = filtered ? [['results', 'Products']] : groups;
    for (const [key, title] of sections) await renderGroup(target, key, title, currentGeneration);
    if (currentGeneration === generation) container.replaceChildren(target);
  } catch (error) { if (currentGeneration === generation) { container.replaceChildren(); showError(error); } }
}
async function loadFilterOptions() {
  try {
    const categories = new Set(), tags = new Set();
    let block = 1, result;
    do {
      result = await request(`/products?${new URLSearchParams({ block, items: 20 })}`);
      result.products.forEach((product) => { product.categories.forEach((value) => categories.add(value)); product.tags.forEach((value) => tags.add(value)); });
      block++;
    } while ((block - 1) * result.items < result.total);
    for (const [id, values] of [['category', categories], ['tag', tags]]) {
      [...values].sort().forEach((value) => { const option = element('option', '', value); option.value = value; $(id).append(option); });
    }
  } catch (error) { showError(error); }
}
async function details(code) {
  try {
    const product = await request(`/products/${encodeURIComponent(code)}`);
    const content = $('details-content');
    content.replaceChildren();
    const close = button('×', () => $('details').close(), 'close'); close.setAttribute('aria-label', 'Close product details');
    const quantity = element('input'); quantity.type = 'number'; quantity.min = '1'; quantity.step = '1'; quantity.value = '1'; quantity.id = 'quantity';
    const label = element('label', '', 'Quantity'); label.htmlFor = 'quantity'; label.append(quantity);
    const add = button('Add to Cart', async () => {
      if (add.disabled || !quantity.reportValidity() || !Number.isSafeInteger(Number(quantity.value))) return;
      const selectedQuantity = Number(quantity.value);
      add.disabled = true;
      try {
        await runCart(async () => {
          if (!cart) cart = await request('/carts', { method: 'POST', session });
          cart = await request(`/carts/${encodeURIComponent(cart.code)}/items`, { method: 'POST', session, body: { productCode: product.code, quantity: selectedQuantity } });
        });
        $('details').close(); notice(`${product.name} added to your cart.`);
      } catch (error) { showError(error); }
      finally { add.disabled = false; }
    }, 'button primary');
    const actions = element('div', 'detail-actions'); actions.append(label, add);
    content.append(close, placeholder(), element('h2', '', product.name), element('p', 'price', money(product.unitPrice, product.currency.code)), element('h3', 'description-label', 'Description'), element('p', '', product.description), actions);
    $('details').showModal();
  } catch (error) { showError(error); }
}
function updateCount() { $('cart-count').textContent = cart ? `(${cart.items.reduce((sum, item) => sum + item.quantity, 0)})` : ''; }
function renderCart() {
  const content = $('cart-content'); content.replaceChildren();
  if (!cart || !cart.items.length) { content.append(element('p', 'empty', 'Your cart is empty.')); return; }
  for (const item of cart.items) {
    const row = element('article', 'cart-item');
    row.append(element('h2', '', item.name), element('p', '', `${money(item.unitPrice, item.currency)} · Quantity: ${item.quantity}`), button('Remove item', async () => {
      try { await runCart(async () => { cart = await request(`/carts/${encodeURIComponent(cart.code)}/items/${encodeURIComponent(item.productCode)}`, { method: 'PUT', session, body: { quantity: 0 } }); }); }
      catch (error) { showError(error); }
    }, 'text-button'));
    content.append(row);
  }
  const footer = element('div', 'cart-footer');
  const totals = element('div'); cart.totals.forEach((total) => totals.append(element('p', 'total', `Total: ${money(total.amount, total.currency)}`)));
  const checkout = button('Checkout', async () => {
    if (checkout.disabled) return;
    checkout.disabled = true;
    try {
      await runCart(async () => {
        await request(`/carts/${encodeURIComponent(cart.code)}/checkout`, { method: 'POST', session });
        cart = null; updateCount(); renderCart();
        notice('Checkout complete.');
        cart = await request('/carts', { method: 'POST', session });
      });
    } catch (error) { showError(error); checkout.disabled = false; }
  }, 'button primary');
  footer.append(totals, checkout); content.append(footer);
}
function resetBrowse(event) {
  event.preventDefault(); $('search').value = '';['category', 'tag', 'sort'].forEach((id) => { $(id).value = ''; }); pages = {}; notice(''); view('browse'); loadProducts();
}
$('logo').addEventListener('click', resetBrowse);
$('browse-link').addEventListener('click', resetBrowse);
$('cart-link').addEventListener('click', async (event) => {
  event.preventDefault(); notice(''); view('cart');
  try { await runCart(async () => { if (!cart) cart = await request('/carts', { method: 'POST', session }); else cart = await request(`/carts/${encodeURIComponent(cart.code)}`, { session }); }); }
  catch (error) { showError(error); }
});
$('search-form').addEventListener('submit', (event) => { event.preventDefault(); pages = {}; notice(''); view('browse'); loadProducts(); });
['category', 'tag', 'sort'].forEach((id) => $(id).addEventListener('change', () => { pages = {}; notice(''); loadProducts(); }));
loadProducts(); loadFilterOptions();
runCart(async () => { cart = await request('/carts', { method: 'POST', session }); }).catch(showError);

