/** Serialise every cart read and write, including initialisation. */
export function createCartQueue() {
  let pending = Promise.resolve();
  return function enqueue(operation) {
    const result = pending.then(operation);
    // A failed request must not prevent subsequent actions from running.
    pending = result.catch(() => {});
    return result;
  };
}
