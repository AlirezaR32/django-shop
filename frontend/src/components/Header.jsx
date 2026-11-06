import { Search, Bell, MapPin, Heart, ArrowRight } from "lucide-react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { useState } from "react";

export function HomeHeader({ onSearch }) {
  const [q, setQ] = useState("");
  return (
    <div className="sticky top-0 z-30 bg-white">
      {/* top bar */}
      <div className="flex items-center justify-between px-4 pt-3 pb-2">
        <div className="flex items-center gap-2 text-zinc-700">
          <div className="size-8 rounded-full bg-zinc-900 text-white grid place-items-center text-xs font-bold">فا</div>
          <div className="leading-tight">
            <div className="text-[11px] text-zinc-500 flex items-center gap-1">
              <MapPin size={12} /> ارسال به
            </div>
            <div className="text-sm font-bold">تهران، خیابان ولیعصر</div>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <Link to="/cart" className="size-9 rounded-full bg-zinc-50 grid place-items-center border border-zinc-100">
            <Bell size={18} className="text-zinc-700" />
          </Link>
          <div className="size-9 rounded-full bg-zinc-50 grid place-items-center border border-zinc-100">
            <Heart size={18} className="text-zinc-700" />
          </div>
        </div>
      </div>

      {/* search */}
      <div className="px-4 pb-3">
        <div className="flex items-center gap-3 bg-[#F3F3F5] rounded-2xl px-3 py-2.5 border border-zinc-100">
          <Search size={18} className="text-zinc-400 shrink-0" />
          <input
            value={q}
            onChange={(e) => setQ(e.target.value)}
            onKeyDown={(e) => { if (e.key === "Enter") onSearch?.(q); }}
            placeholder="جستجو در محصولات — مثلاً گوشی، لباس..."
            className="flex-1 bg-transparent outline-none text-sm placeholder:text-zinc-400"
          />
          {q && <button onClick={() => { setQ(""); onSearch?.("") }} className="text-xs bg-white px-2 py-1 rounded-full border">پاک</button>}
          <button onClick={() => onSearch?.(q)} className="bg-[#E11D48] text-white text-sm font-bold px-4 py-1.5 rounded-xl shrink-0">جستجو</button>
        </div>
      </div>
    </div>
  );
}

export function SimpleHeader({ title, subtitle, back = true, action }) {
  const nav = useNavigate();
  const loc = useLocation();
  return (
    <div className="sticky top-0 z-30 bg-white/90 backdrop-blur border-b border-zinc-100">
      <div className="flex items-center gap-3 px-4 py-3">
        {back && (
          <button onClick={() => loc.key !== "default" ? nav(-1) : nav("/")} className="size-9 rounded-full bg-zinc-50 grid place-items-center border border-zinc-100">
            <ArrowRight size={18} />
          </button>
        )}
        <div className="flex-1">
          <div className="font-extrabold text-[15px] leading-none">{title}</div>
          {subtitle && <div className="text-xs text-zinc-500 mt-1">{subtitle}</div>}
        </div>
        {action}
      </div>
    </div>
  );
}
