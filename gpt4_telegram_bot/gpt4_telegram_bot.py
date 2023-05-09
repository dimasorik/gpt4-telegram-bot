import logging
import os

import openai
from pathlib import Path
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    MessageHandler,
    filters,
    CommandHandler,
)

from better_profanity import profanity
from better_profanity.utils import get_complete_path_of_file, read_wordlist

from openai_constants import ROLE_FILED_NAME, CONTENT_FIELD_NAME, OPENAI_TOKEN_NAME, GPT_4_MODEL, \
    ROLE_USER, ROLE_ASSISTANT
from telegram_constants import TELEGRAM_TOKEN_NAME

RESTART_COMMAND = "restart"
HELP_COMMAND = "help"

logging.basicConfig(level=logging.DEBUG)

chat_map = {}  # Should be Redis or some other key-value storage

model = os.environ.get("GPT_MODEL", GPT_4_MODEL)


async def reset_history_if_required(chat_id, context):
    chat_messages = chat_map.get(chat_id, [])
    if len(chat_messages) >= 10:
        await context.bot.send_message(
            chat_id=chat_id, text="Limit of history reached, resetting conversation"
        )
        chat_map[chat_id] = []


async def process_text_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.debug("Processing text message")
    chat_id = update.effective_chat.id

    await reset_history_if_required(chat_id, context)

    await context.bot.send_message(
        chat_id=chat_id, text="Generating GPT-4 response"
    )

    censored_user_message = profanity.censor(update.message.text)

    append_chat(chat_id, censored_user_message, ROLE_USER)

    chat_messages = chat_map.get(chat_id)
    gpt4_response_text = generate_gpt_response(chat_messages)

    append_chat(chat_id, gpt4_response_text, ROLE_ASSISTANT)

    await context.bot.send_message(chat_id=chat_id, text=gpt4_response_text)


def generate_gpt_response(chat_messages):
    completion = openai.ChatCompletion.create(model=model, messages=chat_messages)
    return completion.choices[0].message[CONTENT_FIELD_NAME]


async def restart_chat(update, context):
    chat_id = update.effective_chat.id
    clear_history(chat_id)
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="Restarting conversation"
    )
    return []


async def help_message(update, context):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="""
        Currently available bot commands:
            1. /restart - reset chat history with GPT
            2. /help - display help
        """
    )


def append_chat(chat_id, content, role):
    chat_messages = chat_map.get(chat_id, [])
    chat_messages.append({ROLE_FILED_NAME: role, CONTENT_FIELD_NAME: content})
    chat_map[chat_id] = chat_messages
    return chat_messages


def clear_history(chat_id):
    logging.debug("resetting chat")
    chat_messages = chat_map.get(chat_id, [])
    chat_messages.clear()
    chat_map[chat_id] = chat_messages
    return chat_messages


if __name__ == "__main__":
    logging.debug("Starting application")
    telegram_token = os.environ[TELEGRAM_TOKEN_NAME]
    openai.api_key = os.environ[OPENAI_TOKEN_NAME]

    profanity.load_censor_words(custom_words=read_wordlist(os.path.dirname(os.path.realpath(__file__)) + "/resources/profanity_wordlist.txt"))

    bot_application = ApplicationBuilder().token(telegram_token).build()

    text_handler = MessageHandler(
        filters.TEXT & (~filters.COMMAND), process_text_message
    )

    bot_application.add_handler(text_handler)

    bot_application.add_handler(CommandHandler(RESTART_COMMAND, restart_chat))

    bot_application.add_handler(CommandHandler(HELP_COMMAND, help_message))

    bot_application.run_polling()
    logging.debug("Application successfully started")
