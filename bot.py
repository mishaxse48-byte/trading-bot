import os
import asyncio
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import requests  # для роботи з Pocket Broker API (якщо буде)

# ----------------------------
# Налаштування бота
# ----------------------------
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TG_CHAT_ID = os.environ.get("TG_CHAT_ID")  # числовий ID

logging.basicConfig(level=logging.INFO)

# ----------------------------
# Контроль надсилання сигналів
# ----------------------------
sending_signals = False

# ----------------------------
# Функція видалення webhook
# ----------------------------
def delete_webhook():
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/deleteWebhook"
    try:
        r = requests.post(url)
        if r.status_code == 200:
            logging.info("Webhook видалено успішно")
        else:
            logging.warning(f"Не вдалося видалити webhook: {r.text}")
    except Exception as e:
        logging.error(f"Помилка при видаленні webhook: {e}")

# ----------------------------
# Функція для надсилання сигналу
# ----------------------------
async def send_signal(app, pair="EUR/USD", action="BUY", confidence=70):
    """
    Надіслати сигнал в Telegram.
    pair: валютна пара
    action: BUY або SELL
    confidence: % ймовірності успішної угоди
    """
    if TG_CHAT_ID and sending_signals:
        text = f"🔔 Сигнал для торгівлі!\nПара: {pair}\nДія: {action}\nЙмовірність вигоди: {confidence}%"
        await app.bot.send_message(chat_id=int(TG_CHAT_ID), text=text)

# ----------------------------
# Функція циклу сигналів (3 сигнали через 3 хв)
# ----------------------------
async def signal_loop(app, pair="EUR/USD", action="BUY"):
    global sending_signals
    for i in range(3):
        if not sending_signals:
            break
        # Тут можна вставити аналіз реальних даних з Pocket Broker API
        confidence = 70  # наприклад, робимо фіксовану ймовірність
        await send_signal(app, pair, action, confidence)
        if i < 2:
            await asyncio.sleep(180)  # 3 хвилини
    sending_signals = False
    await app.bot.send_message(chat_id=int(TG_CHAT_ID), text="Всі сигнали надіслані або надсилання зупинено ⛔")

# ----------------------------
# Команда /start
# ----------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global sending_signals
    sending_signals = True
    chat_id = update.effective_chat.id
    await update.message.reply_text(f"Бот запущено. Твій chat_id: {chat_id}")
    await update.message.reply_text("Надсилання сигналів активовано ✅")
    # Запускаємо фоновий цикл сигналів
    asyncio.create_task(signal_loop(context.application))

# ----------------------------
# Команда /stop
# ----------------------------
async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global sending_signals
    sending_signals = False
    await update.message.reply_text("Бот зупинено. Надсилання сигналів вимкнено ⛔")

# ----------------------------
# Основна функція
# ----------------------------
def main():
    # Спочатку видаляємо webhook, щоб уникнути конфліктів
    delete_webhook()

    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stop", stop))

    # Запускаємо polling (синхронний виклик)
    app.run_polling()
    logging.info("Bot started successfully")

# ----------------------------
if __name__ == "__main__":
    main()
