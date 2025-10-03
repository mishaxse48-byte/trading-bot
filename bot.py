import logging
import os
import time
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Токен бота, його потрібно додати у Render як TELEGRAM_TOKEN
TOKEN = os.environ.get("TELEGRAM_TOKEN")

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привіт 👋 Я твій навчальний трейдинг-бот!")

# Тестова функція для надсилання сигналів
async def signal_sender(application):
    while True:
        try:
            chat_id = os.environ.get("TG_CHAT_ID")
            if chat_id:
                await application.bot.send_message(chat_id=chat_id, text="🔔 Тестовий сигнал: Купити EUR/USD")
            time.sleep(600)  # чекати 10 хвилин
        except Exception as e:
            print(f"Помилка: {e}")
            time.sleep(10)

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    # запуск у фоновому режимі
    app.post_init(signal_sender(app))

    print("✅ Бот запущений...")
    app.run_polling()

if __name__ == "__main__":
    main()
