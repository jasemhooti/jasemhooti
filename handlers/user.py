from telegram import Update
from telegram.ext import CallbackContext
from database import get_db, VPNPackage, User
from keyboards.user import get_package_keyboard

def start(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    username = update.effective_user.username
    first_name = update.effective_user.first_name
    last_name = update.effective_user.last_name

    db = next(get_db())
    user = db.query(User).filter(User.telegram_id == user_id).first()
    if not user:
        new_user = User(telegram_id=user_id, username=username, first_name=first_name, last_name=last_name)
        db.add(new_user)
        db.commit()

    update.message.reply_text(f"سلام {first_name} عزیز!\nبه ربات {context.bot_data['bot_name']} خوش آمدید.")

    packages = db.query(VPNPackage).all()
    if packages:
        update.message.reply_text("لطفاً حجم مورد نظر خود را انتخاب کنید:", reply_markup=get_package_keyboard(packages))
    else:
        update.message.reply_text("در حال حاضر بسته‌ای برای فروش موجود نیست.")

def show_packages(update: Update, context: CallbackContext):
    db = next(get_db())
    packages = db.query(VPNPackage).all()
    if packages:
        update.message.reply_text("لطفاً حجم مورد نظر خود را انتخاب کنید:", reply_markup=get_package_keyboard(packages))
    else:
        update.message.reply_text("در حال حاضر بسته‌ای برای فروش موجود نیست.")

def handle_package_selection(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    package_id = int(query.data.split("_")[1])
    db = next(get_db())
    package = db.query(VPNPackage).filter(VPNPackage.id == package_id).first()
    if package:
        context.user_data['selected_package'] = package
        query.edit_message_text(f"شما بسته {package.name} با حجم {package.size_gb}GB و قیمت {package.price} تومان را انتخاب کردید.\nبرای خرید، دکمه پرداخت را بزنید.",
                               reply_markup=get_payment_keyboard(package.id)) # نیاز به تغییر در کیبورد
    else:
        query.edit_message_text("بسته مورد نظر یافت نشد.")

# ... سایر هندلرهای مربوط به کاربر
