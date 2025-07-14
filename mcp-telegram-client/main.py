import os

import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a welcome message in response to the /start command."""
    user = update.effective_user
    await update.message.reply_html(
        f"Привет, {user.mention_html()}! Я простой эхо-бот. Отправь мне любое сообщение, и я его повторю.",
    )

async def echo_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echoes the user's text message."""
    message_text = update.message.text
    await update.message.reply_text(message_text)

def main() -> None:
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

    application = Application.builder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo_message))
    print("Bot is running and ready to work...")
    application.run_polling()

if __name__ == '__main__':
    main()