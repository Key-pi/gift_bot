from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler
)
from config import BOT_TOKEN
import handlers
import logging



def main():
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_error_handler(handlers.error_handler)
    app.add_handler(CommandHandler("start", handlers.start))
    app.add_handler(CallbackQueryHandler(handlers.check_time, pattern="check"))
    app.add_handler(CallbackQueryHandler(handlers.send_gift, pattern="gift"))
    app.add_handler(CallbackQueryHandler(handlers.send_compliment, pattern="compliment"))
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
