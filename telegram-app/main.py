from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from smolagents import LiteLLMModel, CodeAgent, ToolCollection
import os

model = LiteLLMModel(model_id="ollama_chat/qwen3:14b")
extra_system_prompt = "\nYou are an agent that performs tasks only with the tools given to you. In case there is something outside of the list, you answer that you cannot do it\n"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я твой Telegram-бот.")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Напиши мне что-нибудь, и я повторю это!")


async def message_reponses(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    with ToolCollection.from_mcp(
        {"url": os.getenv("MCP_URL"), "transport": "streamable-http"},
        trust_remote_code=True,
    ) as tool_collection:
        agent = CodeAgent(
            tools=[*tool_collection.tools],
            add_base_tools=True,
            model=model,
            additional_authorized_imports=["json"],
        )
        response = agent.run(extra_system_prompt + user_message)

    await update.message.reply_text(f"Ответ ИИ Агента: {response}")


if __name__ == "__main__":
    app = ApplicationBuilder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_reponses))

    app.run_polling()
