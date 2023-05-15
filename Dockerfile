FROM python:3.11-slim

# Configure Poetry
ENV POETRY_VERSION=1.4.0
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VENV=/opt/poetry-venv
ENV POETRY_CACHE_DIR=/opt/.cache

# Install poetry separated from system interpreter
RUN python3 -m venv $POETRY_VENV \
    && $POETRY_VENV/bin/pip install -U pip setuptools \
    && $POETRY_VENV/bin/pip install poetry==${POETRY_VERSION}

# Add `poetry` to PATH
ENV PATH="${PATH}:${POETRY_VENV}/bin"

WORKDIR /app

COPY poetry.lock pyproject.toml README.md ./
# [OPTIONAL] Validate the project is properly configured
RUN poetry check

RUN pwd

RUN ls -lah

COPY ./gpt4_telegram_bot/ ./gpt4_telegram_bot/

RUN poetry install --no-interaction --no-cache --without dev

# Run your app
CMD [ "poetry", "run", "python", "gpt4_telegram_bot/gpt4_telegram_bot.py" ]
