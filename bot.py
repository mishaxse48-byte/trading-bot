import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import random

# Токен та chat_id
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TG_CHAT_ID = os.environ.get("TG_CHAT_ID")

sending_signals = False

# Валютні пари з ймовірністю вигідності (%)
currency_pairs = {
    "AED/CNY OTC": 92,
    "AUD/CAD OTC": 92,
    "AUD/CHF OTC": 92,
    "AUD/NZD OTC": 92,
    "AUD/USD OTC": 92,
    "CAD/CHF OTC": 92,
    "CHF/JPY OTC": 92,
    "EUR/GBP OTC": 92,
    "EUR/TRY OTC": 92,
    "EUR/USD OTC": 92,
    "NZD/JPY OTC": 92,
    "UAH/USD OTC": 92,
    "USD/JPY OTC": 58,
    "GBP/USD OTC": 64,
    # додаємо всі інші пари з твоєї таблиці...
}

def pick_best_pair():
    """Вибирає валютну пару з максимальною ймовірністю ≥ 70%"""
    best_pairs = {pair: chance for pair, chance in currency_pairs.items() if chance >= 70}
    if not best_pairs:
        return None
    # обираємо випадкову з найвищою ймовірністю
    max_chance = max(best_pairs.values())
    top_pairs = [pair for pair, chance in best_pairs.items() if chance == max_chance]
    return random.choice(top_pairs)

async def send_signal(app):
    """Надіслати сигнал з найвигіднішою парою"""
    pair = pick_best_pair()
    if not pair:
        print("Немає пар для сигналу з достатньою ймовірністю")
        return
    try:
        await app.bot.send_message(
            chat_id=int(TG_CHAT_ID),
            text=f"📈 Сигнал на 5-хвилинний таймфрейм: {pair}\nЙмовірність вигоди: {currency_pairs[pair]}%"
        )
    except Exception as e:
        print(f"Помилка надсилання сигналу: {e}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global sending_signals
    if sending_signals:
        await update.message.reply_text("Сигнали вже надсилаються ⏳")
        return
    sending_signals = True
    chat_id = update.effective_chat.id
    await update.message.reply_text(f"Бот запущено. Твій chat_id: {chat_id}")
    await update.message.reply_text("Надсилання 3 сигналів через 3 хвилини ✅")

    for i in range(3):
        if not sending_signals:
            break
        await send_signal(context.application)
        if i < 2:
            await asyncio.sleep(180)  # 3 хвилини
    sending_signals = False
    await update.message.reply_text("Всі сигнали надіслані або надсилання зупинено ⛔")

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global sending_signals
    sending_signals = False
    await update.message.reply_text("Сигнали зупинено ⛔")

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stop", stop))
    app.run_polling()

if __name__ == "__main__":
    main()
