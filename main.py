from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler
)
from config import BOT_TOKEN
import handlers


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", handlers.start))
    app.add_handler(CallbackQueryHandler(handlers.check_time, pattern="check"))
    app.add_handler(CallbackQueryHandler(handlers.send_gift, pattern="gift"))
    app.add_handler(CallbackQueryHandler(handlers.send_compliment, pattern="compliment"))
    app.run_polling(drop_pending_updates=True)

    app.run_polling()


if __name__ == "__main__":
    main()
