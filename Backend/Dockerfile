ARG BASE_IMAGE=python:3.10.0
FROM $BASE_IMAGE

# Системные зависимости
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

# Копируем проект и зависимости
COPY deps /deps
COPY . .

# Устанавливаем зависимости без интернета
RUN python -m pip install --upgrade pip && \
    python -m pip install --no-index --find-links=/deps -r requirements.txt

# Запуск приложения
CMD ["python", "main.py"]
