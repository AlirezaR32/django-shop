import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { SimpleHeader } from "../components/Header";
import { useAuth } from "../context/AuthContext";
import { Eye, EyeOff, ShieldCheck, Sparkles } from "lucide-react";

export default function Auth() {
  const [mode, setMode] = useState("login"); // login | register
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [show, setShow] = useState(false);
  const [err, setErr] = useState("");
  const { login, register, loading } = useAuth();
  const nav = useNavigate();

  const submit = async (e) => {
    e.preventDefault();
    setErr("");
    if (!username || !password) { setErr("نام کاربری و رمز را وارد کنید"); return; }
    try {
      if (mode === "login") await login(username, password);
      else await register(username, password);
      nav("/");
    } catch (e2) {
      const msg = e2?.response?.data?.detail || e2?.response?.data?.username?.[0] || "خطا در احراز هویت";
      if (String(msg).includes("No active account")) setErr("نام کاربری یا رمز اشتباه است");
      else if (String(msg).includes("already")) setErr("این نام کاربری قبلاً ثبت شده");
      else setErr(String(msg));
    }
  };

  return (
    <div className="bg-[#F8F8F9] min-h-screen flex flex-col">
      <SimpleHeader title={mode === "login" ? "ورود به حساب" : "ثبت‌نام"} subtitle="فروشگاه ایرانی" />
      <div className="flex-1 px-4 pt-6 pb-8">
        <div className="bg-gradient-to-br from-zinc-900 to-zinc-800 rounded-[24px] p-6 text-white relative overflow-hidden">
          <div className="absolute -right-10 -top-10 size-32 bg-white/10 rounded-full blur-2xl" />
          <h2 className="font-black text-xl leading-7 relative">به فروشگاه ایرانی خوش آمدید 👋</h2>
          <p className="text-sm opacity-80 mt-2 leading-6 relative">با ورود، سبد خرید، آدرس‌ها و سفارش‌هایتان همگام می‌شود.</p>
          <div className="flex gap-2 mt-4 relative">
            <span className="inline-flex items-center gap-1 bg-white/10 backdrop-blur border border-white/10 px-3 py-1.5 rounded-full text-xs font-bold"><Sparkles size={12} /> تخفیف اولین خرید</span>
            <span className="inline-flex items-center gap-1 bg-white text-zinc-900 px-3 py-1.5 rounded-full text-xs font-black">ارسال رایگان</span>
          </div>
        </div>

        <div className="bg-white rounded-[24px] border border-zinc-100 p-5 mt-4">
          <div className="flex bg-zinc-50 rounded-full p-1 border border-zinc-100">
            <button onClick={() => setMode("login")} className={`flex-1 py-2.5 rounded-full text-sm font-black transition-all ${mode === "login" ? "bg-zinc-900 text-white shadow" : "text-zinc-600"}`}>ورود</button>
            <button onClick={() => setMode("register")} className={`flex-1 py-2.5 rounded-full text-sm font-black transition-all ${mode === "register" ? "bg-zinc-900 text-white shadow" : "text-zinc-600"}`}>ثبت‌نام</button>
          </div>

          <form onSubmit={submit} className="mt-6 space-y-4">
            <div>
              <label className="text-xs font-bold text-zinc-700">نام کاربری</label>
              <input value={username} onChange={e => setUsername(e.target.value)} placeholder="مثلاً: alireza_32" className="mt-1 w-full bg-zinc-50 border border-zinc-200 rounded-full px-4 py-3.5 text-sm outline-none focus:border-zinc-900 focus:bg-white placeholder:text-zinc-400" />
            </div>
            <div>
              <label className="text-xs font-bold text-zinc-700">رمز عبور</label>
              <div className="relative mt-1">
                <input type={show ? "text" : "password"} value={password} onChange={e => setPassword(e.target.value)} placeholder="حداقل 8 کاراکتر" className="w-full bg-zinc-50 border border-zinc-200 rounded-full px-4 py-3.5 text-sm outline-none focus:border-zinc-900 focus:bg-white placeholder:text-zinc-400 pl-12" />
                <button type="button" onClick={() => setShow(v => !v)} className="absolute left-1 top-1 bottom-1 aspect-square grid place-items-center bg-white border border-zinc-200 rounded-full">
                  {show ? <EyeOff size={16} /> : <Eye size={16} />}
                </button>
              </div>
              <div className="text-[11px] text-zinc-500 mt-2 leading-4">رمز عبور بُر Django auth — ساده انتخاب کنید (مثلاً 12345678 برای تست)</div>
            </div>

            {err && <div className="bg-red-50 border border-red-100 text-red-700 text-xs font-bold p-3 rounded-2xl">{err}</div>}

            <button disabled={loading} className="w-full bg-[#E11D48] text-white font-black py-4 rounded-full hover:bg-[#be123c] disabled:opacity-60 transition-colors">
              {loading ? "لطفاً صبر کنید..." : mode === "login" ? "ورود به حساب" : "ایجاد حساب کاربری"}
            </button>

            <div className="flex items-center gap-2 text-xs text-zinc-500 justify-center">
              <ShieldCheck size={14} /> اطلاعات شما محفوظ و رمزگذاری شده است
            </div>
          </form>

          <div className="mt-6 text-center text-xs text-zinc-500">
            با ورود، <Link to="/" className="text-zinc-900 font-bold">قوانین و حریم خصوصی</Link> را می‌پذیرید
          </div>
        </div>

        {/* demo hint */}
        <div className="mt-4 bg-amber-50 border border-amber-100 rounded-2xl p-4 text-xs leading-6 text-amber-900">
          <div className="font-black">راهنمای سریع تست:</div>
          ۱) یک حساب بسازید (مثلاً <span className="font-mono bg-white px-1.5 py-0.5 rounded border">testuser / 12345678</span>)<br />
          ۲) سپس محصول به سبد اضافه کنید و با آدرس تستی تسویه کنید.<br />
          بدون لاگین هم می‌توانید خرید را ببینید — سبد مهمان فعال است.
        </div>
      </div>
    </div>
  );
}
