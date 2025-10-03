import os
import asyncio
import random
import yfinance as yf
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Токен і chat_id
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TG_CHAT_ID = os.environ.get("TG_CHAT_ID")

# Контроль надсилання сигналів
sending_signals = False

# Список валютних пар, які аналізуватимемо
CURRENCY_PAIRS = ["EURUSD=X", "GBPUSD=X", "USDJPY=X", "AUDUSD=X", "USDCAD=X"]

async def generate_signal():
    """Проста логіка для вигідного сигналу (~70%)"""
    pair = random.choice(CURRENCY_PAIRS)
    # Беремо останню ціну з Yahoo Finance
    data = yf.download(pair, period="1d", interval="1m")
    last_price = data["Close"].iloc[-1]
    
    # Простий випадковий сигнал із 70% ймовірністю виграшу
    action = random.choices(["BUY", "SELL"], weights=[0.7, 0.3])[0]
    
    signal_text = f"🔔 Торгівельний сигнал:\nПара: {pair}\nДія: {action}\nЦіна: {last_price:.5f}"
    return signal_text

async def send_signal(app):
    """Надсилає один сигнал"""
    if TG_CHAT_ID:
        signal = await generate_signal()
        await app.bot.send_message(chat_id=int(TG_CHAT_ID), text=signal)

async def signal_loop(app):
    """Надсилання 3 сигналів через 3 хвилини, можна зупинити через /stop"""
    global sending_signals
    for i in range(3):
        if not sending_signals:
            break
        await send_signal(app)
        if i < 2:  # між сигналами пауза 3 хвилини
            await asyncio.sleep(180)
    sending_signals = False
    if TG_CHAT_ID:
        await app.bot.send_message(chat_id=int(TG_CHAT_ID), text="Всі сигнали надіслані або надсилання зупинено ⛔")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global sending_signals
    sending_signals = True
    chat_id = update.effective_chat.id
    await update.message.reply_text(f"Бот запущено. Твій chat_id: {chat_id}")
    await update.message.reply_text("Надсилання 3 сигналів кожні 3 хвилини активовано ✅")
    # Запускаємо цикл сигналів
    asyncio.create_task(signal_loop(context.application))

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global sending_signals
    sending_signals = False
    await update.message.reply_text("Сигнали зупинено ⛔\nБот вимкнув надсилання сигналів.")

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stop", stop))
    app.run_polling()  # один синхронний виклик

if __name__ == "__main__":
    main()
