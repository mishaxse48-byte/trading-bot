import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TG_CHAT_ID = os.environ.get("TG_CHAT_ID")

sending_signals = False

async def signal_loop(app):
    """Фоновий цикл надсилання сигналів кожні 10 хвилин"""
    while sending_signals:
        try:
            await app.bot.send_message(
                chat_id=int(TG_CHAT_ID),
                text="🔔 Сигнал для торгівлі активовано!"
            )
        except Exception as e:
            print(f"Помилка надсилання сигналу: {e}")
        await asyncio.sleep(600)  # 10 хв

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global sending_signals
    sending_signals = True
    chat_id = update.effective_chat.id
    await update.message.reply_text(f"Бот запущено. Твій chat_id: {chat_id}")
    await update.message.reply_text("Надсилання сигналів активовано ✅")
    # Запускаємо фоновий цикл
    asyncio.create_task(signal_loop(context.application))

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global sending_signals
    sending_signals = False
    await update.message.reply_text("Сигнали зупинено ⛔")

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stop", stop))
    app.run_polling()  # синхронний виклик

if __name__ == "__main__":
    main()
