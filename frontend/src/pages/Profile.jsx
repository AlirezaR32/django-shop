import { Link } from "react-router-dom";
import { SimpleHeader } from "../components/Header";
import { useAuth } from "../context/AuthContext";
import { User, Package, MapPin, Heart, ShieldCheck, LogOut, ChevronLeft, Settings, Gift, Headset } from "lucide-react";

export default function Profile() {
  const { user, logout, isAuthed } = useAuth();

  if (!isAuthed) {
    return (
      <div className="bg-[#F8F8F9] min-h-screen">
        <SimpleHeader title="حساب کاربری" />
        <div className="px-4 mt-6">
          <div className="bg-white rounded-[24px] border border-zinc-100 p-6 text-center">
            <div className="size-20 rounded-full bg-zinc-900 text-white grid place-items-center mx-auto text-xl font-black">فا</div>
            <h3 className="font-black text-base mt-4">وارد حساب شوید</h3>
            <p className="text-sm text-zinc-500 mt-1">برای مشاهده سفارش‌ها و آدرس‌ها وارد شوید</p>
            <Link to="/auth" className="inline-flex mt-5 bg-[#E11D48] text-white font-black px-8 py-3 rounded-full">ورود / ثبت‌نام</Link>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-[#F8F8F9] min-h-screen pb-8">
      <SimpleHeader title="حساب کاربری" />
      <div className="px-4 mt-4">
        <div className="bg-gradient-to-br from-zinc-900 to-zinc-800 rounded-[24px] p-5 text-white flex items-center gap-4 relative overflow-hidden">
          <div className="absolute -right-6 -top-6 size-32 bg-white/10 rounded-full blur-2xl" />
          <div className="size-14 rounded-full bg-white text-zinc-900 grid place-items-center font-black text-lg relative">فا</div>
          <div className="relative">
            <div className="font-black">{user.username}</div>
            <div className="text-xs opacity-70">کاربر فروشگاه ایرانی • عضو از 1403</div>
            <div className="inline-flex mt-2 bg-white text-zinc-900 text-[11px] font-black px-3 py-1 rounded-full">سطح: طلایی ✨</div>
          </div>
          <Link to="/cart" className="mr-auto relative bg-white/10 backdrop-blur p-3 rounded-full border border-white/10"><Settings size={16} /></Link>
        </div>
      </div>

      <div className="px-4 mt-4 grid grid-cols-4 gap-2">
        {[
          { to: "/orders", label: "سفارش‌ها", icon: Package, count: "3" },
          { to: "/cart", label: "سبد خرید", icon: Gift, count: "2" },
          { to: "/checkout", label: "آدرس‌ها", icon: MapPin, count: "2" },
          { to: "/", label: "علاقه‌مندی", icon: Heart, count: "12" },
        ].map(i => (
          <Link key={i.label} to={i.to} className="bg-white rounded-2xl border border-zinc-100 p-3 flex flex-col items-center gap-2">
            <div className="relative size-10 rounded-full bg-zinc-50 border border-zinc-100 grid place-items-center">
              <i.icon size={18} />
              <span className="absolute -top-1 -right-1 bg-[#E11D48] text-white text-[10px] leading-none px-1.5 py-1 rounded-full font-bold">{i.count}</span>
            </div>
            <span className="text-xs font-bold">{i.label}</span>
          </Link>
        ))}
      </div>

      <div className="px-4 mt-4 space-y-3">
        <div className="bg-white rounded-[20px] border border-zinc-100 overflow-hidden divide-y divide-zinc-100">
          {[
            { label: "سفارش‌های من", sub: "پیگیری و تاریخچه", icon: Package, to: "/orders" },
            { label: "آدرس‌ها", sub: "مدیریت آدرس‌های ارسال", icon: MapPin, to: "/checkout" },
            { label: "پشتیبانی", sub: "021-12345678", icon: Headset, to: "/" },
            { label: "تنظیمات", sub: "حریم خصوصی و اعلان‌ها", icon: Settings, to: "/" },
          ].map(row => (
            <Link key={row.label} to={row.to} className="flex items-center gap-3 p-4 hover:bg-zinc-50 transition-colors">
              <div className="size-10 rounded-full bg-zinc-50 border border-zinc-100 grid place-items-center"><row.icon size={18} className="text-zinc-700" /></div>
              <div className="flex-1">
                <div className="font-bold text-sm">{row.label}</div>
                <div className="text-xs text-zinc-500">{row.sub}</div>
              </div>
              <ChevronLeft size={16} className="text-zinc-400" />
            </Link>
          ))}
        </div>

        <button onClick={logout} className="w-full bg-white border border-zinc-100 rounded-full py-3.5 flex items-center justify-center gap-2 font-bold text-red-600">
          <LogOut size={16} /> خروج از حساب
        </button>

        <div className="bg-emerald-50 border border-emerald-100 rounded-2xl p-4 flex gap-3 text-xs leading-6 text-emerald-800">
          <ShieldCheck size={18} className="shrink-0" /> حساب شما با JWT امن شده است. توکن‌ها پس از 60 دقیقه منقضی می‌شوند.
        </div>

        <div className="text-center text-[11px] text-zinc-400 pt-2">نسخه 1.0.0 • فروشگاه ایرانی — ساخته شده با Django + React</div>
      </div>
    </div>
  );
}
