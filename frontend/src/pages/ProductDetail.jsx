import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { Star, Heart, Share2, Truck, ShieldCheck, RotateCcw, ChevronDown, Plus, Minus, ShoppingBag, Check } from "lucide-react";
import { productsApi } from "../services/api";
import { useCart } from "../context/CartContext";
import { formatPrice } from "../utils/format";
import { SimpleHeader } from "../components/Header";

const MOCK_DETAIL = {
  id: 1,
  title: "گوشی موبایل سامسونگ Galaxy S23 Ultra — 256 گیگابایت",
  short_desc: "دوربین 200 مگاپیکسلی، قلم S Pen، پردازنده Snapdragon 8 Gen 2",
  desc: "گلکسی S23 Ultra با طراحی جذاب، بدنه تیتانیومی و دوربین فوق‌العاده 200 مگاپیکسلی، بهترین تجربه عکاسی و کارایی را ارائه می‌دهد. باتری 5000 میلی‌آمپر با شارژ سریع 45 وات و نمایشگر Dynamic AMOLED 2X با نرخ 120 هرتز.",
  price: 48500000,
  final_price: 42500000,
  off_percent: 0.12,
  review_avg_point: 4.6,
  review_count: 342,
  sell_count: 1290,
  stock_quantity: 18,
  is_available: true,
  category: { name: "موبایل" },
  brand: { name: "Samsung", logo: "" },
  images: [],
};

const PLACEHOLDERS = [
  "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=600&h=600&fit=crop",
  "https://images.unsplash.com/photo-1592899677977-9c10ca588bbd?w=600&h=600&fit=crop",
  "https://images.unsplash.com/photo-1585060544812-6b45742d762f?w=600&h=600&fit=crop",
];

export default function ProductDetail() {
  const { id } = useParams();
  const [product, setProduct] = useState(null);
  const [qty, setQty] = useState(1);
  const [activeImg, setActiveImg] = useState(0);
  const [adding, setAdding] = useState(false);
  const [added, setAdded] = useState(false);
  const [error, setError] = useState("");
  const { addToCart } = useCart();

  useEffect(() => {
    let cancelled = false;
    (async () => {
      try {
        const data = await productsApi.detail(id);
        if (!cancelled) setProduct(data);
      } catch {
        if (!cancelled) setProduct({ ...MOCK_DETAIL, id: Number(id) });
      }
    })();
    return () => { cancelled = true; };
  }, [id]);

  if (!product) {
    return (
      <div className="bg-white min-h-screen">
        <SimpleHeader title="جزئیات محصول" />
        <div className="p-4 space-y-4">
          <div className="aspect-square shimmer rounded-[24px]" />
          <div className="h-6 shimmer rounded w-3/4" />
          <div className="h-4 shimmer rounded" />
        </div>
      </div>
    );
  }

  const off = product.off_percent ? Math.round(parseFloat(product.off_percent) * 100) : 0;
  const hasOff = off > 0;
  const imgs = product.images?.length ? product.images.map(i => {
    const u = i.image;
    if (u.startsWith("http")) return u;
    if (u.startsWith("/media")) return `http://localhost:8000${u}`;
    return u;
  }) : PLACEHOLDERS;

  const onAdd = async () => {
    setAdding(true);
    setError("");
    const r = await addToCart(product, qty);
    setAdding(false);
    if (r.ok) {
      setAdded(true);
      setTimeout(() => setAdded(false), 2000);
    } else {
      setError(r.msg || "خطا در افزودن");
    }
  };

  return (
    <div className="bg-[#F8F8F9] min-h-screen pb-[96px]">
      <SimpleHeader title="جزئیات محصول" subtitle={product.category?.name} action={
        <div className="flex gap-2">
          <button className="size-9 rounded-full bg-zinc-50 border border-zinc-100 grid place-items-center"><Share2 size={16} /></button>
          <button className="size-9 rounded-full bg-zinc-50 border border-zinc-100 grid place-items-center"><Heart size={16} /></button>
        </div>
      } />

      {/* gallery */}
      <div className="bg-white">
        <div className="relative aspect-[1.05] bg-[#F9F9FB] overflow-hidden">
          <img src={imgs[activeImg]} alt={product.title} className="w-full h-full object-contain p-6" />
          {hasOff && <span className="absolute top-4 right-4 bg-[#E11D48] text-white text-xs font-black px-3 py-1.5 rounded-full">{off}٪ تخفیف</span>}
          <div className="absolute bottom-4 left-1/2 -translate-x-1/2 flex gap-1.5">
            {imgs.slice(0, 4).map((_, i) => (
              <span key={i} className={`h-1.5 rounded-full transition-all ${i === activeImg ? "w-6 bg-zinc-900" : "w-1.5 bg-zinc-300"}`} />
            ))}
          </div>
        </div>
        <div className="flex gap-2 px-4 py-3 overflow-x-auto scrollbar-hide">
          {imgs.slice(0, 4).map((img, i) => (
            <button key={i} onClick={() => setActiveImg(i)} className={`shrink-0 size-[72px] rounded-2xl overflow-hidden border-2 ${i === activeImg ? "border-zinc-900" : "border-zinc-100"} bg-zinc-50`}>
              <img src={img} alt="" className="w-full h-full object-cover" />
            </button>
          ))}
          <div className="shrink-0 size-[72px] rounded-2xl border-2 border-dashed border-zinc-200 grid place-items-center text-xs text-zinc-500">+2</div>
        </div>
      </div>

      {/* info */}
      <div className="bg-white mt-2 rounded-t-[24px] -mt-2 relative z-10 px-4 pt-5 pb-4 border-t border-zinc-100">
        <div className="flex items-start justify-between gap-3">
          <div className="flex-1">
            <div className="inline-flex items-center gap-1.5 bg-zinc-900 text-white text-[11px] font-bold px-2.5 py-1 rounded-full">
              <span className="size-1.5 bg-emerald-400 rounded-full animate-pulse" /> موجود در انبار • {product.stock_quantity || 12} عدد
            </div>
            <h1 className="font-black text-[17px] leading-7 mt-3">{product.title}</h1>
            <p className="text-sm text-zinc-500 mt-1 leading-6">{product.short_desc}</p>
          </div>
          <div className="shrink-0 bg-zinc-50 border border-zinc-100 rounded-2xl px-3 py-2 text-center">
            <div className="text-[11px] text-zinc-500">برند</div>
            <div className="font-black text-sm">{product.brand?.name || "Samsung"}</div>
          </div>
        </div>

        <div className="flex items-center gap-3 mt-4">
          <div className="flex items-center gap-1.5 bg-amber-50 border border-amber-100 px-3 py-1.5 rounded-full">
            <Star size={14} className="fill-amber-400 text-amber-400" />
            <span className="text-sm font-black">{parseFloat(product.review_avg_point || 4.6).toFixed(1)}</span>
            <span className="text-xs text-zinc-500">({product.review_count || 342} نظر)</span>
          </div>
          <span className="text-xs text-zinc-400">•</span>
          <span className="text-xs text-zinc-600 font-medium">{product.sell_count || 1290} فروش</span>
          <span className="text-xs text-zinc-600 mr-auto flex items-center gap-1"><span className="size-2 bg-emerald-500 rounded-full" /> ارسال امروز</span>
        </div>

        {/* price */}
        <div className="mt-5 bg-[#F9F9FB] rounded-2xl p-4 border border-zinc-100 flex items-end justify-between">
          <div>
            <div className="text-xs text-zinc-500">قیمت محصول</div>
            {hasOff && <div className="text-xs text-zinc-400 line-through price-fa">{formatPrice(product.price)} تومان</div>}
            <div className="font-black text-xl price-fa flex items-baseline gap-1.5">{formatPrice(product.final_price ?? product.price)} <span className="text-xs font-bold text-zinc-500">تومان</span></div>
            {hasOff && <div className="text-xs text-emerald-600 font-bold mt-1">شما {formatPrice(product.price - product.final_price)} تومان سود می‌کنید!</div>}
          </div>
          <div className="flex items-center gap-2 bg-white rounded-full p-1 border border-zinc-200 shadow-sm">
            <button onClick={() => setQty(q => Math.max(1, q - 1))} className="size-8 rounded-full bg-zinc-50 border grid place-items-center hover:bg-zinc-100">
              <Minus size={14} />
            </button>
            <span className="w-8 text-center font-black text-sm">{qty}</span>
            <button onClick={() => setQty(q => q + 1)} className="size-8 rounded-full bg-zinc-900 text-white grid place-items-center hover:bg-black">
              <Plus size={14} />
            </button>
          </div>
        </div>

        {/* perks */}
        <div className="grid grid-cols-3 gap-2 mt-4">
          <div className="bg-white border border-zinc-100 rounded-2xl p-3 text-center">
            <Truck size={18} className="mx-auto text-zinc-700" />
            <div className="text-[11px] font-bold mt-1">ارسال رایگان</div>
            <div className="text-[10px] text-zinc-500">بالای 500 هزار</div>
          </div>
          <div className="bg-white border border-zinc-100 rounded-2xl p-3 text-center">
            <ShieldCheck size={18} className="mx-auto text-zinc-700" />
            <div className="text-[11px] font-bold mt-1">ضمانت اصالت</div>
            <div className="text-[10px] text-zinc-500">18 ماه گارانتی</div>
          </div>
          <div className="bg-white border border-zinc-100 rounded-2xl p-3 text-center">
            <RotateCcw size={18} className="mx-auto text-zinc-700" />
            <div className="text-[11px] font-bold mt-1">بازگشت 7 روزه</div>
            <div className="text-[10px] text-zinc-500">بدون قید</div>
          </div>
        </div>

        {/* desc */}
        <div className="mt-6">
          <h3 className="font-black text-sm flex items-center gap-2">توضیحات محصول <span className="size-1.5 bg-[#E11D48] rounded-full" /></h3>
          <p className="text-sm text-zinc-600 leading-7 mt-2 bg-zinc-50 rounded-2xl p-4 border border-zinc-100">
            {product.desc || MOCK_DETAIL.desc}
          </p>
          <details className="mt-3 group">
            <summary className="flex items-center justify-between bg-white border border-zinc-100 rounded-2xl px-4 py-3 cursor-pointer list-none">
              <span className="font-bold text-sm">ویژگی‌ها و مشخصات</span><ChevronDown size={16} className="group-open:rotate-180 transition-transform" />
            </summary>
            <div className="mt-2 bg-white border border-zinc-100 rounded-2xl overflow-hidden text-sm divide-y divide-zinc-100">
              {[
                ["برند", product.brand?.name || "Samsung"],
                ["دسته‌بندی", product.category?.name || "موبایل"],
                ["وزن", "234 گرم"],
                ["رنگ", "مشکی فانتوم"],
                ["گارانتی", "18 ماه شرکتی"],
              ].map(([k, v]) => (
                <div key={k} className="flex justify-between px-4 py-3">
                  <span className="text-zinc-500">{k}</span><span className="font-bold">{v}</span>
                </div>
              ))}
            </div>
          </details>
        </div>

        {/* related */}
        <div className="mt-6 -mx-4">
          <div className="px-4 flex items-center justify-between">
            <h3 className="font-black text-sm">محصولات مشابه</h3>
            <Link to="/" className="text-xs text-[#E11D48] font-bold">مشاهده همه</Link>
          </div>
          <div className="flex gap-3 overflow-x-auto scrollbar-hide px-4 mt-3 pb-2">
            {[1,2,3].map(i => (
              <Link key={i} to={`/product/${i}`} className="shrink-0 w-[160px] bg-white rounded-2xl border border-zinc-100 overflow-hidden">
                <img src={PLACEHOLDERS[i%3]} alt="" className="w-full h-28 object-cover bg-zinc-50" />
                <div className="p-3">
                  <div className="font-bold text-xs line-clamp-2 leading-5">گوشی شیائومی Redmi Note 13</div>
                  <div className="font-black text-xs mt-1 price-fa">{formatPrice(12500000)} تومان</div>
                </div>
              </Link>
            ))}
          </div>
        </div>
      </div>

      {/* sticky add */}
      <div className="fixed bottom-0 inset-x-0 z-40 flex justify-center pointer-events-none">
        <div className="w-full max-w-[480px] bg-white border-t border-zinc-100 px-4 py-3 flex items-center gap-3 shadow-[0_-8px_24px_rgba(0,0,0,0.08)] pointer-events-auto">
          <div className="flex-1">
            <div className="text-xs text-zinc-500">مبلغ قابل پرداخت</div>
            <div className="font-black text-base price-fa">{formatPrice((product.final_price ?? product.price) * qty)} تومان</div>
          </div>
          <button
            onClick={onAdd}
            disabled={adding}
            className={`flex-1 max-w-[220px] h-12 rounded-full font-black text-sm flex items-center justify-center gap-2 ${added ? "bg-emerald-600 text-white" : "bg-[#E11D48] text-white hover:bg-[#be123c]"} transition-colors`}
          >
            {added ? <><Check size={18} /> افزوده شد</> : adding ? "در حال افزودن..." : <><ShoppingBag size={18} /> افزودن به سبد</>}
          </button>
        </div>
      </div>

      {error && <div className="fixed bottom-[84px] left-1/2 -translate-x-1/2 bg-red-600 text-white text-xs font-bold px-4 py-2 rounded-full">{error}</div>}
    </div>
  );
}
