import { Link } from "react-router-dom";
import { SimpleHeader } from "../components/Header";
const CATS = [
  { name: "موبایل", count: "1,240 کالا", emoji: "📱", grad: "from-violet-500 to-indigo-500" },
  { name: "لپ‌تاپ و کامپیوتر", count: "860 کالا", emoji: "💻", grad: "from-sky-500 to-blue-500" },
  { name: "پوشاک مردانه", count: "2,100 کالا", emoji: "👔", grad: "from-zinc-700 to-zinc-900" },
  { name: "پوشاک زنانه", count: "3,400 کالا", emoji: "👗", grad: "from-rose-500 to-pink-500" },
  { name: "خانه و آشپزخانه", count: "980 کالا", emoji: "🏠", grad: "from-amber-500 to-orange-500" },
  { name: "زیبایی و سلامت", count: "1,600 کالا", emoji: "💄", grad: "from-pink-500 to-rose-500" },
  { name: "کتاب و لوازم تحریر", count: "720 کالا", emoji: "📚", grad: "from-emerald-500 to-teal-500" },
  { name: "ورزش و سفر", count: "540 کالا", emoji: "⚽", grad: "from-orange-500 to-red-500" },
];
export default function Categories() {
  return (
    <div className="bg-[#F8F8F9] min-h-screen">
      <SimpleHeader title="دسته‌بندی‌ها" subtitle="همه دسته‌ها" />
      <div className="px-4 mt-4 grid grid-cols-2 gap-3">
        {CATS.map(c => (
          <Link key={c.name} to={`/?category=${encodeURIComponent(c.name)}`} className="bg-white rounded-[20px] border border-zinc-100 p-4 flex flex-col gap-3 hover:shadow-md transition-shadow">
            <div className={`size-12 rounded-2xl bg-gradient-to-br ${c.grad} grid place-items-center text-2xl shadow`}>{c.emoji}</div>
            <div>
              <div className="font-black text-sm">{c.name}</div>
              <div className="text-xs text-zinc-500">{c.count}</div>
            </div>
            <div className="text-xs font-bold text-zinc-900">مشاهده →</div>
          </Link>
        ))}
      </div>
      <div className="px-4 mt-6 bg-white border border-zinc-100 rounded-[20px] p-4">
        <div className="font-black text-sm">برندهای محبوب</div>
        <div className="flex gap-2 mt-3 overflow-x-auto scrollbar-hide">
          {["Samsung", "Apple", "Nike", "Sony", "Anker", "چرم مشهد"].map(b => (
            <span key={b} className="shrink-0 bg-zinc-50 border border-zinc-100 px-4 py-2 rounded-full text-xs font-bold">{b}</span>
          ))}
        </div>
      </div>
      <div className="h-6" />
    </div>
  );
}
