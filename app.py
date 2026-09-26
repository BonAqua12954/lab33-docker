import os
import time
from flask import Flask
import redis

app = Flask(__name__)

# Порт читается из переменной окружения PORT, по умолчанию 5000
PORT = int(os.environ.get("PORT", 5000))

# Адрес Redis тоже из переменных окружения — не хардкодим
REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
REDIS_PORT = int(os.environ.get("REDIS_PORT", 6379))

# Подключаемся к Redis. decode_responses=True — чтобы получать строки, а не байты
r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)


@app.route("/")
def index():
    return "Hello, Docker! Version 1.0.1 (Swarm rolling update)"


@app.route("/health")
def health():
    # Проверяем, что Redis доступен — это и есть «живость» сервиса
    try:
        r.ping()
        return {"status": "ok", "redis": "connected"}, 200
    except Exception as e:
        return {"status": "error", "redis": str(e)}, 500


@app.route("/count")
def count():
    # INCR атомарно увеличивает счётчик в Redis и возвращает новое значение
    value = r.incr("visits")
    return {"count": value}


if __name__ == "__main__":
    # host="0.0.0.0" обязателен, иначе контейнер не будет доступен снаружи
    app.run(host="0.0.0.0", port=PORT)