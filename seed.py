from decimal import Decimal
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()
from products.models import Category, Brand, Product, OffCode
from users.models import User
from django.utils import timezone
from datetime import timedelta

# Clear
# Category
cats = {}
for name in ["موبایل", "لپ‌تاپ", "پوشاک", "خانه و آشپزخانه", "زیبایی", "کتاب", "ساعت"]:
    c, _ = Category.objects.get_or_create(name=name)
    cats[name] = c

brands_data = [
    ("Samsung", "https://logo.clearbit.com/samsung.com"),
    ("Apple", "https://logo.clearbit.com/apple.com"),
    ("Sony", "https://logo.clearbit.com/sony.com"),
    ("Nike", "https://logo.clearbit.com/nike.com"),
    ("Anker", None),
    ("چرم مشهد", None),
    ("شیائومی", None),
]

brands = {}
for name, logo in brands_data:
    b, _ = Brand.objects.get_or_create(name=name, defaults={"logo": logo})
    brands[name] = b

products = [
    {"title": "گوشی موبایل سامسونگ Galaxy S23 Ultra", "short_desc": "256 گیگ، 12 گیگ رم، قلم S Pen", "desc": "بهترین پرچمدار سامسونگ با دوربین 200 مگاپیکسل و شارژ سریع 45 وات. مناسب عکاسی حرفه‌ای و گیم.", "price": 48500000, "off_percent": Decimal("0.12"), "category": cats["موبایل"], "brand": brands["Samsung"], "stock_quantity": 25, "review_avg_point": Decimal("4.6"), "review_count": 342, "sell_count": 89, "view_count": 5420},
    {"title": "آیفون 15 Pro Max — 256GB", "short_desc": "تیتانیوم، دوربین سه‌گانه، A17 Pro", "desc": "آیفون جدید با بدنه تیتانیومی و پردازنده گرافیکی قدرتمند. انتخاب حرفه‌ای‌ها.", "price": 72000000, "off_percent": Decimal("0.05"), "category": cats["موبایل"], "brand": brands["Apple"], "stock_quantity": 12, "review_avg_point": Decimal("4.8"), "review_count": 521, "sell_count": 120, "view_count": 8120},
    {"title": "هدفون بی‌سیم سونی WH-1000XM5", "short_desc": "نویز کنسلینگ، 30 ساعت پخش", "desc": "بهترین هدفون نویز کنسلینگ بازار با کیفیت صدای Hi-Res و میکروفون 8 گانه.", "price": 18500000, "off_percent": Decimal("0.23"), "category": cats["موبایل"], "brand": brands["Sony"], "stock_quantity": 40, "review_avg_point": Decimal("4.7"), "review_count": 210, "sell_count": 67, "view_count": 3200},
    {"title": "لپ‌تاپ ایسوس VivoBook 15", "short_desc": "Core i5، 16GB RAM، 512 SSD", "desc": "لپ‌تاپ سبک و قدرتمند برای کار و تحصیل. نمایشگر 15.6 اینچی FHD.", "price": 38000000, "off_percent": Decimal("0.10"), "category": cats["لپ‌تاپ"], "brand": brands["Anker"], "stock_quantity": 8, "review_avg_point": Decimal("4.4"), "review_count": 89, "sell_count": 34, "view_count": 2100},
    {"title": "کفش نایک Air Max 270", "short_desc": "سبک، تنفس‌پذیر، مناسب دویدن", "desc": "کفش ورزشی با کوشن فوق‌العاده و طراحی مدرن.", "price": 5600000, "off_percent": Decimal("0.00"), "category": cats["پوشاک"], "brand": brands["Nike"], "stock_quantity": 60, "review_avg_point": Decimal("4.3"), "review_count": 156, "sell_count": 200, "view_count": 4300},
    {"title": "کیف چرم طبیعی دست‌دوز", "short_desc": "جنس چرم گاوی، جادار", "desc": "کیف دستی چرم طبیعی با دوخت دستی و یراق آلات فلزی.", "price": 3200000, "off_percent": Decimal("0.25"), "category": cats["پوشاک"], "brand": brands["چرم مشهد"], "stock_quantity": 30, "review_avg_point": Decimal("4.9"), "review_count": 67, "sell_count": 45, "view_count": 1800},
    {"title": "ساعت هوشمند اپل واچ سری 9", "short_desc": "45mm، GPS، حسگر سلامت", "desc": "اپل واچ جدید با چیپ S9 و صفحه نمایش همیشه روشن.", "price": 22000000, "off_percent": Decimal("0.10"), "category": cats["ساعت"], "brand": brands["Apple"], "stock_quantity": 18, "review_avg_point": Decimal("4.6"), "review_count": 98, "sell_count": 56, "view_count": 2900},
    {"title": "پاوربانک انکر 20000mAh", "short_desc": "شارژ سریع 22.5W، دو پورت", "desc": "پاوربانک قدرتمند با قابلیت شارژ همزمان دو دستگاه.", "price": 1800000, "off_percent": Decimal("0.25"), "category": cats["موبایل"], "brand": brands["Anker"], "stock_quantity": 100, "review_avg_point": Decimal("4.5"), "review_count": 340, "sell_count": 320, "view_count": 5600},
    {"title": "ادو پرفیوم زنانه — 100ml", "short_desc": "رایحه گرم و شیرین، ماندگاری بالا", "desc": "عطری جذاب برای مناسبت‌های خاص با پخش بوی عالی.", "price": 2400000, "off_percent": Decimal("0.30"), "category": cats["زیبایی"], "brand": brands["چرم مشهد"], "stock_quantity": 45, "review_avg_point": Decimal("4.2"), "review_count": 78, "sell_count": 90, "view_count": 1500},
    {"title": "سرویس قابلمه 10 پارچه", "short_desc": "گرانیت، نچسب، مناسب 6 نفر", "desc": "سرویس کامل آشپزخانه با پوشش گرانیت و دسته نسوز.", "price": 8900000, "off_percent": Decimal("0.15"), "category": cats["خانه و آشپزخانه"], "brand": brands["Anker"], "stock_quantity": 12, "review_avg_point": Decimal("4.4"), "review_count": 42, "sell_count": 21, "view_count": 900},
    {"title": "کتاب هوش مصنوعی — مقدماتی", "short_desc": "از صفر تا حرفه‌ای، 320 صفحه", "desc": "کتابی جامع برای یادگیری مفاهیم هوش مصنوعی با مثال‌های عملی.", "price": 450000, "off_percent": Decimal("0.00"), "category": cats["کتاب"], "brand": brands["چرم مشهد"], "stock_quantity": 80, "review_avg_point": Decimal("4.8"), "review_count": 112, "sell_count": 150, "view_count": 1100},
    {"title": "گوشی شیائومی Redmi Note 13", "short_desc": "128GB، دوربین 108MP", "desc": "گوشی اقتصادی با نمایشگر AMOLED 120 هرتز.", "price": 12500000, "off_percent": Decimal("0.08"), "category": cats["موبایل"], "brand": brands["شیائومی"], "stock_quantity": 35, "review_avg_point": Decimal("4.5"), "review_count": 203, "sell_count": 110, "view_count": 4100},
]

for p in products:
    if not Product.objects.filter(title=p["title"]).exists():
        Product.objects.create(**p)
        print(f"created {p['title']}")

# Off code
code, created = OffCode.objects.get_or_create(code="OFF20", defaults={"off_percent": Decimal("0.20"), "expire_duration": timedelta(days=30)})
if created:
    print("off code OFF20 created")
code2, _ = OffCode.objects.get_or_create(code="WELCOME", defaults={"off_percent": Decimal("0.15"), "expire_duration": timedelta(days=7)})
# test user
if not User.objects.filter(username="testuser").exists():
    User.objects.create_user(username="testuser", password="12345678")
    print("testuser created")
if not User.objects.filter(username="demo").exists():
    User.objects.create_user(username="demo", password="demo1234")
    print("demo created")

print(f"Total products: {Product.objects.count()}")
