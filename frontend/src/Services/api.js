const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api";

const getHeaders = () => {
  const headers = {
    "Content-Type": "application/json",
  };
  if (typeof window !== "undefined") {
    const token = localStorage.getItem("token");
    if (token) {
      headers["Authorization"] = `Token ${token}`;
    }
    const sessionId = localStorage.getItem("session_id");
    if (sessionId) {
      headers["X-Session-ID"] = sessionId;
    }
  }
  return headers;
};

// Generic fetch handler
const request = async (endpoint, options = {}) => {
  const url = `${API_BASE_URL}${endpoint}`;
  const config = {
    ...options,
    headers: {
      ...getHeaders(),
      ...options.headers,
    },
  };

  try {
    const response = await fetch(url, config);
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || errorData.error || `HTTP error! status: ${response.status}`);
    }
    return await response.json();
  } catch (err) {
    console.error(`API Request Error [${endpoint}]:`, err);
    throw err;
  }
};

export const api = {
  // Products Catalog APIs
  getProducts: (params = "") => request(`/products/${params}`),
  getProductBySlug: (slug) => request(`/products/${slug}/`),
  getCategories: () => request(`/categories/`),
  getBrands: () => request(`/brands/`),
  addReview: (productSlug, reviewData) => request(`/products/${productSlug}/add_review/`, {
    method: "POST",
    body: JSON.stringify(reviewData)
  }),

  // Cart APIs
  getCart: () => request(`/cart/`),
  addToCart: (productId, quantity = 1) => request(`/cart/add_item/`, {
    method: "POST",
    body: JSON.stringify({ product_id: productId, quantity })
  }),
  updateCartItem: (itemId, quantity) => request(`/cart/update_item/`, {
    method: "POST",
    body: JSON.stringify({ item_id: itemId, quantity })
  }),
  removeCartItem: (itemId) => request(`/cart/remove_item/`, {
    method: "POST",
    body: JSON.stringify({ item_id: itemId })
  }),
  clearCart: () => request(`/cart/clear/`, { method: "POST" }),

  // Orders & Checkout APIs
  createOrder: (orderData) => request(`/orders/create_order/`, {
    method: "POST",
    body: JSON.stringify(orderData)
  }),
  getOrders: () => request(`/orders/`),
  getDashboardStats: () => request(`/orders/dashboard_stats/`),
  createPaymentIntent: (orderNumber) => request(`/payments/create-intent/`, {
    method: "POST",
    body: JSON.stringify({ order_number: orderNumber })
  }),

  // Auth APIs
  login: (credentials) => request(`/login/`, {
    method: "POST",
    body: JSON.stringify(credentials)
  }),
  signup: (userData) => request(`/signup/`, {
    method: "POST",
    body: JSON.stringify(userData)
  }),
  getUserProfile: () => request(`/users/me/`),
};
