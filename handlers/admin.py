from telegram import Update
from telegram.ext import CallbackContext
from database import get_db, Order, User, VPNPackage
from keyboards.user import get_package_keyboard  # ممکن است نیاز به کیبورد ادمین داشته باشید
from keyboards.admin import get_admin_confirmation_keyboard, get_admin_panel_keyboard
from utils.xui_api import login_to_xui, create_xui_config  # ایمپورت توابع X-UI

def admin_panel(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if user_id == context.bot_data['admin_id']:
        update.message.reply_text("به پنل مدیریت خوش آمدید!\nدر اینجا می‌توانید تنظیمات ربات را مدیریت کنید.", reply_markup=get_admin_panel_keyboard())
    else:
        update.message.reply_text("شما دسترسی به این بخش را ندارید.")

def list_pending_orders(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if user_id == context.bot_data['admin_id']:
        db = next(get_db())
        pending_orders = db.query(Order).filter(Order.payment_status == "pending").all()
        if pending_orders:
            for order in pending_orders:
                user = db.query(User).filter(User.id == order.user_id).first()
                package = db.query(VPNPackage).filter(VPNPackage.id == order.package_id).first()
                if user and package:
                    update.message.reply_photo(photo=order.receipt_photo_id,
                                             caption=f"سفارش جدید:\nکاربر: {user.first_name} {user.last_name} ({user.username})\nحجم: {package.name} ({package.size_gb}GB)\nقیمت: {package.price} تومان",
                                             reply_markup=get_admin_confirmation_keyboard(order.id))
        else:
            update.message.reply_text("در حال حاضر هیچ سفارش در انتظار تاییدی وجود ندارد.")
    else:
        update.message.reply_text("شما دسترسی به این بخش را ندارید.")

def handle_admin_confirmation(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    order_id = int(query.data.split("_")[2])
    action = query.data.split("_")[0]
    db = next(get_db())
    order = db.query(Order).filter(Order.id == order_id).first()
    if order:
        user = db.query(User).filter(User.id == order.user_id).first()
        package = db.query(VPNPackage).filter(VPNPackage.id == order.package_id).first()
        if action == "confirm":
            order.payment_status = "confirmed"
            order.admin_confirmed = True
            order.admin_confirmation_date = datetime.utcnow()

            # تعامل با پنل X-UI برای ایجاد کانفیگ
            session = login_to_xui()
            if session:
                xui_config_link = create_xui_config(session, user.username, package.__dict__) # __dict__ برای دسترسی ساده به مشخصات بسته
                if xui_config_link:
                    order.xui_config_id = xui_config_link # در صورت دریافت لینک مستقیم
                    db.commit()
                    context.bot.send_message(chat_id=user.telegram_id,
                                             text=f"سفارش شما برای بسته {package.name} تایید شد.\nلینک کانفیگ شما: {xui_config_link}")
                    context.bot.send_message(chat_id=context.bot_data['report_channel_id'],
                                             text=f"سفارش با شناسه {order.id} برای کاربر {user.username} تایید شد.")
                    query.edit_message_text(f"سفارش با شناسه {order.id} تایید شد.")
                else:
                    context.bot.send_message(chat_id=context.bot_data['admin_id'],
                                             text=f"خطا در ایجاد کانفیگ برای سفارش {order.id} کاربر {user.username}.")
                    query.edit_message_text(f"خطا در ایجاد کانفیگ برای سفارش {order.id}.")
            else:
                context.bot.send_message(chat_id=context.bot_data['admin_id'],
                                         text=f"خطا در اتصال به پنل X-UI برای سفارش {order.id} کاربر {user.username}.")
                query.edit_message_text(f"خطا در اتصال به پنل X-UI برای سفارش {order.id}.")

        elif action == "reject":
            order.payment_status = "rejected"
            db.commit()
            context.bot.send_message(chat_id=user.telegram_id,
                                     text=f"سفارش شما برای بسته {package.name} متاسفانه رد شد.")
            context.bot.send_message(chat_id=context.bot_data['report_channel_id'],
                                     text=f"سفارش با شناسه {order.id} برای کاربر {user.username} رد شد.")
            query.edit_message_text(f"سفارش با شناسه {order.id} رد شد.")
    else:
        query.edit_message_text("سفارش مورد نظر یافت نشد.")

# ... سایر هندلرهای مربوط به ادمین
