from telegram import Update
from telegram.ext import CallbackContext
from database import get_db, Order, VPNPackage, User
from config import PAYMENT_CARD_NUMBER
from keyboards.admin import get_admin_confirmation_keyboard
from utils.xui_api import login_to_xui, create_xui_config

def handle_buy_package(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    package = context.user_data.get('selected_package')
    if package:
        user_id = update.effective_user.id
        db = next(get_db())
        new_order = Order(user_id=user_id, package_id=package.id, payment_status="pending")
        db.add(new_order)
        db.commit()
        context.user_data['current_order_id'] = new_order.id
        query.edit_message_text(f"برای خرید بسته {package.name} به مبلغ {package.price} تومان، لطفاً مبلغ را به کارت زیر واریز کرده و رسید پرداخت را ارسال کنید:\n\nشماره کارت: `{PAYMENT_CARD_NUMBER}`",
                                parse_mode="Markdown",
                                reply_markup=None) # حذف کیبورد قبلی
    else:
        query.edit_message_text("ابتدا یک بسته را انتخاب کنید.")

def receive_payment_receipt(update: Update, context: CallbackContext):
    if update.message.photo:
        photo = update.message.photo[-1]
        order_id = context.user_data.get('current_order_id')
        if order_id:
            db = next(get_db())
            order = db.query(Order).filter(Order.id == order_id).first()
            if order:
                order.receipt_photo_id = photo.file_id
                db.commit()
                admin_id = context.bot_data['admin_id']
                package = db.query(VPNPackage).filter(VPNPackage.id == order.package_id).first()
                user = db.query(User).filter(User.id == order.user_id).first()
                if user and package:
                    context.bot.send_photo(chat_id=admin_id,
                                           photo=photo.file_id,
                                           caption=f"رسید پرداخت از کاربر {user.first_name} {user.last_name} ({user.username})\nبرای سفارش بسته {package.name} به مبلغ {package.price} تومان")
                    context.bot.send_message(chat_id=admin_id,
                                             text=f"لطفاً سفارش با شناسه {order_id} را بررسی و تایید کنید.",
                                             reply_markup=get_admin_confirmation_keyboard(order_id))
                    update.message.reply_text("رسید پرداخت شما دریافت شد. منتظر تایید ادمین باشید.")
                    context.job_queue.run_once(callback=auto_confirm_order,
                                               when=context.bot_data['admin_confirmation_timeout'],
                                               user_id=order.id,
                                               context={'order_id': order_id})
                else:
                    update.message.reply_text("خطایی در پردازش سفارش رخ داد.")
            else:
                update.message.reply_text("سفارش مورد نظر یافت نشد.")
        else:
            update.message.reply_text("ابتدا یک بسته را انتخاب و مراحل خرید را آغاز کنید.")
    else:
        update.message.reply_text("لطفاً رسید پرداخت را به صورت عکس ارسال کنید.")

def auto_confirm_order(context: CallbackContext):
    order_id = context.job.context['order_id']
    db = next(get_db())
    order = db.query(Order).filter(Order.id == order_id, Order.payment_status == "pending").first()
    if order:
        user = db.query(User).filter(User.id == order.user_id).first()
        package = db.query(VPNPackage).filter(VPNPackage.id == order.package_id).first()
        order.payment_status = "confirmed"
        order.admin_confirmed = True
        order.admin_confirmation_date = datetime.utcnow()
        # تعامل با پنل X-UI برای ایجاد کانفیگ
        session = login_to_xui()
        if session:
            xui_config_link = create_xui_config(session, user.username, package.__dict__)
            if xui_config_link:
                order.xui_config_id = xui_config_link
                db.commit()
                context.bot.send_message(chat_id=user.telegram_id,
                                         text=f"به دلیل عدم تایید ادمین در مهلت مقرر، سفارش شما برای بسته {package.name} به صورت خودکار تایید شد.\nلینک کانفیگ شما: {xui_config_link}")
                context.bot.send_message(chat_id=context.bot_data['report_channel_id'],
                                         text=f"سفارش با شناسه {order.id} برای کاربر {user.username} به صورت خودکار تایید شد.")
                admin_id = context.bot_data['admin_id']
                context.bot.send_message(chat_id=admin_id,
                                         text=f"سفارش با شناسه {order.id} برای کاربر {user.username} به صورت خودکار تایید شد.")
            else:
                admin_id = context.bot_data['admin_id']
                context.bot.send_message(chat_id=admin_id,
                                         text=f"خطا در ایجاد خودکار کانفیگ برای سفارش {order.id} کاربر {user.username}.")
        else:
            admin_id = context.bot_data['admin_id']
            context.bot.send_message(chat_id=admin_id,
                                     text=f"خطا در اتصال به پنل X-UI برای تایید خودکار سفارش {order.id} کاربر {user.username}.")

# ... سایر هندلرهای مربوط به پرداخت
