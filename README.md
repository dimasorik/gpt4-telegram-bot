# gpt4-telegram-bot
Telegram Bot that is using AI GPT-4 version from the [OpenAI](https://openai.com/) company.

In order to use it - you will 2 things: 
1. Create Telegram Bot within telegram infa. The [BotFather](https://t.me/botfather) from Telegram will help you with that.
2. Get GPT-4 API token from OpenAI. Details [here](https://help.openai.com/en/articles/7102672-how-can-i-access-gpt-4).

## Developer's instructions
This project is using [python-poetry](https://python-poetry.org/) as a PYTHON PACKAGING AND DEPENDENCY MANAGEMENT. 
### Prerequisites
1. Python >= 3.11 version 
2. [Poetry](https://python-poetry.org/) >= 1.4.0 version 
### Running project locally
1. Checkout && cd to the project's folder
2. Install dependencies `poetry install`
3. Export env variables `export TELEGRAM_TOKEN=token && export OPENAI_TOKEN_NAME=token`
4. Run `poetry run python gpt4_telegram_bot/gpt4_telegram_bot.py`
### Building and running docker image
1. Set the tokens inside `docker-compose.yaml`
2. Run docker-compose `docker-compose up`

## Functionality 
The current features of the bot: 
1. Pass the complete text chat to the OpenAI's GPT-4  and forwarding reply to it
2. Reset the chat hystory with `/restart` command

### Bot commands
Currenty supported commands: 
1. `/restart` - reset the chat history for GPT-4
