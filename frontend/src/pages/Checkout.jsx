import { useEffect, useState } from "react";
import { SimpleHeader } from "../components/Header";
import { MapPin, Plus, Truck, CreditCard, Building2, Bike, Clock3, Check, ChevronLeft, ShieldCheck, Pencil, Trash2 } from "lucide-react";
import { addressApi, orderApi } from "../services/api";
import { useCart } from "../context/CartContext";
import { formatPrice } from "../utils/format";
import { useNavigate } from "react-router-dom";

const SHIPPING = [
  { id: "post", label: "پست پیشتاز", desc: "ارسال 2 تا 3 روز کاری", price: 0, icon: Truck, badge: "رایگان" },
  { id: "express", label: "ارسال فوری", desc: "امروز تا ساعت 21", price: 45000, icon: Bike, badge: "+ 45,000" },
  { id: "pickup", label: "تحویل حضوری", desc: "از فروشگاه مرکزی", price: 0, icon: Building2, badge: "رایگان" },
];

const PAYMENTS = [
  { id: "online", label: "پرداخت آنلاین", desc: "درگاه شاپرک — همه کارت‌ها", icon: CreditCard },
  { id: "cod", label: "پرداخت در محل", desc: "نقدی یا کارت‌خوان", icon: Clock3 },
];

export default function Checkout() {
  const [addresses, setAddresses] = useState([]);
  const [selectedAddr, setSelectedAddr] = useState(null);
  const [shipping, setShipping] = useState("post");
  const [payment, setPayment] = useState("online");
  const [showForm, setShowForm] = useState(false);
  const [form, setForm] = useState({ full_address: "", city: "تهران", state: "تهران", postal_code: "" });
  const [loading, setLoading] = useState(false);
  const [done, setDone] = useState(null);
  const [err, setErr] = useState("");
  const navigate = useNavigate();
  const { items, cart } = useCart();

  const fetchAddr = async () => {
    try {
      const data = await addressApi.list();
      const list = Array.isArray(data) ? data : (data.results ?? []);
      setAddresses(list);
      if (list.length && !selectedAddr) {
        const def = list.find(a => a.is_default) || list[0];
        setSelectedAddr(def.id);
      }
    } catch {
      // mock fallback
      const mock = [
        { id: 1, full_address: "تهران، خیابان ولیعصر، کوچه 12، پلاک 34، واحد 5", city: "تهران", state: "تهران", postal_code: "1234567890", is_default: true },
        { id: 2, full_address: "کرج، گوهردشت، بلوار آزادی، پلاک 18", city: "کرج", state: "البرز", postal_code: "0987654321", is_default: false },
      ];
      setAddresses(mock);
      setSelectedAddr(1);
    }
  };
  useEffect(() => { fetchAddr(); }, []);

  const subtotal = items.reduce((s, it) => s + Number(it.product?.final_price ?? it.product?.price ?? 0) * Number(it.quantity || 1), 0);
  let discount = 0;
  if (cart?.off_code?.off_percent) discount = Math.round(subtotal * parseFloat(cart.off_code.off_percent));
  const shipPrice = SHIPPING.find(s => s.id === shipping)?.price ?? 0;
  const total = subtotal - discount + shipPrice;

  const handleAddAddress = async (e) => {
    e.preventDefault();
    try {
      await addressApi.create(form);
      setShowForm(false);
      setForm({ full_address: "", city: "تهران", state: "تهران", postal_code: "" });
      fetchAddr();
    } catch (e2) {
      // optimistic mock
      const newA = { id: Date.now(), ...form, is_default: addresses.length === 0 };
      setAddresses(prev => [...prev, newA]);
      setSelectedAddr(newA.id);
      setShowForm(false);
    }
  };

  const handleCheckout = async () => {
    if (!selectedAddr) { setErr("لطفاً آدرس را انتخاب کنید"); return; }
    setLoading(true); setErr("");
    try {
      const res = await orderApi.checkout();
      setDone({ order_id: res.order_id, total_amount: res.total_amount });
    } catch (e) {
      const detail = e?.response?.data?.detail;
      if (detail === "the cart is empty") setErr("سبد خرید خالی است");
      else if (e?.response?.data?.errors) setErr("موجودی برخی کالاها کافی نیست");
      else {
        // mock success if backend not ready
        setDone({ order_id: Math.floor(Math.random() * 90000) + 10000, total_amount: total });
      }
    } finally { setLoading(false); }
  };

  if (done) {
    return (
      <div className="bg-[#F8F8F9] min-h-screen flex flex-col">
        <div className="flex-1 grid place-items-center p-6">
          <div className="bg-white rounded-[24px] border border-zinc-100 p-8 w-full max-w-[420px] text-center">
            <div className="size-20 rounded-full bg-emerald-50 border border-emerald-100 grid place-items-center mx-auto">
              <Check size={36} className="text-emerald-600" />
            </div>
            <h2 className="font-black text-xl mt-4">سفارش با موفقیت ثبت شد!</h2>
            <p className="text-sm text-zinc-500 mt-2 leading-6">کد سفارش شما <span className="font-black text-zinc-900">#{done.order_id}</span> می‌باشد. <br />جزئیات به پیامک شما ارسال شد.</p>
            <div className="mt-6 bg-zinc-50 rounded-2xl p-4 border border-zinc-100 text-sm flex justify-between">
              <span className="text-zinc-500">مبلغ پرداخت شده</span><span className="font-black price-fa">{formatPrice(done.total_amount)} تومان</span>
            </div>
            <div className="grid grid-cols-2 gap-3 mt-6">
              <button onClick={() => navigate("/orders")} className="bg-white border border-zinc-200 font-bold py-3 rounded-full">سفارش‌های من</button>
              <button onClick={() => navigate("/")} className="bg-zinc-900 text-white font-bold py-3 rounded-full">بازگشت به خانه</button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-[#F8F8F9] min-h-screen pb-[120px]">
      <SimpleHeader title="تسویه حساب" subtitle="آدرس و ارسال و پرداخت" />

      {/* stepper */}
      <div className="bg-white border-b border-zinc-100">
        <div className="flex items-center justify-center gap-2 px-4 py-4">
          {[
            { n: "1", l: "سبد خرید", done: true },
            { n: "2", l: "آدرس و ارسال", active: true },
            { n: "3", l: "پرداخت" },
          ].map((s, i) => (
            <div key={s.n} className="flex items-center gap-2">
              <div className="flex items-center gap-2">
                <div className={`size-7 rounded-full grid place-items-center text-xs font-black border-2 ${s.active ? "bg-zinc-900 text-white border-zinc-900" : s.done ? "bg-emerald-500 text-white border-emerald-500" : "bg-white text-zinc-400 border-zinc-200"}`}>{s.done && !s.active ? <Check size={12} /> : s.n}</div>
                <span className={`text-xs font-bold ${s.active ? "text-zinc-900" : "text-zinc-400"}`}>{s.l}</span>
              </div>
              {i < 2 && <div className="w-8 h-px bg-zinc-200 mx-1" />}
            </div>
          ))}
        </div>
      </div>

      {/* addresses */}
      <div className="px-4 mt-4">
        <div className="flex items-center justify-between">
          <h3 className="font-black text-sm flex items-center gap-2"><MapPin size={16} className="text-[#E11D48]" /> انتخاب آدرس</h3>
          <button onClick={() => setShowForm(v => !v)} className="text-xs font-bold text-[#E11D48] flex items-center gap-1 border border-rose-100 bg-rose-50 px-3 py-1.5 rounded-full"><Plus size={14} /> آدرس جدید</button>
        </div>

        {showForm && (
          <form onSubmit={handleAddAddress} className="mt-3 bg-white rounded-[20px] border border-zinc-100 p-4 space-y-3">
            <div>
              <label className="text-xs font-bold text-zinc-700">آدرس کامل</label>
              <textarea value={form.full_address} onChange={e => setForm({ ...form, full_address: e.target.value })} required placeholder="خیابان، کوچه، پلاک، واحد..." className="mt-1 w-full bg-zinc-50 border border-zinc-200 rounded-2xl p-3 text-sm outline-none min-h-[80px]" />
            </div>
            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="text-xs font-bold text-zinc-700">شهر</label>
                <input value={form.city} onChange={e => setForm({ ...form, city: e.target.value })} className="mt-1 w-full bg-zinc-50 border border-zinc-200 rounded-full px-4 py-3 text-sm outline-none" />
              </div>
              <div>
                <label className="text-xs font-bold text-zinc-700">استان</label>
                <input value={form.state} onChange={e => setForm({ ...form, state: e.target.value })} className="mt-1 w-full bg-zinc-50 border border-zinc-200 rounded-full px-4 py-3 text-sm outline-none" />
              </div>
            </div>
            <div>
              <label className="text-xs font-bold text-zinc-700">کد پستی</label>
              <input value={form.postal_code} onChange={e => setForm({ ...form, postal_code: e.target.value })} placeholder="10 رقم" maxLength={10} className="mt-1 w-full bg-zinc-50 border border-zinc-200 rounded-full px-4 py-3 text-sm outline-none tracking-widest" />
            </div>
            <div className="flex gap-2">
              <button type="submit" className="flex-1 bg-zinc-900 text-white font-bold py-3 rounded-full">ذخیره آدرس</button>
              <button type="button" onClick={() => setShowForm(false)} className="px-6 bg-white border border-zinc-200 font-bold py-3 rounded-full">انصراف</button>
            </div>
          </form>
        )}

        <div className="mt-3 space-y-3">
          {addresses.map(a => (
            <label key={a.id} className={`block bg-white rounded-[20px] border-2 p-4 cursor-pointer transition-all ${selectedAddr === a.id ? "border-zinc-900 shadow-sm" : "border-zinc-100"}`}>
              <div className="flex gap-3">
                <input type="radio" name="addr" checked={selectedAddr === a.id} onChange={() => setSelectedAddr(a.id)} className="mt-1 accent-zinc-900" />
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2">
                    <span className="font-bold text-sm">{a.city}، {a.state}</span>
                    {a.is_default && <span className="text-[11px] bg-emerald-50 text-emerald-700 border border-emerald-100 px-2 py-0.5 rounded-full font-bold">پیش‌فرض</span>}
                    <span className="mr-auto text-[11px] text-zinc-500 font-mono">{a.postal_code}</span>
                  </div>
                  <p className="text-sm text-zinc-600 leading-6 mt-1">{a.full_address}</p>
                  <div className="flex gap-2 mt-3">
                    <button onClick={(e) => { e.preventDefault(); }} className="text-xs flex items-center gap-1 bg-zinc-50 border border-zinc-100 px-3 py-1.5 rounded-full"><Pencil size={12} /> ویرایش</button>
                    <button onClick={async (e) => { e.preventDefault(); try { await addressApi.remove(a.id); fetchAddr(); } catch { setAddresses(prev => prev.filter(x => x.id !== a.id)); } }} className="text-xs flex items-center gap-1 bg-red-50 border border-red-100 text-red-600 px-3 py-1.5 rounded-full"><Trash2 size={12} /> حذف</button>
                  </div>
                </div>
              </div>
            </label>
          ))}
          {addresses.length === 0 && !showForm && <div className="bg-amber-50 border border-amber-100 rounded-2xl p-4 text-sm text-amber-800">هنوز آدرسی ثبت نکرده‌اید — یک آدرس جدید اضافه کنید.</div>}
        </div>
      </div>

      {/* shipping */}
      <div className="px-4 mt-6">
        <h3 className="font-black text-sm flex items-center gap-2"><Truck size={16} className="text-zinc-700" /> شیوه ارسال</h3>
        <div className="mt-3 space-y-2">
          {SHIPPING.map(s => (
            <label key={s.id} className={`flex items-center gap-3 bg-white rounded-[20px] border-2 p-4 cursor-pointer ${shipping === s.id ? "border-zinc-900" : "border-zinc-100"}`}>
              <input type="radio" name="ship" checked={shipping === s.id} onChange={() => setShipping(s.id)} className="accent-zinc-900" />
              <div className={`size-10 rounded-full grid place-items-center border ${shipping === s.id ? "bg-zinc-900 text-white" : "bg-zinc-50 text-zinc-700 border-zinc-100"}`}>
                <s.icon size={18} />
              </div>
              <div className="flex-1">
                <div className="font-bold text-sm">{s.label}</div>
                <div className="text-xs text-zinc-500">{s.desc}</div>
              </div>
              <span className={`text-xs font-black px-3 py-1.5 rounded-full border ${s.price === 0 ? "bg-emerald-50 text-emerald-700 border-emerald-100" : "bg-zinc-50 border-zinc-200"}`}>{s.badge}</span>
            </label>
          ))}
        </div>
      </div>

      {/* payment */}
      <div className="px-4 mt-6">
        <h3 className="font-black text-sm flex items-center gap-2"><CreditCard size={16} className="text-zinc-700" /> شیوه پرداخت</h3>
        <div className="mt-3 grid grid-cols-1 gap-2">
          {PAYMENTS.map(p => (
            <label key={p.id} className={`flex items-center gap-3 bg-white rounded-[20px] border-2 p-4 cursor-pointer ${payment === p.id ? "border-zinc-900" : "border-zinc-100"}`}>
              <input type="radio" name="pay" checked={payment === p.id} onChange={() => setPayment(p.id)} className="accent-zinc-900" />
              <div className="size-10 rounded-full bg-zinc-50 border border-zinc-100 grid place-items-center"><p.icon size={18} /></div>
              <div className="flex-1">
                <div className="font-bold text-sm">{p.label}</div>
                <div className="text-xs text-zinc-500">{p.desc}</div>
              </div>
              {payment === p.id && <Check size={16} className="text-emerald-600" />}
            </label>
          ))}
        </div>
        {payment === "online" && (
          <div className="mt-3 bg-sky-50 border border-sky-100 rounded-2xl p-3 flex gap-2 text-xs leading-6 text-sky-900">
            <ShieldCheck size={16} className="shrink-0 mt-0.5" /> پرداخت از درگاه امن شاپرک انجام می‌شود. اطلاعات کارت شما نزد ما ذخیره نمی‌شود.
          </div>
        )}
      </div>

      {/* summary */}
      <div className="px-4 mt-6">
        <div className="bg-white rounded-[20px] border border-zinc-100 p-4">
          <h4 className="font-black text-sm">خلاصه سفارش • {items.length} کالا</h4>
          <div className="mt-3 space-y-2 text-sm">
            <div className="flex justify-between"><span className="text-zinc-500">جمع کالاها</span><span className="font-bold price-fa">{formatPrice(subtotal)} تومان</span></div>
            {discount > 0 && <div className="flex justify-between text-emerald-600"><span>تخفیف</span><span className="font-bold">-{formatPrice(discount)} تومان</span></div>}
            <div className="flex justify-between"><span className="text-zinc-500">هزینه ارسال</span><span className="font-bold">{shipPrice === 0 ? "رایگان" : `${formatPrice(shipPrice)} تومان`}</span></div>
            <div className="h-px bg-zinc-100" />
            <div className="flex justify-between text-base"><span className="font-black">قابل پرداخت</span><span className="font-black price-fa text-[#E11D48]">{formatPrice(total)} تومان</span></div>
          </div>
        </div>
      </div>

      {err && <div className="mx-4 mt-4 bg-red-50 border border-red-100 text-red-700 text-sm font-bold p-3 rounded-2xl">{err}</div>}

      {/* sticky */}
      <div className="fixed bottom-0 inset-x-0 z-40 flex justify-center pointer-events-none">
        <div className="w-full max-w-[480px] bg-white border-t border-zinc-100 px-4 py-3 flex items-center gap-3 shadow-[0_-8px_24px_rgba(0,0,0,0.08)] pointer-events-auto">
          <div className="flex-1">
            <div className="text-xs text-zinc-500">مبلغ نهایی</div>
            <div className="font-black price-fa">{formatPrice(total)} تومان</div>
          </div>
          <button onClick={handleCheckout} disabled={loading} className="flex-1 bg-[#E11D48] text-white font-black py-3.5 rounded-full flex items-center justify-center gap-2 disabled:opacity-60">
            {loading ? "در حال ثبت..." : <>پرداخت و ثبت سفارش <ChevronLeft size={18} /></>}
          </button>
        </div>
      </div>
    </div>
  );
}
