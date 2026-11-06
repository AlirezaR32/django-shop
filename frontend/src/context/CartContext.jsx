import { createContext, useContext, useEffect, useState, useCallback } from "react";
import { cartApi } from "../services/api";
import { useAuth } from "./AuthContext";

const CartCtx = createContext(null);
export const useCart = () => useContext(CartCtx);

export function CartProvider({ children }) {
  const { isAuthed } = useAuth();
  const [cart, setCart] = useState(null);
  const [loading, setLoading] = useState(false);
  // local guest cart for unauthed
  const [guestItems, setGuestItems] = useState(() => {
    try { return JSON.parse(localStorage.getItem("guest_cart") || "[]"); } catch { return []; }
  });

  const fetchCart = useCallback(async () => {
    if (!isAuthed) return;
    try {
      setLoading(true);
      const data = await cartApi.get();
      setCart(data);
    } catch (e) {
      console.warn("fetch cart failed", e);
    } finally { setLoading(false); }
  }, [isAuthed]);

  useEffect(() => { if (isAuthed) fetchCart(); }, [fetchCart, isAuthed]);

  useEffect(() => {
    localStorage.setItem("guest_cart", JSON.stringify(guestItems));
  }, [guestItems]);

  const count = isAuthed ? (cart?.items?.length ?? 0) : guestItems.length;
  const items = isAuthed ? (cart?.items ?? []) : guestItems;

  const addToCart = async (product, qty = 1) => {
    if (!isAuthed) {
      setGuestItems(prev => {
        const exists = prev.find(i => i.product === product.id || i.product?.id === product.id);
        if (exists) return prev;
        return [...prev, { id: Date.now(), product: product, quantity: qty, product_id: product.id }];
      });
      return { ok: true, guest: true };
    }
    try {
      await cartApi.add(product.id, qty);
      await fetchCart();
      return { ok: true };
    } catch (e) {
      const msg = e?.response?.data?.detail || "خطا در افزودن به سبد";
      return { ok: false, msg };
    }
  };

  const updateQty = async (itemId, qty) => {
    if (!isAuthed) {
      setGuestItems(prev => prev.map(i => i.id === itemId ? { ...i, quantity: qty } : i));
      return;
    }
    await cartApi.update(itemId, qty);
    await fetchCart();
  };

  const removeItem = async (itemId) => {
    if (!isAuthed) {
      setGuestItems(prev => prev.filter(i => i.id !== itemId));
      return;
    }
    await cartApi.remove(itemId);
    await fetchCart();
  };

  const applyOff = async (code) => {
    if (!isAuthed) throw new Error("ابتدا وارد شوید");
    return cartApi.applyOff(code);
  };

  return (
    <CartCtx.Provider value={{ cart, items, count, loading, fetchCart, addToCart, updateQty, removeItem, applyOff, isAuthed, guestItems }}>
      {children}
    </CartCtx.Provider>
  );
}
