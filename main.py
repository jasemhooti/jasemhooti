import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from config import BOT_TOKEN, ADMIN_ID, BOT_NAME, REPORT_CHANNEL_ID, ADMIN_CONFIRMATION_TIMEOUT
from database import get_db
from handlers import user, admin, payment, game, support  # ایمپورت کردن هندلرها

# فعال کردن لاگینگ
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    # ذخیره تنظیمات سراسری در context.bot_data
    dp.bot_data['admin_id'] = ADMIN_ID
    dp.bot_data['bot_name'] = BOT_NAME
    dp.bot_data['report_channel_id'] = REPORT_CHANNEL_ID
    dp.bot_data['admin_confirmation_timeout'] = ADMIN_CONFIRMATION_TIMEOUT

    # هندلرهای مربوط به کاربر
    dp.add_handler(CommandHandler("start", user.start))
    dp.add_handler(CommandHandler("packages", user.show_packages))
    dp.add_handler(CallbackQueryHandler(user.handle_package_selection, pattern=r"^buy_\d+$"))

    # هندلرهای مربوط به پرداخت
    dp.add_handler(CallbackQueryHandler(payment.handle_buy_package, pattern=r"^payment_\d+$")) # نیاز به تغییر در pattern
    dp.add_handler(MessageHandler(Filters.photo, payment.receive_payment_receipt))

    # هندلرهای مربوط به ادمین
    dp.add_handler(CommandHandler("admin", admin.admin_panel))
    dp.add_handler(CommandHandler("pending_orders", admin.list_pending_orders))
    dp.add_handler(CallbackQueryHandler(admin.handle_admin_confirmation, pattern=r"^(confirm_order|reject_order)_\d+$"))

    # هندلرهای مربوط به بازی
    # dp.add_handler(...)

    # هندلرهای مربوط به پشتیبانی
    # dp.add_handler(...)

    # هندلرهای پیام‌های ناشناخته
    def unknown(update: Update, context: CallbackContext):
        update.message.reply_text("متوجه دستور شما نشدم.")
    dp.add_handler(MessageHandler(Filters.command, unknown))

    # شروع ربات
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
