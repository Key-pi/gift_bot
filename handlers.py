import os
import random
from datetime import datetime
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from telegram.ext import ContextTypes
from config import SECRET_TOKEN, OPEN_TIME, TIMEZONE
import logging




WHITE_LIST = [470878254]
# ---------- helpers ----------

def now():
    return datetime.now(TIMEZONE)


def format_time_left(delta):
    total_seconds = max(0, int(delta.total_seconds()))

    days = total_seconds // 86400
    hours = (total_seconds % 86400) // 3600
    minutes = (total_seconds % 3600) // 60

    parts = []
    if days:
        parts.append(f"{days} дн.")
    if hours:
        parts.append(f"{hours} ч.")
    if minutes:
        parts.append(f"{minutes} мин.")

    return " ".join(parts) if parts else "меньше минуты"


def load_compliments():
    try:
        with open("compliments.txt", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    except Exception as e:
        logging.exception("Failed to load compliments")
        return []


COMPLIMENTS = load_compliments()


def keyboard_before_time():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("💌 Комплимент", callback_data="compliment")],
        [InlineKeyboardButton("✨ Проверить позже", callback_data="check")]
    ])


def keyboard_after_time():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🎁 Получить подарок", callback_data="gift")],
        [InlineKeyboardButton("💌 Комплимент", callback_data="compliment")]
    ])


# ---------- handlers ----------
async def error_handler(update, context):
    logging.exception("Exception while handling update", exc_info=context.error)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "Этот бот принимает гостей только по приглашению ✨"
        )
        return

    if update.effective_user.id not in WHITE_LIST:
        await update.message.reply_text(
            "Не хорошо трогать чужие QR-коды 😡😡😡"
        )
        return

    token = context.args[0]

    if token != SECRET_TOKEN:
        await update.message.reply_text(
            "Магия не откликнулась… 💫"
        )
        return

    if now() < OPEN_TIME:
        time_left = OPEN_TIME - now()
        await update.message.reply_text(
            "Время волшебства ещё не наступило.\n\n"
            f"Осталось ждать: {format_time_left(time_left)}",
            reply_markup=keyboard_before_time()
        )
        return

    await update.message.reply_text(
        "Волшебство настало ✨",
        reply_markup=keyboard_after_time()
    )


async def check_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if now() < OPEN_TIME:
        time_left = OPEN_TIME - now()

        text = (
            "Ещё рано… подожди)💫\n\n"
            f"Осталось ждать: {format_time_left(time_left)}"
        )
        # если текст и кнопки те же — просто отвечаем на клик
        if query.message.text == text:
            return

        await query.edit_message_text(
            text,
            reply_markup=keyboard_before_time()
        )
        return

    await query.edit_message_text(
        "Волшебство настало ✨",
        reply_markup=keyboard_after_time()
    )


async def send_gift(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if now() < OPEN_TIME:
        await query.message.reply_text("Ещё чуть-чуть… 🕯️")
        return

    file_path = "gift.txt"

    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            await query.message.reply_document(
                document=InputFile(f, filename="gift.txt"),
                caption="С Новым годом ❤️"
            )
    else:
        await query.message.reply_text(
            "С Новым годом ❤️\n\nЭто твой подарок."
        )

async def send_compliment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if not COMPLIMENTS:
        await query.message.reply_text(
            "Я временно без слов… но это не навсегда 💭"
        )
        return

    compliment = random.choice(COMPLIMENTS)

    await query.message.reply_text(
        f"💌 {compliment}"
    )
