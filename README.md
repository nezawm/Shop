# NezShop

بک‌اند فروشگاه اینترنتی نوشته‌شده با Django و Django REST Framework.

## امکانات

- **Accounts** — احراز هویت با OTP، پروفایل و آدرس کاربران
- **Products** — مدیریت محصولات، برندها، فیلتر و جستجو
- **Cart** — سبد خرید
- **Order** — سفارش‌ها و تسویه‌حساب
- **Discount** — کدهای تخفیف
- **Payment** — پرداخت
- **Report** — گزارش‌گیری
- مستندسازی API با drf-spectacular (Swagger UI)
- احراز هویت با JWT (`djangorestframework_simplejwt`)

## نصب و اجرا

1. کلون کردن پروژه و ساخت محیط مجازی:

   ```bash
   git clone <repo-url>
   cd NezShop_Project
   python -m venv venv
   source venv/bin/activate  # ویندوز: venv\Scripts\activate
   ```

2. نصب پکیج‌ها:

   ```bash
   pip install -r requirements.txt
   ```

3. تنظیم متغیرهای محیطی:

   ```bash
   cp .env.example .env
   # سپس مقادیر داخل .env را با مقادیر واقعی خودت جایگزین کن
   ```

4. اجرای مایگریشن‌ها و بالا آوردن سرور:

   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py runserver
   ```

5. مستندات API:
   - Swagger UI: `/api/schema/swagger-ui/` (بسته به تنظیمات urls.py پروژه)

## ساختار پروژه

```
NezShop_Project/
├── Accounts/     # کاربران، پروفایل، احراز هویت
├── Products/     # محصولات و برندها
├── Cart/         # سبد خرید
├── Order/        # سفارش‌ها
├── Discount/     # کدهای تخفیف
├── Payment/      # پرداخت
├── Report/       # گزارش‌ها
├── Core/         # ابزارها و کلاس‌های پایه مشترک
└── NezShop_Project/  # تنظیمات اصلی جنگو
```

## نکته امنیتی

فایل `db.sqlite3` و پوشه `media/` جزو این مخزن نیستند (در `.gitignore` قرار دارند) چون شامل داده و فایل‌های تست/محلی هستند. برای اجرای پروژه، بعد از migrate یک دیتابیس تازه ساخته می‌شود.
