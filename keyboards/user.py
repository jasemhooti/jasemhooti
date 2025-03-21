from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def get_package_keyboard(packages):
    keyboard =
    for package in packages:
        keyboard.append([InlineKeyboardButton(f"{package.name} ({package.size_gb}GB - {package.price} تومان)", callback_data=f"buy_{package.id}")])
    return InlineKeyboardMarkup(keyboard)

def get_payment_keyboard(order_id):
    keyboard = [[InlineKeyboardButton("ارسال رسید پرداخت", callback_data=f"send_receipt_{order_id}")]]
    return InlineKeyboardMarkup(keyboard)

def get_admin_confirmation_keyboard(order_id):
    keyboard = [
        [InlineKeyboardButton("تایید", callback_data=f"confirm_order_{order_id}"),
         InlineKeyboardButton("رد", callback_data=f"reject_order_{order_id}")]
    ]
    return InlineKeyboardMarkup(keyboard)

# ... سایر کیبوردها
