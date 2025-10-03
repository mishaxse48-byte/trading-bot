import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Токен бота та chat_id з Environment Variables
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TG_CHAT_ID = os.environ.get("TG_CHAT_ID")  # числовий chat_id

# Функція для надсилання сигналу
async def send_signal(app):
    if TG_CHAT_ID:
        await app.bot.send_message(chat_id=int(TG_CHAT_ID), text="🔔 Сигнал для торгівлі активовано!")

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    # Показуємо chat_id для перевірки
    await update.message.reply_text(f"Твій chat_id: {chat_id}")
    # Надсилаємо тестовий сигнал
    await send_signal(context.application)

# Основна функція
async def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    # Працюємо через run_polling (він автоматично initialize/start/polling)
    await app.run_polling()
    print("Bot started successfully")

if __name__ == "__main__":
    asyncio.run(main())
