ARG BASE_IMAGE=python:3.10.0
FROM $BASE_IMAGE

# Системные зависимости и зеркало для APT
RUN sed -i 's|http://deb.debian.org|http://mirror.yandex.ru|g' /etc/apt/sources.list && \
    apt-get -y update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        postgresql-client \
        openssl \
        libssl-dev \
        curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Копирование проекта
COPY . .
WORKDIR .

# Установка Python-зависимостей через зеркало
RUN python3 -m pip install --upgrade pip && \
    python3 -m pip install --no-cache-dir -r requirements.txt

# Запуск приложения
CMD ["python", "main.py"]