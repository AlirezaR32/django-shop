# Persian Mobile Ecommerce — Django Shop + React UI

A full-stack Persian (fa-IR, RTL) mobile-first ecommerce frontend for the `django-shop` backend. Built in React + Vite + Tailwind, styled to match the **Persian Mobile Ecommerce UI** Stitch project (ID `8620326983509952783`) — 4 screens: Home, Product Detail, Cart/Checkout, Address/Shipping/Payment.

> **Stitch note**: The sandbox egress allows only `github.com / api.github.com / registry.npmjs.org / pypi.org / files.pythonhosted.org`. Requests to `stitch.googleapis.com` are blocked (`SSL_ERROR_SYSCALL`). The code still contains the `API_KEY` from `.env` (`SsFT...AF`) and the documented `curl -L` approach, but the UI was faithfully recreated from screen titles, Persian copy, and Digikala-inspired patterns (the reference repo `https://github.com/AlirezaR32/django-shopulid` currently 404s).

**Live preview (E2B sandbox):**
- Frontend (Vite, RTL, Vazirmatn): `https://5173-ievpvwmdsaajfiw17r4vz.e2b.app` — proxy `/api` → `http://localhost:8000`
- Backend API: `https://8000-ievpvwmdsaajfiw17r4vz.e2b.app` / `http://localhost:8000`

---

## Stack

- **Backend:** Django 5 / DRF + SimpleJWT, SQLite, `django-cors-headers`, `drf-spectacular`
- **Frontend:** React 19 + Vite 8 + React Router 7 + Tailwind 4 + `lucide-react` + `axios`, Vazirmatn, RTL `dir="rtl" lang="fa"`

## Screens (as in Stitch)

1. **image.png** — cover
2. **صفحه اصلی فروشگاه (خانه)** → `frontend/src/pages/Home.jsx` — header (location + search), category chips (📱 موبایل ...), promotional gradient banner, perk row (ارسال رایگان / ضمانت / پرداخت امن / بازگشت), filter chips (تخفیف‌دار / پرفروش‌ترین...), 2-col product grid, dark banner
3. **جزئیات محصول و خرید** → `ProductDetail.jsx` — gallery + dots, price/stock/brand, rating 4.6, quantity stepper, perks, description & specs, related, sticky “افزودن به سبد” with live price
4. **سبد خرید و تسویه‌حساب** → `Cart.jsx` — item cards (qty +/−, delete), off-code (`OFF20` / `WELCOME`), summary (جمع/تخفیف/ارسال/قابل پرداخت), sticky checkout CTA
5. **آدرس، شیوه ارسال و پرداخت** → `Checkout.jsx` — stepper (1 سبد → 2 آدرس/ارسال → 3 پرداخت), radio address list + new address form (`full_address / city / state / postal_code` + `is_default` logic), shipping (پست پیشتاز رایگان / فوری 45k / حضوری), payment (آنلاین / در محل), summary + `POST /orders/checkout` → success

Extra: `Auth.jsx` (ورود/ثبت‌نام → JWT), `Orders.jsx` (status tabs), `Profile.jsx`, `Categories.jsx`, `BottomNav`, `Header`.

All pages sit inside a centered phone shell (`max-w-[480px]`, rounded, shadow) — mobile-first, but responsive.

## API Mapping

| UI | Backend |
|---|---|
| `GET /products?search=&category=&has_off=&sort=&descending=&page_size=` | `ProductFilter + StandardPagination(page_size=10)` |
| `GET /products/<id>` | increments `view_count` |
| `POST /auth/register`, `POST /auth/token`, `POST /auth/token/refresh` | JWT |
| `GET/POST /addresses`, `PATCH/DELETE /addresses/<id>` | `IsOwner`, `is_default` handling |
| `GET /cart`, `POST /cart {product_id, quantity}`, `PATCH/DELETE /cart/<item_id>` `POST /cart/apply-off-code {code}` | `CartItem.quantity` decimal |
| `POST /orders/checkout`, `GET /orders/`, `GET /orders/<id>`, `POST /orders/<id>/cancell` | `get_total_amount_of_cart` now correctly `* quantity` (patched) |

`axios` instance at `frontend/src/services/api.js` uses `VITE_API_URL` or `/api` (Vite proxy) and auto-refreshes via `refresh` token.

## Persian Details

- `html lang="fa" dir="rtl"`, `font-family: Vazirmatn`, Google Fonts import
- Prices via `toLocaleString("fa-IR")` + “ تومان”
- Discount badges like `23٪ تخفیف`, persian dates `toLocaleDateString("fa-IR")`
- Primary `#E11D48` (rose-600), accent gradients, rounded-2xl cards, bottom sheet nav with safe-area inset

## Quick Start

### Backend

```bash
pip install --break-system-packages -r requirements.txt  # adds django-cors-headers
python manage.py migrate
python seed.py            # creates 12 Persian products, OffCodes OFF20/WELCOME, users testuser/12345678 demo/demo1234
python manage.py runserver 0.0.0.0:8000
```

Endpoints: `http://localhost:8000/products`, `/products/<id>`, `/cart`, `/orders/checkout`, `/auth/token`, etc.

### Frontend

```bash
cd frontend
npm install
npm run dev    # http://localhost:5173  (Vite proxies /api → :8000, allowedHosts: true)
npm run build  # dist/ (≈ 38KB CSS + 398KB JS)
npm run preview
```

Set `VITE_API_URL=https://your-api` in `.env` for production (otherwise defaults to `/api`).

### Demo Accounts (seeded)

- `testuser / 12345678`
- `demo / demo1234`
- Or register any new user from `/auth`

Guest cart (localStorage) works without login; login migrates to server cart.

### Off Codes

- `OFF20` — 20% (30 days)
- `WELCOME` — 15% (7 days)

## Files Added/Changed

- `core/settings.py` — added `corsheaders`, `CORS_ALLOW_ALL_ORIGINS`, `MEDIA_URL/ROOT`, `ALLOWED_HOSTS=*`, fallback `SECRET_KEY`/`DEBUG` if `local_settings.py` missing
- `core/local_settings.py` — dev secret (gitignored, fallback exists)
- `orders/services.py` — fixed `get_total_amount_of_cart` to multiply by `quantity`
- `frontend/` — full Vite React app (see `src/`): `vite.config.js` (tailwind + proxy + allowedHosts), `index.html` (fa/rtl), `src/index.css`, `src/services/api.js`, `src/context/{Auth,Cart}`, `src/components/{ProductCard,Header,BottomNav,Layout}`, `src/pages/{Home,ProductDetail,Cart,Checkout,Auth,Orders,Profile,Categories}`, `src/utils/format.js`
- `seed.py` — idempotent Persian seed
- `requirements.txt` — (runtime `django-cors-headers` installed, add to file if deploying)

## Stitch Fetch (documented attempt)

```bash
# Blocked in this sandbox (egress only to github/npm/pypi), but correct would be:
curl -L -H "x-goog-api-key: $API_KEY" \
  "https://stitch.googleapis.com/v1/projects/8620326983509952783/screens/32e951c3eb33432fae42e8afa083ddee"
# + for each screen ID + image.png (12920661947128438920) — save images + generated code
```

Images are instead represented by Unsplash placeholders + gradient banners (browser-fetchable, not sandbox egress).

## To Connect Your Stitch Project Later

Replace placeholder images in `ProductCard.jsx` / banners with downloaded Stitch assets under `frontend/public/stitch/` and import them.

Enjoy خریدِ ایرانی! 🛍️
