from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler
)
from config import BOT_TOKEN
import handlers
import logging
from telegram.error import NetworkError
import asyncio


async def watchdog(context):
    logging.info("Bot alive")

def post_init(application):
    application.job_queue.run_repeating(
        watchdog,
        interval=60,
        first=60,
    )

def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.FileHandler("bot.log"),
            logging.StreamHandler(),
        ],
    )

    app = ApplicationBuilder().token(BOT_TOKEN).post_init(post_init).build()

    app.add_error_handler(handlers.error_handler)
    app.add_handler(CommandHandler("start", handlers.start))
    app.add_handler(CallbackQueryHandler(handlers.check_time, pattern="check"))
    app.add_handler(CallbackQueryHandler(handlers.send_gift, pattern="gift"))
    app.add_handler(CallbackQueryHandler(handlers.send_compliment, pattern="compliment"))
    app.run_polling(drop_pending_updates=True)

    # raise RuntimeError("TEST CRASH")


if __name__ == "__main__":
    main()
