export function element(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
}

export function button(label, action, className = 'button secondary') {
  const node = element('button', className, label);
  node.type = 'button';
  node.addEventListener('click', action);
  return node;
}

export function errorMessage(code, fallback) {
  const messages = {
    PRODUCT_NOT_FOUND: 'Product not found.',
    CART_NOT_FOUND: 'Cart not found. Reload the page to create a new session.',
    CART_ITEM_NOT_FOUND: 'Cart item not found.',
    INVALID_SORT: 'Choose a supported sort order.',
    INVALID_REQUEST: 'Check the request and try again.',
    INVALID_SESSION: 'The shopping session is invalid. Reload the page.',
    DATA_CONFLICT: 'The cart has changed. Try again.',
    INTERNAL_ERROR: 'The request could not be completed.',
    NOT_READY: 'The database is unavailable.',
    HTTP_ERROR: 'The requested endpoint is unavailable.',
    REQUEST_FAILED: 'The request failed.',
    NETWORK_ERROR: 'Unable to contact the server.',
  };
  return messages[code] || fallback || messages.REQUEST_FAILED;
}
