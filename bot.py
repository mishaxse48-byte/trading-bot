import asyncio
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

sending_signals = False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global sending_signals
    chat_id = update.effective_chat.id

    if sending_signals:
        await update.message.reply_text("Сигнали вже надсилаються ⏳")
        return

    sending_signals = True
    await update.message.reply_text(f"Бот запущено. Твій chat_id: {chat_id}")
    await update.message.reply_text("Надсилання 3 сигналів кожні 3 хвилини ✅")

    for i in range(3):
        if not sending_signals:
            break
        await context.bot.send_message(chat_id=chat_id, text=f"🔔 Сигнал {i+1} для торгівлі активовано!")
        if i < 2:
            await asyncio.sleep(180)  # 3 хвилини

    sending_signals = False
    await update.message.reply_text("Всі 3 сигнали надіслані або надсилання зупинено ⛔")

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global sending_signals
    sending_signals = False
    await update.message.reply_text("Сигнали зупинено ⛔")

def main():
    TOKEN = os.environ.get("TELEGRAM_TOKEN")
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stop", stop))
    app.run_polling()  # синхронний запуск

if __name__ == "__main__":
    main()
