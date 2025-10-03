import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Токен та chat_id з Environment Variables
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TG_CHAT_ID = os.environ.get("TG_CHAT_ID")  # числовий ID

# Контроль надсилання сигналів
sending_signals = False

async def send_signal(app):
    """Надіслати один сигнал"""
    if TG_CHAT_ID:
        await app.bot.send_message(chat_id=int(TG_CHAT_ID), text="🔔 Сигнал для торгівлі активовано!")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global sending_signals
    chat_id = update.effective_chat.id
    await update.message.reply_text(f"Твій chat_id: {chat_id}")

    if sending_signals:
        await update.message.reply_text("Сигнали вже надсилаються ⏳")
        return

    sending_signals = True
    await update.message.reply_text("Бот запущено. Надсилання 3 сигналів кожні 3 хвилини ✅")

    for i in range(3):
        if not sending_signals:
            break  # зупинка, якщо /stop натиснуто
        await send_signal(context.application)
        if i < 2:
            await asyncio.sleep(180)  # 3 хвилини

    sending_signals = False
    await update.message.reply_text("Всі сигнали надіслані або надсилання зупинено ⛔")

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global sending_signals
    sending_signals = False
    await update.message.reply_text("Бот зупинено. Надсилання сигналів вимкнено ⛔")

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stop", stop))
    app.run_polling()  # лише один виклик

if __name__ == "__main__":
    main()
