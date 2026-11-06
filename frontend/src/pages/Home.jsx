import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { ChevronLeft, Flame, Sparkles, ArrowUpDown, SlidersHorizontal, Package, Award, Truck, ShieldCheck } from "lucide-react";
import { HomeHeader } from "../components/Header";
import ProductCard from "../components/ProductCard";
import { productsApi } from "../services/api";
import { useCart } from "../context/CartContext";
import { formatPrice } from "../utils/format";

const CATEGORIES = [
  { name: "موبایل", emoji: "📱", color: "bg-violet-50 border-violet-100" },
  { name: "لپ‌تاپ", emoji: "💻", color: "bg-sky-50 border-sky-100" },
  { name: "پوشاک", emoji: "👗", color: "bg-rose-50 border-rose-100" },
  { name: "خانه", emoji: "🏠", color: "bg-amber-50 border-amber-100" },
  { name: "زیبایی", emoji: "💄", color: "bg-pink-50 border-pink-100" },
  { name: "کتاب", emoji: "📚", color: "bg-emerald-50 border-emerald-100" },
  { name: "ورزش", emoji: "⚽", color: "bg-orange-50 border-orange-100" },
  { name: "ساعت", emoji: "⌚", color: "bg-zinc-50 border-zinc-200" },
];

const MOCK = [
  { id: 1, title: "گوشی موبایل سامسونگ Galaxy S23", short_desc: "حافظه 256، رم 8، دوربین 50 مگاپیکسل", price: 42500000, final_price: 38900000, off_percent: 0.08, category: { name: "موبایل" }, brand: { name: "Samsung" }, review_avg_point: 4.6, is_available: true, images: [] },
  { id: 2, title: "هدفون بی‌سیم سونی WH-1000XM5", short_desc: "نویز کنسلینگ، 30 ساعت شارژدهی", price: 18500000, final_price: 14200000, off_percent: 0.23, category: { name: "صوتی" }, brand: { name: "Sony" }, review_avg_point: 4.8, is_available: true, images: [] },
  { id: 3, title: "کفش نایک Air Max", short_desc: "سبک، راحت، مناسب دویدن", price: 5600000, final_price: 5600000, off_percent: 0, category: { name: "پوشاک" }, brand: { name: "Nike" }, review_avg_point: 4.3, is_available: true, images: [] },
  { id: 4, title: "ساعت هوشمند اپل واچ 9", short_desc: "صفحه 45mm، حسگر سلامت", price: 22000000, final_price: 19800000, off_percent: 0.1, category: { name: "ساعت" }, brand: { name: "Apple" }, review_avg_point: 4.7, is_available: true, images: [] },
  { id: 5, title: "کیف چرم طبیعی", short_desc: "دست‌دوز، جادار، شیک", price: 3200000, final_price: 2400000, off_percent: 0.25, category: { name: "کیف" }, brand: { name: "چرم مشهد" }, review_avg_point: 4.5, is_available: true, images: [] },
  { id: 6, title: "پاوربانک 20000 میلی‌آمپر", short_desc: "شارژ سریع 22.5 وات", price: 1800000, final_price: 1350000, off_percent: 0.25, category: { name: "جانبی" }, brand: { name: "Anker" }, review_avg_point: 4.4, is_available: true, images: [] },
];

export default function Home() {
  const [products, setProducts] = useState(MOCK);
  const [loading, setLoading] = useState(false);
  const [filter, setFilter] = useState({ has_off: false, sort: "", search: "" });
  const [selectedCat, setSelectedCat] = useState(null);
  const { addToCart } = useCart();
  const [toast, setToast] = useState("");

  const fetch = async (params = {}) => {
    setLoading(true);
    try {
      const data = await productsApi.list({ page_size: 20, ...params });
      const list = data.results ?? data;
      if (Array.isArray(list) && list.length) setProducts(list);
    } catch {
      // keep mock
    } finally { setLoading(false); }
  };

  useEffect(() => { fetch(); }, []);

  const onSearch = (q) => {
    setFilter(f => ({ ...f, search: q }));
    fetch({ search: q, ...(selectedCat ? { category: selectedCat } : {}), ...(filter.has_off ? { has_off: "" } : {}) });
  };

  const toggleOff = () => {
    const newVal = !filter.has_off;
    setFilter({ ...filter, has_off: newVal });
    fetch({ ...(newVal ? { has_off: "" } : {}), ...(filter.search ? { search: filter.search } : {}), ...(selectedCat ? { category: selectedCat } : {}), ...(filter.sort ? { sort: filter.sort } : {}) });
  };

  const changeSort = (sort) => {
    const newSort = filter.sort === sort ? "" : sort;
    setFilter({ ...filter, sort: newSort });
    fetch({ sort: newSort, descending: newSort ? "true" : undefined, ...(filter.has_off ? { has_off: "" } : {}), ...(filter.search ? { search: filter.search } : {}) });
  };

  const filterByCat = (cat) => {
    const next = selectedCat === cat ? null : cat;
    setSelectedCat(next);
    fetch({ ...(next ? { category: next } : {}), ...(filter.has_off ? { has_off: "" } : {}), ...(filter.sort ? { sort: filter.sort, descending: "true" } : {}) });
  };

  const handleAdd = async (p) => {
    const r = await addToCart(p, 1);
    if (r?.ok) {
      setToast(`"${p.title.slice(0, 20)}..." به سبد اضافه شد`);
      setTimeout(() => setToast(""), 1800);
    } else {
      setToast(r?.msg || "خطا");
      setTimeout(() => setToast(""), 1800);
    }
  };

  return (
    <div className="bg-white min-h-screen">
      <HomeHeader onSearch={onSearch} />

      {/* categories */}
      <div className="px-4">
        <div className="flex items-center justify-between mt-1 mb-3">
          <span className="font-extrabold text-sm">دسته‌بندی‌ها</span>
          <Link to="/categories" className="text-xs text-[#E11D48] font-bold flex items-center gap-1">همه <ChevronLeft size={14} /></Link>
        </div>
        <div className="flex gap-2 overflow-x-auto scrollbar-hide pb-2 -mx-4 px-4">
          {CATEGORIES.map(c => (
            <button
              key={c.name}
              onClick={() => filterByCat(c.name)}
              className={`shrink-0 flex flex-col items-center gap-2 w-[72px] p-3 rounded-2xl border ${selectedCat === c.name ? "bg-zinc-900 text-white border-zinc-900" : c.color} transition-colors`}
            >
              <span className="text-2xl">{c.emoji}</span>
              <span className={`text-xs font-bold ${selectedCat === c.name ? "text-white" : "text-zinc-700"}`}>{c.name}</span>
            </button>
          ))}
        </div>
      </div>

      {/* banner */}
      <div className="px-4 mt-4">
        <div className="rounded-[20px] overflow-hidden bg-gradient-to-br from-[#E11D48] to-[#be123c] p-4 text-white relative">
          <div className="absolute -right-6 -top-6 size-32 bg-white/10 rounded-full blur-2xl" />
          <div className="absolute -left-10 -bottom-10 size-40 bg-black/10 rounded-full" />
          <div className="relative flex gap-4 items-center">
            <div className="flex-1">
              <div className="inline-flex items-center gap-1 bg-white/15 backdrop-blur px-2.5 py-1 rounded-full text-xs font-bold border border-white/20">
                <Flame size={14} className="text-amber-300" /> پیشنهاد شگفت‌انگیز
              </div>
              <h3 className="font-black text-lg leading-6 mt-2">تا ۵۰٪ تخفیف<br />روی همه محصولات</h3>
              <p className="text-xs opacity-90 mt-1.5">فقط تا پایان جمعه — ارسال رایگان</p>
              <button className="mt-3 bg-white text-[#E11D48] text-xs font-black px-4 py-2 rounded-full">مشاهده محصولات</button>
            </div>
            <img src="https://images.unsplash.com/photo-1483985988355-763728e1935b?w=200&h=260&fit=crop" alt="" className="w-[112px] h-[140px] object-cover rounded-2xl shadow-lg rotate-2 hidden sm:block" />
          </div>
          <div className="flex gap-1.5 justify-center mt-3">
            <span className="size-1.5 rounded-full bg-white"></span>
            <span className="size-1.5 rounded-full bg-white/40"></span>
            <span className="size-1.5 rounded-full bg-white/40"></span>
          </div>
        </div>
      </div>

      {/* perks */}
      <div className="px-4 mt-3 grid grid-cols-4 gap-2">
        {[
          { icon: Truck, label: "ارسال رایگان" },
          { icon: ShieldCheck, label: "ضمانت اصالت" },
          { icon: Award, label: "پرداخت امن" },
          { icon: Package, label: "۷ روز بازگشت" },
        ].map(({ icon: Icon, label }) => (
          <div key={label} className="bg-zinc-50 rounded-2xl border border-zinc-100 py-3 flex flex-col items-center gap-1.5">
            <div className="size-8 rounded-full bg-white grid place-items-center border border-zinc-100"><Icon size={16} className="text-zinc-700" /></div>
            <span className="text-[11px] font-bold text-zinc-700">{label}</span>
          </div>
        ))}
      </div>

      {/* filters */}
      <div className="px-4 mt-5 flex items-center gap-2 overflow-x-auto scrollbar-hide">
        <button onClick={toggleOff} className={`shrink-0 flex items-center gap-1.5 px-3.5 py-2 rounded-full border text-xs font-bold ${filter.has_off ? "bg-[#E11D48] text-white border-[#E11D48]" : "bg-white border-zinc-200 text-zinc-700"}`}>
          <Sparkles size={14} /> فقط تخفیف‌دار
        </button>
        {[
          { k: "sell", l: "پرفروش‌ترین" },
          { k: "price", l: "ارزان‌ترین" },
          { k: "point", l: "محبوب‌ترین" },
          { k: "view", l: "پربازدیدترین" },
        ].map(s => (
          <button key={s.k} onClick={() => changeSort(s.k)} className={`shrink-0 px-3.5 py-2 rounded-full border text-xs font-bold ${filter.sort === s.k ? "bg-zinc-900 text-white border-zinc-900" : "bg-white border-zinc-200 text-zinc-700"}`}>{s.l}</button>
        ))}
        <button className="shrink-0 size-9 rounded-full bg-white border border-zinc-200 grid place-items-center">
          <SlidersHorizontal size={16} />
        </button>
      </div>

      {/* section title */}
      <div className="px-4 mt-6 flex items-center justify-between">
        <h2 className="font-black text-[15px] flex items-center gap-2">
          <span className="size-1.5 rounded-full bg-[#E11D48]"></span> محصولات پیشنهادی
        </h2>
        <span className="text-xs text-zinc-500">{products.length} محصول</span>
      </div>

      {/* grid */}
      <div className="px-4 mt-3 grid grid-cols-2 gap-3 pb-6">
        {loading ? (
          Array.from({ length: 6 }).map((_, i) => (
            <div key={i} className="bg-white rounded-[22px] border border-zinc-100 overflow-hidden">
              <div className="aspect-square shimmer" />
              <div className="p-3 space-y-2">
                <div className="h-3 shimmer rounded" />
                <div className="h-3 w-2/3 shimmer rounded" />
              </div>
            </div>
          ))
        ) : (
          products.map(p => (
            <ProductCard key={p.id} product={p} onQuickAdd={handleAdd} />
          ))
        )}
      </div>

      {/* banner 2 */}
      <div className="mx-4 mb-6 rounded-[20px] overflow-hidden bg-zinc-900 text-white p-4 flex items-center gap-4">
        <div className="flex-1">
          <div className="text-amber-300 text-xs font-bold">حراج ویژه کیف و کفش</div>
          <div className="font-black text-sm mt-1 leading-5">استایل پاییزی<br />با قیمت باورنکردنی</div>
          <div className="inline-flex mt-3 bg-white text-zinc-900 text-xs font-black px-4 py-2 rounded-full">خرید کنید <ChevronLeft size={14} /></div>
        </div>
        <img src="https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=200&h=200&fit=crop" alt="" className="size-24 rounded-2xl object-cover" />
      </div>

      {toast && (
        <div className="fixed bottom-[90px] left-1/2 -translate-x-1/2 bg-zinc-900 text-white text-xs font-bold px-4 py-3 rounded-full shadow-xl z-50 flex items-center gap-2">
          <span className="size-2 rounded-full bg-emerald-400 animate-pulse" /> {toast}
        </div>
      )}
    </div>
  );
}
