import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Отримуємо токен і chat_id з Environment Variables
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TG_CHAT_ID = os.environ.get("TG_CHAT_ID")  # числовий chat_id

# Приклад функції для надсилання сигналу
async def send_signal(app):
    if TG_CHAT_ID:
        await app.bot.send_message(chat_id=int(TG_CHAT_ID), text="Сигнал для торгівлі активовано!")

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Бот готовий. Надсилаю сигнал...")
    # Викликаємо функцію сигналу
    await send_signal(context.application)

# Основна функція
async def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # Додаємо обробник команди /start
    app.add_handler(CommandHandler("start", start))

    # Запускаємо бота
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
