import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, Context

# Токен і chat_id з Environment Variables
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TG_CHAT_ID = os.environ.get("TG_CHAT_ID")  # числовий chat_id

# Контроль надсилання сигналів
sending_signals = False

async def send_signal(app, pair="EUR/USD"):
    """Надіслати один сигнал для торгової пари"""
    if TG_CHAT_ID:
        try:
            await app.bot.send_message(
                chat_id=int(TG_CHAT_ID),
                text=f"🔔 Сигнал для торгівлі: {pair} активовано!"
            )
        except Exception as e:
            print(f"Помилка надсилання сигналу: {e}")

async def signal_sequence(app, pair="EUR/USD"):
    """Надсилання 3 сигналів з інтервалом 3 хв"""
    global sending_signals
    for i in range(3):
        if not sending_signals:
            break
        await send_signal(app, pair)
        if i < 2:
            await asyncio.sleep(180)  # 3 хвилини
    sending_signals = False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global sending_signals
    sending_signals = True
    chat_id = update.effective_chat.id
    await update.message.reply_text(f"Бот запущено. Твій chat_id: {chat_id}")
    await update.message.reply_text("Надсилання 3 сигналів кожні 3 хвилини ✅")
    asyncio.create_task(signal_sequence(context.application, pair="EUR/USD"))

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global sending_signals
    sending_signals = False
    await update.message.reply_text("Сигнали зупинено ⛔")
    await update.message.reply_text("Бот зупинено. Надсилання сигналів вимкнено ⛔")

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stop", stop))

    # Webhook для Render
    PORT = int(os.environ.get("PORT", 8443))
    WEBHOOK_URL = os.environ.get("WEBHOOK_URL")  # має бути https://yourdomain/path
    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_url=WEBHOOK_URL
    )

if __name__ == "__main__":
    main()
