import { useEffect, useState } from "react";
import { SimpleHeader } from "../components/Header";
import { orderApi } from "../services/api";
import { Package, Truck, CheckCircle2, XCircle, RotateCcw } from "lucide-react";
import { formatPrice } from "../utils/format";

const TABS = [
  { key: "", label: "همه" },
  { key: "PROCESSING", label: "جاری" },
  { key: "COMPLETED", label: "تحویل شده" },
  { key: "CANCELLED", label: "لغو شده" },
];

export default function Orders() {
  const [tab, setTab] = useState("");
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(false);

  const fetch = async (status) => {
    setLoading(true);
    try {
      const data = await orderApi.list(status || undefined);
      const list = Array.isArray(data) ? data : (data.results ?? []);
      setOrders(list);
    } catch {
      setOrders([]);
    } finally { setLoading(false); }
  };
  useEffect(() => { fetch(tab); }, [tab]);

  const cancel = async (id) => {
    try { await orderApi.cancel(id); fetch(tab); } catch {}
  };

  return (
    <div className="bg-[#F8F8F9] min-h-screen pb-8">
      <SimpleHeader title="سفارش‌های من" subtitle={`${orders.length} سفارش`} />
      <div className="px-4 mt-3 flex gap-2 overflow-x-auto scrollbar-hide">
        {TABS.map(t => (
          <button key={t.key} onClick={() => setTab(t.key)} className={`shrink-0 px-5 py-2.5 rounded-full text-xs font-black border ${tab === t.key ? "bg-zinc-900 text-white border-zinc-900" : "bg-white border-zinc-200 text-zinc-700"}`}>{t.label}</button>
        ))}
      </div>

      <div className="px-4 mt-4 space-y-3">
        {loading ? (
          <div className="bg-white rounded-2xl border border-zinc-100 p-8 text-center text-sm text-zinc-500">در حال بارگذاری...</div>
        ) : orders.length === 0 ? (
          <div className="bg-white rounded-[20px] border border-zinc-100 p-8 text-center">
            <div className="size-16 rounded-full bg-zinc-50 border border-zinc-100 grid place-items-center mx-auto"><Package size={28} className="text-zinc-300" /></div>
            <div className="font-bold text-sm mt-3">سفارشی یافت نشد</div>
            <div className="text-xs text-zinc-500 mt-1">در این دسته هنوز سفارشی ثبت نکرده‌اید.</div>
          </div>
        ) : (
          orders.map(o => (
            <div key={o.id} className="bg-white rounded-[20px] border border-zinc-100 p-4">
              <div className="flex items-center justify-between">
                <div className="font-black text-sm">سفارش #{o.id}</div>
                <span className={`text-[11px] font-black px-3 py-1 rounded-full border ${
                  o.status === "PROCESSING" ? "bg-amber-50 text-amber-700 border-amber-100" :
                  o.status === "COMPLETED" ? "bg-emerald-50 text-emerald-700 border-emerald-100" :
                  o.status === "CANCELLED" ? "bg-red-50 text-red-600 border-red-100" :
                  "bg-zinc-50 text-zinc-600 border-zinc-100"
                }`}>{o.status || "PROCESSING"}</span>
              </div>
              <div className="text-xs text-zinc-500 mt-1">{o.ordered_at ? new Date(o.ordered_at).toLocaleDateString("fa-IR") : "امروز"} • {o.total_amount ? `${formatPrice(o.total_amount)} تومان` : ""}</div>
              {o.items?.length > 0 && (
                <div className="mt-3 space-y-2">
                  {o.items.slice(0, 3).map(it => (
                    <div key={it.id} className="flex items-center gap-2 text-xs">
                      <div className="size-8 rounded-full bg-zinc-50 border border-zinc-100 grid place-items-center">📦</div>
                      <span className="font-bold truncate flex-1">{it.product ?? `محصول #${it.product}`}</span>
                      <span className="text-zinc-500">× {it.quantity}</span>
                    </div>
                  ))}
                </div>
              )}
              <div className="flex gap-2 mt-4">
                {o.status === "PROCESSING" && <button onClick={() => cancel(o.id)} className="flex-1 bg-white border border-zinc-200 font-bold py-2.5 rounded-full text-xs">لغو سفارش</button>}
                <button className="flex-1 bg-zinc-900 text-white font-bold py-2.5 rounded-full text-xs">جزئیات</button>
              </div>
            </div>
          ))
        )}
      </div>

      {/* footer info */}
      <div className="mx-4 mt-6 bg-white border border-zinc-100 rounded-2xl p-4 flex items-center gap-3 text-xs">
        <Truck size={16} className="text-zinc-700" />
        <span className="font-bold">پیگیری مرسوله با کد سفارش از پشتیبانی: 021-12345678</span>
      </div>
    </div>
  );
}
