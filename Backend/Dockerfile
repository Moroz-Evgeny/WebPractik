ARG BASE_IMAGE=python:3.10.11
FROM $BASE_IMAGE

# Установка DNS Google для стабильного резолва доменов
RUN echo "nameserver 8.8.8.8" > /etc/resolv.conf

# Установка системных зависимостей с использованием другого зеркала
RUN sed -i 's|http://deb.debian.org|http://ftp.de.debian.org|g' /etc/apt/sources.list && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    openssl libssl-dev \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Создание рабочей директории
WORKDIR /app

# Копирование зависимостей и установка
COPY requirements.txt .
RUN python3 -m pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Копирование всего проекта
COPY . .

# Открытие порта
EXPOSE 8000

# Запуск приложения
CMD ["python3", "main.py"]
