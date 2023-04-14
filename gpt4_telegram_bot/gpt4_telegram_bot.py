import logging
import os

import openai
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    MessageHandler,
    filters,
    CommandHandler,
)

from openai_constants import ROLE_FILED_NAME, CONTENT_FIELD_NAME, OPENAI_TOKEN_NAME, GPT_4_MODEL, \
    ROLE_USER, ROLE_ASSISTANT
from telegram_constants import TELEGRAM_TOKEN_NAME

RESTART_COMMAND = "restart"

logging.basicConfig(level=logging.DEBUG)

chat_messages = []


async def process_text_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.debug("Processing text message")
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="Generating GPT-4 response"
    )
    append_chat(update.message.text, ROLE_USER)

    gpt4_response_text = generate_gpt_response()

    append_chat(gpt4_response_text, ROLE_ASSISTANT)

    await context.bot.send_message(chat_id=update.effective_chat.id, text=gpt4_response_text)


def generate_gpt_response():
    completion = openai.ChatCompletion.create(model=GPT_4_MODEL, messages=chat_messages)
    return completion.choices[0].message[CONTENT_FIELD_NAME]


async def restart_chat(update, context):
    clear_history()
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="Restarting conversation"
    )
    return chat_messages


def append_chat(content, role):
    chat_messages.append({ROLE_FILED_NAME: role, CONTENT_FIELD_NAME: content})
    return chat_messages


def clear_history():
    logging.debug("resetting chat")
    chat_messages.clear()
    return chat_messages


if __name__ == "__main__":
    logging.debug("Starting application")
    telegram_token = os.environ[TELEGRAM_TOKEN_NAME]
    openai.api_key = os.environ[OPENAI_TOKEN_NAME]

    bot_application = ApplicationBuilder().token(telegram_token).build()

    text_handler = MessageHandler(
        filters.TEXT & (~filters.COMMAND), process_text_message
    )

    bot_application.add_handler(text_handler)

    bot_application.add_handler(CommandHandler(RESTART_COMMAND, restart_chat))

    bot_application.run_polling()
    logging.debug("Application successfully started")
