#!/bin/bash
set -e

echo "شروع تست محیط مجازی..."

# رفتن به پوشه ربات (فرض بر اینکه کد قبلاً دانلود شده)
cd netbox_bot

# ایجاد محیط مجازی
echo "ایجاد محیط مجازی..."
python3 -m venv venv

# فعال کردن محیط مجازی
echo "فعال کردن محیط مجازی..."
source venv/bin/activate

# نصب یک بسته ساده
echo "نصب بسته requests..."
venv/bin/pip install requests

echo "تست به پایان رسید."
