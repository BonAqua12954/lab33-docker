# ========== Стадия 1: builder ==========
# Здесь мы только устанавливаем зависимости. Компиляторы, кэш pip — всё останется тут.
FROM python:3.11-slim AS builder

WORKDIR /app

COPY requirements.txt .

# --user ставит пакеты в /root/.local — потом просто скопируем эту папку
RUN pip install --no-cache-dir --user -r requirements.txt


# ========== Стадия 2: runtime ==========
# Здесь только то, что нужно для запуска. Никаких компиляторов.
FROM python:3.11-slim

WORKDIR /app

# Забираем установленные пакеты из builder-стадии
COPY --from=builder /root/.local /root/.local

# Код приложения
COPY app.py .

# Чтобы python нашёл пакеты из /root/.local
ENV PATH=/root/.local/bin:$PATH

# Значения по умолчанию. При запуске через compose их можно переопределить.
ENV PORT=5000
ENV REDIS_HOST=redis
ENV REDIS_PORT=6379

EXPOSE 5000

CMD ["python", "app.py"]