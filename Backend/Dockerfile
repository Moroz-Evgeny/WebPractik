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

# Копируем проект и зависимости(deps или requirements)
# COPY deps /deps
COPY . .

WORKDIR .
# Установка Python зависимостей только из локальной папки!
# RUN pip install --no-index --find-links=/deps /deps/*

#Установка зависимостей из интернета
RUN python3 -m pip install --user --upgrade pip && \
    python3 -m pip install -r requirements.txt

# Запуск приложения
CMD ["python", "main.py"]
