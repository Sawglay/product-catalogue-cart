import assert from 'node:assert/strict';
import { test } from 'node:test';
import { createCartQueue } from '../scripts/cart-queue.js';

test('creation, mutation and read run in order despite a delayed response', async () => {
  const enqueue = createCartQueue();
  let release;
  const response = new Promise((resolve) => { release = resolve; });
  const events = [];
  let cart;
  const creation = enqueue(async () => {
    events.push('create');
    await response;
    cart = { quantity: 0 };
  });
  const addition = enqueue(async () => {
    events.push('add');
    cart = { quantity: cart.quantity + 2 };
  });
  const read = enqueue(async () => {
    events.push('read');
    assert.equal(cart.quantity, 2);
  });
  await Promise.resolve();
  assert.deepEqual(events, ['create']);
  release();
  await Promise.all([creation, addition, read]);
  assert.deepEqual(events, ['create', 'add', 'read']);
});

test('a rejected request reaches its caller and does not block later actions', async () => {
  const enqueue = createCartQueue();
  const failure = new Error('Request failed');
  const failed = enqueue(async () => { throw failure; });
  const next = enqueue(async () => 'cart refreshed');
  await assert.rejects(failed, (error) => error === failure);
  assert.equal(await next, 'cart refreshed');
});
