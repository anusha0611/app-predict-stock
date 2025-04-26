const USER_SERVICE_URL = import.meta.env.VITE_USER_SERVICE_URL;
const STOCK_DATA_SERVICE_URL = import.meta.env.VITE_STOCK_DATA_SERVICE_URL;

export const api = {
  // User Service APIs
  register: async (data) =>
    fetch(`${USER_SERVICE_URL}/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    }),

  // Stock Data Service APIs
  fetchStocks: async () =>
    fetch(`${STOCK_DATA_SERVICE_URL}/stocks`).then((res) => res.json()),

  addStock: async (data) =>
    fetch(`${STOCK_DATA_SERVICE_URL}/stocks`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    }),
};
