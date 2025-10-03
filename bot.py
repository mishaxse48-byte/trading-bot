import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Токен бота та chat_id з Environment Variables
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TG_CHAT_ID = os.environ.get("TG_CHAT_ID")  # числовий ID

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    # Спочатку показуємо chat_id для перевірки
    await update.message.reply_text(f"Твій chat_id: {chat_id}")
    
    # Якщо TG_CHAT_ID налаштований, надсилаємо сигнал
    if TG_CHAT_ID:
        await context.application.bot.send_message(
            chat_id=int(TG_CHAT_ID),
            text="🔔 Тестовий сигнал: Купити EUR/USD"
        )

# Основна функція
async def main():
    # Створюємо застосунок
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # Додаємо обробник команди /start
    app.add_handler(CommandHandler("start", start))

    # Правильний асинхронний запуск
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    print("Bot started successfully")
    await app.idle()  # чекаємо завершення

if __name__ == "__main__":
    asyncio.run(main())
