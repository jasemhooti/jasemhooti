from telegram import InlineKeyboardButton, InlineKeyboardMarkup

# می‌توانید کیبوردهای مربوط به پنل مدیریت ادمین را در اینجا تعریف کنید
# مثال:
def get_admin_panel_keyboard():
    keyboard = [
        [InlineKeyboardButton("لیست سفارشات معلق", callback_data="list_pending")],
        [InlineKeyboardButton("تنظیمات ربات", callback_data="admin_settings")],
        # ... سایر دکمه‌ها
    ]
    return InlineKeyboardMarkup(keyboard)
