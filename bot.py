import os
import asyncio
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# 🔑 Твій API ключ Alpha Vantage
ALPHA_VANTAGE_KEY = "TMCO3557CFCJRLRX"

# ⚡ Дані для Telegram
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TG_CHAT_ID = os.environ.get("TG_CHAT_ID")

sending_signals = False

# 📊 Отримання реальних даних з Alpha Vantage
def get_forex_signal(pair="EUR/USD"):
    from_symbol, to_symbol = pair.split("/")
    url = (
        f"https://www.alphavantage.co/query?function=FX_INTRADAY&from_symbol={from_symbol}"
        f"&to_symbol={to_symbol}&interval=5min&apikey={ALPHA_VANTAGE_KEY}&outputsize=compact"
    )

    response = requests.get(url)
    data = response.json()

    if "Time Series FX (5min)" not in data:
        return None

    candles = data["Time Series FX (5min)"]
    times = sorted(candles.keys(), reverse=True)

    if len(times) < 2:
        return None

    last = candles[times[0]]
    prev = candles[times[1]]

    last_close = float(last["4. close"])
    prev_close = float(prev["4. close"])

    direction = "UP 📈 (Buy)" if last_close > prev_close else "DOWN 📉 (Sell)"
    probability = round(abs((last_close - prev_close) / prev_close) * 100, 2)

    return {
        "pair": pair,
        "direction": direction,
        "last_close": last_close,
        "probability": probability,
    }

# 📤 Надсилаємо сигнал у Telegram
async def send_signal(app, pair="EUR/USD"):
    signal = get_forex_signal(pair)
    if signal:
        message = (
            f"📊 Сигнал на 5-хв таймфрейм\n"
            f"Валютна пара: {signal['pair']}\n"
            f"Напрямок: {signal['direction']}\n"
            f"Ймовірність: {signal['probability']}%\n"
            f"Ціна: {signal['last_close']}"
        )
        await app.bot.send_message(chat_id=int(TG_CHAT_ID), text=message)
    else:
        await app.bot.send_message(chat_id=int(TG_CHAT_ID), text="❌ Не вдалося отримати сигнал")

# 🚀 Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global sending_signals
    chat_id = update.effective_chat.id
    await update.message.reply_text(f"Бот запущено. Твій chat_id: {chat_id}")

    if sending_signals:
        await update.message.reply_text("Сигнали вже надсилаються ⏳")
        return

    sending_signals = True
    await update.message.reply_text("Надсилання 3 сигналів через 3 хвилини ✅")

    # Відправляємо 3 сигнали підряд кожні 3 хвилини
    pairs = ["EUR/USD", "GBP/USD", "AUD/USD", "USD/JPY"]
    for i in range(3):
        if not sending_signals:
            break
        pair = pairs[i % len(pairs)]
        await send_signal(context.application, pair)
        if i < 2:
            await asyncio.sleep(180)

    sending_signals = False
    await update.message.reply_text("✅ Всі сигнали надіслані або надсилання зупинено ⛔")

# 🛑 Команда /stop
async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global sending_signals
    sending_signals = False
    await update.message.reply_text("Сигнали зупинено ⛔")

# 🔧 Головна функція
def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stop", stop))
    app.run_polling()

if __name__ == "__main__":
    main()
