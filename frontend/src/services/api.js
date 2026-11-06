import axios from "axios";

// In dev, vite proxies /api -> localhost:8000, so we can use /api as base
// In production fallback, use VITE_API_URL env or localhost:8000
const baseURL = import.meta.env.VITE_API_URL
  ? import.meta.env.VITE_API_URL
  : "/api";

const api = axios.create({
  baseURL,
  timeout: 8000,
  headers: { "Content-Type": "application/json" },
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("access");
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

api.interceptors.response.use(
  (r) => r,
  async (error) => {
    const original = error.config;
    if (
      error.response?.status === 401 &&
      !original._retry &&
      localStorage.getItem("refresh")
    ) {
      original._retry = true;
      try {
        const res = await axios.post(`${baseURL}/auth/token/refresh`, {
          refresh: localStorage.getItem("refresh"),
        });
        const newAccess = res.data.access;
        localStorage.setItem("access", newAccess);
        original.headers.Authorization = `Bearer ${newAccess}`;
        return api(original);
      } catch (e) {
        localStorage.removeItem("access");
        localStorage.removeItem("refresh");
        // not redirect, just reject
      }
    }
    return Promise.reject(error);
  }
);

export default api;

// Helpers
export const productsApi = {
  list: (params = {}) => api.get("/products", { params }).then(r => r.data),
  detail: (id) => api.get(`/products/${id}`).then(r => r.data),
};

export const cartApi = {
  get: () => api.get("/cart").then(r => r.data),
  add: (product_id, quantity = 1) => api.post("/cart", { product_id, quantity }).then(r => r.data),
  update: (item_id, quantity) => api.patch(`/cart/${item_id}`, { quantity }).then(r => r.data),
  remove: (item_id) => api.delete(`/cart/${item_id}`).then(r => r.data),
  applyOff: (code) => api.post("/cart/apply-off-code", { code }).then(r => r.data),
};

export const authApi = {
  register: (username, password) => api.post("/auth/register", { username, password }).then(r => r.data),
  login: (username, password) => api.post("/auth/token", { username, password }).then(r => r.data),
  refresh: (refresh) => api.post("/auth/token/refresh", { refresh }).then(r => r.data),
};

export const addressApi = {
  list: () => api.get("/addresses").then(r => r.data),
  create: (data) => api.post("/addresses", data).then(r => r.data),
  update: (id, data) => api.patch(`/addresses/${id}`, data).then(r => r.data),
  remove: (id) => api.delete(`/addresses/${id}`).then(r => r.data),
};

export const orderApi = {
  list: (status) => api.get("/orders/", { params: status ? { status } : {} }).then(r => r.data),
  detail: (id) => api.get(`/orders/${id}`).then(r => r.data),
  checkout: () => api.post("/orders/checkout").then(r => r.data),
  cancel: (id) => api.post(`/orders/${id}/cancell`).then(r => r.data),
};
