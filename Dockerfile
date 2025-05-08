FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

ENV LANG=en_US.UTF-8 \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONWARNINGS="ignore:Unverified HTTPS request" \
    PATH=/usr/src/venv/bin:$PATH \
    VIRTUAL_ENV=/usr/src/venv \
    POETRY_VERSION=2.1.2


COPY pyproject.toml poetry.lock ./


RUN python -m venv /usr/src/venv && \
    pip install -U pip && \
    pip install "poetry==$POETRY_VERSION" && \
    poetry install --no-root --no-interaction --without=dev

COPY . .

COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

CMD ["/app/entrypoint.sh"]

# CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
