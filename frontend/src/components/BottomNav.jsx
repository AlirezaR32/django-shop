import { NavLink, useLocation } from "react-router-dom";
import { House, Search, ShoppingBag, User, LayoutGrid } from "lucide-react";
import { useCart } from "../context/CartContext";

export default function BottomNav() {
  const { count } = useCart();
  const location = useLocation();

  const tabs = [
    { to: "/", label: "خانه", icon: House },
    { to: "/categories", label: "دسته‌ها", icon: LayoutGrid },
    { to: "/cart", label: "سبد خرید", icon: ShoppingBag, badge: count },
    { to: "/profile", label: "حساب", icon: User },
  ];

  return (
    <nav className="fixed bottom-0 inset-x-0 z-40 flex justify-center pointer-events-none">
      <div className="w-full max-w-[480px] pointer-events-auto bg-white border-t border-zinc-100 px-2 pt-2 pb-[calc(0.5rem+env(safe-area-inset-bottom))] rounded-t-[20px] shadow-[0_-8px_24px_rgba(0,0,0,0.06)]">
        <div className="flex items-center justify-around">
          {tabs.map(({ to, label, icon: Icon, badge }) => {
            const active = location.pathname === to || (to !== "/" && location.pathname.startsWith(to));
            return (
              <NavLink
                key={to}
                to={to}
                className={`flex flex-col items-center gap-1 px-4 py-1.5 rounded-2xl transition-all ${active ? "text-[#E11D48] bg-rose-50" : "text-zinc-400"}`}
              >
                <div className="relative">
                  <Icon size={22} strokeWidth={active ? 2.2 : 1.8} />
                  {badge > 0 && (
                    <span className="absolute -top-1.5 -right-2 bg-[#E11D48] text-white text-[10px] leading-none px-1.5 py-1 rounded-full min-w-[16px] text-center font-bold">
                      {badge > 9 ? "9+" : badge}
                    </span>
                  )}
                </div>
                <span className={`text-[11px] ${active ? "font-bold" : "font-medium"}`}>{label}</span>
              </NavLink>
            );
          })}
        </div>
        <div className="mx-auto mt-2 h-1 w-24 bg-zinc-900 rounded-full opacity-10" />
      </div>
    </nav>
  );
}
