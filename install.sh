#!/bin/bash

# خروج در صورت بروز خطا
set -e

# پیام خوشامدگویی
echo "شروع فرآیند نصب ربات NetBox..."

# نصب پیش‌نیازها
echo "نصب پیش‌نیازها..."
sudo apt update
sudo apt install -y python3 python3-pip git screen python3-venv  # نصب python3-venv

# ارتقاء pip
pip3 install --upgrade pip

# دانلود سورس کد از گیت‌هاب
REPOSITORY_URL="https://github.com/jasemhooti/jasemhooti.git"
BOT_FOLDER="netbox_bot"

if [ -d "$BOT_FOLDER" ]; then
    echo "پوشه $BOT_FOLDER از قبل وجود دارد. حذف می‌شود..."
    rm -rf "$BOT_FOLDER"
fi

echo "دانلود سورس کد از $REPOSITORY_URL..."
git clone "$REPOSITORY_URL"

# رفتن به پوشه ربات
cd "$BOT_FOLDER"

# ایجاد محیط مجازی
echo "ایجاد محیط مجازی پایتون..."
python3 -m venv venv

# فعال کردن محیط مجازی
echo "فعال کردن محیط مجازی..."
source venv/bin/activate

# نصب کتابخانه‌های پایتون
echo "نصب کتابخانه‌های پایتون..."
pip install -r requirements.txt

# ایجاد فایل تنظیمات (اگر وجود ندارد) و جایگزینی مقادیر
if [ ! -f "config.py" ]; then
    echo "ایجاد فایل تنظیمات اولیه..."
    cp config.example.py config.py # فرض وجود یک فایل config.example.py
fi

# جایگزینی توکن ربات
sed -i "s/YOUR_BOT_TOKEN/6414210268:AAEL-RZiABoMzS_QY922hOQnpXcam9OgiF0/g" config.py
# جایگزینی ID ادمین
sed -i "s/YOUR_ADMIN_ID/5691972852/g" config.py
# جایگزینی نام ربات
sed -i "s/YOUR_BOT_NAME/NetBox/g" config.py
# جایگزینی شماره کارت (اختیاری)
sed -i "s/YOUR_PAYMENT_CARD_NUMBER/شماره کارت خود را اینجا وارد کنید/g" config.py
# جایگزینی ID کانال گزارشات (اختیاری)
sed -i "s/@YOUR_REPORT_CHANNEL_ID/@نام_کانال_یا_گروه_گزارشات/g" config.py
# جایگزینی آدرس پنل X-UI
sed -i "s/YOUR_XUI_PANEL_URL/http:\/\/irancell.jasemhooti1.ir:8443\//g" config.py
# جایگزینی نام کاربری پنل X-UI
sed -i "s/YOUR_XUI_PANEL_USERNAME/jasemhooti/g" config.py
# جایگزینی رمز عبور پنل X-UI
sed -i "s/YOUR_XUI_PANEL_PASSWORD/JasemhootI6906/g" config.py

# اجرای ربات در یک screen جداگانه از داخل محیط مجازی
echo "اجرای ربات در پس‌زمینه از داخل محیط مجازی..."
screen -dmS netbox_bot venv/bin/python main.py

echo "ربات NetBox با موفقیت نصب و اجرا شد!"
echo "برای مشاهده لاگ‌ها:"
echo "screen -r netbox_bot"

# غیرفعال کردن محیط مجازی (اختیاری، معمولاً نیازی نیست)
# deactivate
