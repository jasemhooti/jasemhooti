import os

# توکن ربات تلگرام
BOT_TOKEN = "6414210268:AAEL-RZiABoMzS_QY922hOQnpXcam9OgiF0"

# ID عددی ادمین
ADMIN_ID = 5691972852

# نام ربات
BOT_NAME = "NetBox"

# شماره کارت برای پرداخت
PAYMENT_CARD_NUMBER = "شماره کارت خود را اینجا وارد کنید"

# کانال یا گروه برای ارسال گزارشات
REPORT_CHANNEL_ID = "@نام_کانال_یا_گروه_گزارشات"  # با @ یا ID عددی

# تنظیمات مربوط به پنل X-UI (باید API پنل را بررسی کنید)
XUI_PANEL_URL = "http://irancell.jasemhooti1.ir:8443/"
XUI_PANEL_USERNAME = "jasemhooti"
XUI_PANEL_PASSWORD = "JasemhootI6906"

# مسیر پایگاه داده SQLite
DATABASE_FILE = "netbox.db"

# زمان انتظار برای تایید ادمین (ثانیه)
ADMIN_CONFIRMATION_TIMEOUT = 300  # 5 دقیقه

# هزینه شرکت در بازی
GAME_ENTRY_FEE = 500

# حداقل مبلغ شرط بندی در بازی
MIN_GAME_BET = 500

# حداکثر مبلغ شرط بندی در بازی
MAX_GAME_BET = 5000000

# لینک کانال اجباری (اگر فعال باشد)
FORCE_JOIN_CHANNEL_LINK = "لینک کانال تلگرام شما"
ENABLE_FORCE_JOIN = False  # True برای فعال کردن، False برای غیر فعال کردن
