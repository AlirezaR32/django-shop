import { Link } from "react-router-dom";
import { Star, ShoppingBag } from "lucide-react";
import { formatPrice, formatOff } from "../utils/format";

const PLACEHOLDERS = [
  "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400&h=400&fit=crop",
  "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400&h=400&fit=crop",
  "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&h=400&fit=crop",
  "https://images.unsplash.com/photo-1498049794561-7780e7231661?w=400&h=400&fit=crop",
  "https://images.unsplash.com/photo-1512499617640-c74ae3a79d37?w=400&h=400&fit=crop",
  "https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f?w=400&h=400&fit=crop",
];

function imgFor(id, images) {
  if (images && images.length && images[0].image) {
    // images may be relative media url
    const img = images[0].image;
    if (img.startsWith("http")) return img;
    if (img.startsWith("/media")) return `http://localhost:8000${img}`;
    return img;
  }
  return PLACEHOLDERS[Number(id) % PLACEHOLDERS.length];
}

export default function ProductCard({ product, onQuickAdd }) {
  const off = product.off_percent ? Math.round(parseFloat(product.off_percent) * 100) : (formatOff(product.price, product.final_price) || 0);
  const hasOff = off > 0;
  const rating = parseFloat(product.review_avg_point || 0).toFixed(1);
  return (
    <Link to={`/product/${product.id}`} className="bg-white rounded-[22px] border border-zinc-100 overflow-hidden flex flex-col group hover:shadow-lg transition-shadow">
      <div className="relative aspect-square bg-[#F9F9FB] p-3">
        <img src={imgFor(product.id, product.images)} alt={product.title} className="w-full h-full object-contain mix-blend-multiply group-hover:scale-[1.03] transition-transform duration-300" loading="lazy" />
        {hasOff && (
          <span className="absolute top-3 right-3 bg-[#E11D48] text-white text-xs font-black px-2 py-1 rounded-full">
            {off}٪ تخفیف
          </span>
        )}
        {!product.is_available && (
          <span className="absolute bottom-3 right-3 bg-zinc-900 text-white text-[11px] px-2 py-1 rounded-full">ناموجود</span>
        )}
        <div className="absolute bottom-3 left-3 bg-white/90 backdrop-blur px-2 py-1 rounded-full flex items-center gap-1 text-[11px] border border-zinc-100">
          <Star size={12} className="fill-amber-400 text-amber-400" /> {rating}
        </div>
      </div>
      <div className="p-3 flex-1 flex flex-col gap-1.5">
        <div className="text-[11px] text-zinc-500 leading-none">{product.brand?.name || "برند"} • {product.category?.name || "دسته‌بندی"}</div>
        <div className="font-bold text-[13px] leading-5 line-clamp-2 min-h-[40px]">{product.title}</div>
        {product.short_desc && <div className="text-xs text-zinc-500 line-clamp-1">{product.short_desc}</div>}
        <div className="mt-auto pt-2 flex items-end justify-between">
          <div>
            {hasOff && <div className="text-[11px] text-zinc-400 line-through price-fa">{formatPrice(product.price)}</div>}
            <div className="font-black text-[14px] price-fa flex items-baseline gap-1">
              {formatPrice(product.final_price ?? product.price)} <span className="text-[11px] font-bold text-zinc-500">تومان</span>
            </div>
          </div>
          <button
            onClick={(e) => { e.preventDefault(); onQuickAdd?.(product); }}
            className="size-8 rounded-full bg-zinc-900 text-white grid place-items-center hover:bg-black transition-colors"
          >
            <ShoppingBag size={14} />
          </button>
        </div>
      </div>
    </Link>
  );
}

export function ProductCardHorizontal({ product, qty, onInc, onDec, onRemove }) {
  return (
    <div className="flex gap-3 bg-white rounded-2xl border border-zinc-100 p-3">
      <img src={imgFor(product.id, product.images)} alt={product.title} className="size-20 rounded-xl bg-zinc-50 object-cover" />
      <div className="flex-1 min-w-0">
        <div className="text-xs text-zinc-500">{product.brand?.name}</div>
        <div className="font-bold text-sm leading-5 line-clamp-2">{product.title}</div>
        <div className="font-black text-sm price-fa mt-1">{formatPrice(product.final_price ?? product.price)} تومان</div>
        {qty !== undefined && (
          <div className="flex items-center gap-2 mt-2">
            <div className="flex items-center gap-2 bg-zinc-50 rounded-full p-1 border border-zinc-100">
              <button onClick={() => onInc?.()} className="size-7 rounded-full bg-white border grid place-items-center font-bold">+</button>
              <span className="w-6 text-center text-sm font-bold">{qty}</span>
              <button onClick={() => onDec?.()} className="size-7 rounded-full bg-white border grid place-items-center font-bold">−</button>
            </div>
            <button onClick={() => onRemove?.()} className="text-xs text-red-500 mr-auto">حذف</button>
          </div>
        )}
      </div>
    </div>
  );
}
