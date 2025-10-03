import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Токен бота та chat_id з Environment Variables
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TG_CHAT_ID = os.environ.get("TG_CHAT_ID")  # числовий chat_id

# Контроль надсилання сигналів
sending_signals = False

# Функція для надсилання сигналу
async def send_signal(app):
    global sending_signals
    if TG_CHAT_ID and sending_signals:
        await app.bot.send_message(chat_id=int(TG_CHAT_ID), text="🔔 Сигнал для торгівлі активовано!")

# /start включає надсилання сигналів
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global sending_signals
    chat_id = update.effective_chat.id
    await update.message.reply_text(f"Твій chat_id: {chat_id}")
    sending_signals = True
    await update.message.reply_text("Бот запущено. Надсилання сигналів активовано.")
    await send_signal(context.application)

# /stop вимикає сигнали
async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global sending_signals
    sending_signals = False
    await update.message.reply_text("Бот зупинено. Сигнали більше не надсилаються.")

# Основна функція
async def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stop", stop))
    await app.run_polling()
    print("Bot started successfully")

if __name__ == "__main__":
    asyncio.run(main())
