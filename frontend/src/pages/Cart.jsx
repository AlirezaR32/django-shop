import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Trash2, Plus, Minus, Tag, Truck, ChevronLeft, ShoppingBag, ShieldCheck } from "lucide-react";
import { SimpleHeader } from "../components/Header";
import { useCart } from "../context/CartContext";
import { formatPrice } from "../utils/format";
import { useAuth } from "../context/AuthContext";

export default function Cart() {
  const { items, count, updateQty, removeItem, applyOff, isAuthed, cart } = useCart();
  const { isAuthed: authed } = useAuth();
  const [code, setCode] = useState("");
  const [applyMsg, setApplyMsg] = useState("");
  const [applyErr, setApplyErr] = useState("");
  const navigate = useNavigate();

  const subtotal = items.reduce((sum, it) => {
    const p = it.product || {};
    const price = p.final_price ?? p.price ?? 0;
    const q = Number(it.quantity || 1);
    return sum + Number(price) * q;
  }, 0);

  // if cart has off_code, calc discount
  let discount = 0;
  let offPercent = 0;
  if (cart?.off_code?.off_percent) {
    offPercent = parseFloat(cart.off_code.off_percent);
    discount = Math.round(subtotal * offPercent);
  }
  const shipping = subtotal > 500000 ? 0 : 35000;
  const total = subtotal - discount + shipping;

  const handleApply = async () => {
    setApplyMsg(""); setApplyErr("");
    if (!code.trim()) return;
    if (!authed) { setApplyErr("ابتدا وارد حساب شوید"); return; }
    try {
      await applyOff(code.trim());
      setApplyMsg("کد با موفقیت اعمال شد!");
    } catch (e) {
      setApplyErr(e?.response?.data?.detail || "کد نامعتبر یا منقضی شده");
    }
  };

  if (count === 0) {
    return (
      <div className="bg-white min-h-screen flex flex-col">
        <SimpleHeader title="سبد خرید" subtitle="0 کالا" />
        <div className="flex-1 grid place-items-center p-8 text-center">
          <div>
            <div className="size-24 rounded-full bg-zinc-50 border border-zinc-100 grid place-items-center mx-auto">
              <ShoppingBag size={36} className="text-zinc-300" />
            </div>
            <h3 className="font-black text-base mt-4">سبد خرید شما خالی است!</h3>
            <p className="text-sm text-zinc-500 mt-1 leading-6">می‌توانید محصولات جذاب را از فروشگاه<br />مشاهده و به سبد اضافه کنید.</p>
            <Link to="/" className="inline-flex mt-6 bg-zinc-900 text-white font-bold text-sm px-8 py-3 rounded-full">شروع خرید</Link>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-[#F8F8F9] min-h-screen pb-[140px]">
      <SimpleHeader title="سبد خرید" subtitle={`${count} کالا در سبد شما`} />

      {/* items */}
      <div className="px-4 mt-4 space-y-3">
        {items.map((it) => {
          const p = it.product || { title: "محصول", price: 1000000, final_price: 1000000, brand: { name: "برند" } };
          const id = it.id;
          const qty = Number(it.quantity || 1);
          const img = p.images?.[0]?.image
            ? (p.images[0].image.startsWith("http") ? p.images[0].image : `http://localhost:8000${p.images[0].image}`)
            : `https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=200&h=200&fit=crop`;
          return (
            <div key={id} className="bg-white rounded-[20px] border border-zinc-100 p-3 flex gap-3">
              <Link to={`/product/${p.id ?? 1}`} className="shrink-0">
                <img src={img} alt={p.title} className="size-[96px] rounded-2xl bg-zinc-50 object-cover border border-zinc-100" />
              </Link>
              <div className="flex-1 min-w-0 flex flex-col">
                <div className="text-[11px] text-zinc-500">{p.brand?.name || "برند"} • {p.category?.name || "دسته"}</div>
                <Link to={`/product/${p.id ?? 1}`} className="font-bold text-[13px] leading-5 line-clamp-2">{p.title}</Link>
                <div className="flex items-center gap-2 mt-1">
                  <span className="size-1.5 bg-emerald-500 rounded-full" /> <span className="text-xs text-emerald-600 font-bold">موجود در انبار</span>
                </div>
                <div className="flex items-end justify-between mt-auto pt-2">
                  <div>
                    <div className="font-black text-sm price-fa">{formatPrice(p.final_price ?? p.price)} <span className="text-[11px] font-bold text-zinc-500">تومان</span></div>
                    {p.price !== p.final_price && <div className="text-[11px] text-zinc-400 line-through price-fa">{formatPrice(p.price)}</div>}
                  </div>
                  <div className="flex items-center gap-1.5">
                    <div className="flex items-center bg-zinc-50 rounded-full border border-zinc-100 p-1">
                      <button onClick={() => updateQty(id, qty + 1)} className="size-7 rounded-full bg-white border grid place-items-center shadow-sm"><Plus size={12} /></button>
                      <span className="w-7 text-center font-black text-sm">{qty}</span>
                      <button onClick={() => qty > 1 ? updateQty(id, qty - 1) : removeItem(id)} className="size-7 rounded-full bg-white border grid place-items-center shadow-sm"><Minus size={12} /></button>
                    </div>
                    <button onClick={() => removeItem(id)} className="size-8 rounded-full bg-red-50 text-red-600 grid place-items-center border border-red-100">
                      <Trash2 size={14} />
                    </button>
                  </div>
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* off code */}
      <div className="px-4 mt-4">
        <div className="bg-white rounded-[20px] border border-zinc-100 p-4">
          <div className="flex items-center gap-2 font-bold text-sm">
            <div className="size-8 rounded-full bg-amber-50 grid place-items-center border border-amber-100"><Tag size={16} className="text-amber-600" /></div>
            کد تخفیف دارید؟
          </div>
          <div className="flex gap-2 mt-3">
            <input value={code} onChange={e => setCode(e.target.value)} placeholder="مثلاً: OFF20" className="flex-1 bg-zinc-50 border border-zinc-200 rounded-full px-4 py-3 text-sm outline-none focus:border-zinc-900 placeholder:text-zinc-400" />
            <button onClick={handleApply} className="bg-zinc-900 text-white font-black text-sm px-6 rounded-full shrink-0 hover:bg-black">اعمال</button>
          </div>
          {applyMsg && <div className="text-xs text-emerald-600 font-bold mt-2">{applyMsg}</div>}
          {applyErr && <div className="text-xs text-red-600 font-bold mt-2">{applyErr}</div>}
          {!isAuthed && <div className="text-xs text-zinc-500 mt-2">برای استفاده از کد تخفیف وارد حساب شوید.</div>}
        </div>
      </div>

      {/* summary */}
      <div className="px-4 mt-4">
        <div className="bg-white rounded-[20px] border border-zinc-100 p-4">
          <h3 className="font-black text-sm">جزئیات پرداخت</h3>
          <div className="mt-3 space-y-3 text-sm">
            <div className="flex justify-between"><span className="text-zinc-500">جمع سبد خرید</span><span className="font-bold price-fa">{formatPrice(subtotal)} تومان</span></div>
            {discount > 0 && <div className="flex justify-between text-emerald-600"><span>سود شما از تخفیف ({Math.round(offPercent * 100)}٪)</span><span className="font-black price-fa">-{formatPrice(discount)} تومان</span></div>}
            <div className="flex justify-between"><span className="text-zinc-500 flex items-center gap-1"><Truck size={14} /> هزینه ارسال</span><span className={`font-bold ${shipping === 0 ? "text-emerald-600" : ""}`}>{shipping === 0 ? "رایگان" : `${formatPrice(shipping)} تومان`}</span></div>
            <div className="h-px bg-zinc-100" />
            <div className="flex justify-between text-base"><span className="font-black">مبلغ قابل پرداخت</span><span className="font-black price-fa text-[#E11D48]">{formatPrice(total)} تومان</span></div>
          </div>
          <div className="mt-3 flex items-center gap-2 bg-emerald-50 border border-emerald-100 rounded-full px-3 py-2 text-xs text-emerald-800">
            <ShieldCheck size={14} /> پرداخت امن با رمز پویا • ضمانت بازگشت وجه
          </div>
        </div>
      </div>

      {/* sticky checkout */}
      <div className="fixed bottom-0 inset-x-0 z-40 flex justify-center pointer-events-none">
        <div className="w-full max-w-[480px] bg-white border-t border-zinc-100 px-4 py-3 flex items-center gap-3 shadow-[0_-8px_24px_rgba(0,0,0,0.08)] pointer-events-auto pb-[calc(0.75rem+env(safe-area-inset-bottom))]">
          <div className="flex-1">
            <div className="text-xs text-zinc-500">مبلغ نهایی</div>
            <div className="font-black price-fa">{formatPrice(total)} تومان</div>
          </div>
          <button onClick={() => navigate("/checkout")} className="flex-1 bg-[#E11D48] text-white font-black py-3.5 rounded-full flex items-center justify-center gap-2 hover:bg-[#be123c] transition-colors">
            ادامه جهت تسویه حساب <ChevronLeft size={18} />
          </button>
        </div>
      </div>
    </div>
  );
}
