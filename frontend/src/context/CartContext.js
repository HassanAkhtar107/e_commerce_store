"use client";

import React, { createContext, useContext, useState, useEffect } from "react";
import { api } from "@/Services/api";

const CartContext = createContext();

export const CartProvider = ({ children }) => {
  const [cart, setCart] = useState({ items: [], total_price: 0, total_items: 0 });
  const [isCartOpen, setIsCartOpen] = useState(false);
  const [loading, setLoading] = useState(true);

  // Initialize session ID if not existing
  useEffect(() => {
    if (typeof window !== "undefined") {
      let sessionId = localStorage.getItem("session_id");
      if (!sessionId) {
        sessionId = "sess_" + Math.random().toString(36).substring(2) + Date.now().toString(36);
        localStorage.setItem("session_id", sessionId);
      }
      fetchCart();
    }
  }, []);

  const fetchCart = async () => {
    try {
      setLoading(true);
      const data = await api.getCart();
      if (data) {
        setCart(data);
      }
    } catch (err) {
      console.warn("Using fallback local cart", err);
    } finally {
      setLoading(false);
    }
  };

  const addToCart = async (product, quantity = 1) => {
    try {
      // Optimistic update
      setCart((prev) => {
        const existingIndex = prev.items.findIndex((item) => item.product?.id === product.id);
        let newItems = [...prev.items];
        if (existingIndex > -1) {
          newItems[existingIndex] = {
            ...newItems[existingIndex],
            quantity: newItems[existingIndex].quantity + quantity,
            subtotal: (Number(product.current_price || product.price) * (newItems[existingIndex].quantity + quantity))
          };
        } else {
          newItems.push({
            id: Date.now(),
            product: product,
            quantity: quantity,
            subtotal: Number(product.current_price || product.price) * quantity
          });
        }
        const newCount = newItems.reduce((acc, item) => acc + item.quantity, 0);
        const newTotal = newItems.reduce((acc, item) => acc + Number(item.subtotal || 0), 0);
        return { ...prev, items: newItems, total_items: newCount, total_price: newTotal };
      });

      // Backend sync
      if (product.id) {
        const updatedCart = await api.addToCart(product.id, quantity);
        if (updatedCart && updatedCart.items) {
          setCart(updatedCart);
        }
      }
    } catch (err) {
      console.error("Error adding to cart:", err);
    }
  };

  const updateQuantity = async (itemId, quantity) => {
    try {
      setCart((prev) => {
        const newItems = prev.items
          .map((item) => {
            if (item.id === itemId) {
              if (quantity <= 0) return null;
              const price = Number(item.product?.current_price || item.product?.price || 0);
              return { ...item, quantity, subtotal: price * quantity };
            }
            return item;
          })
          .filter(Boolean);

        const newCount = newItems.reduce((acc, item) => acc + item.quantity, 0);
        const newTotal = newItems.reduce((acc, item) => acc + Number(item.subtotal || 0), 0);
        return { ...prev, items: newItems, total_items: newCount, total_price: newTotal };
      });

      const updatedCart = await api.updateCartItem(itemId, quantity);
      if (updatedCart && updatedCart.items) {
        setCart(updatedCart);
      }
    } catch (err) {
      console.error("Error updating quantity:", err);
    }
  };

  const removeFromCart = async (itemId) => {
    try {
      setCart((prev) => {
        const newItems = prev.items.filter((item) => item.id !== itemId);
        const newCount = newItems.reduce((acc, item) => acc + item.quantity, 0);
        const newTotal = newItems.reduce((acc, item) => acc + Number(item.subtotal || 0), 0);
        return { ...prev, items: newItems, total_items: newCount, total_price: newTotal };
      });

      const updatedCart = await api.removeCartItem(itemId);
      if (updatedCart && updatedCart.items) {
        setCart(updatedCart);
      }
    } catch (err) {
      console.error("Error removing item:", err);
    }
  };

  const clearCart = async () => {
    try {
      setCart({ items: [], total_price: 0, total_items: 0 });
      await api.clearCart();
    } catch (err) {
      console.error("Error clearing cart:", err);
    }
  };

  return (
    <CartContext.Provider
      value={{
        cart,
        cartItems: cart.items || [],
        cartCount: cart.total_items || 0,
        cartTotal: cart.total_price || 0,
        addToCart,
        updateQuantity,
        removeFromCart,
        clearCart,
        isCartOpen,
        setIsCartOpen,
        loading,
        fetchCart,
      }}
    >
      {children}
    </CartContext.Provider>
  );
};

export const useCart = () => useContext(CartContext);
