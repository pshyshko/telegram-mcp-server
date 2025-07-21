from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from smolagents import LiteLLMModel, CodeAgent, ToolCollection

TELEGRAM_BOT_TOKEN = "7824647017:AAGCdEoQ8EVpWhxSEqXgGxeXEOnxwnm2QnE"
model = LiteLLMModel(
  model_id='ollama_chat/qwen3:14b'
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я твой Telegram-бот.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Напиши мне что-нибудь, и я повторю это!")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    with ToolCollection.from_mcp({"url": "http://127.0.0.1:8050/mcp", "transport": "streamable-http"}, trust_remote_code=True) as tool_collection:
      agent = CodeAgent(tools=[*tool_collection.tools], add_base_tools=True, model=model, additional_authorized_imports=["json"])
      response = agent.run(user_message)

    await update.message.reply_text(f"Ответ ИИ Агента: {response}")

if __name__ == '__main__':

    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    app.run_polling()
