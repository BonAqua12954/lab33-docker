# Лабораторная №33 — Контейнеризация и оркестрация

Учебный проект: упаковка HTTP-сервиса в Docker-контейнер, запуск
многоконтейнерного стека через Docker Compose и развёртывание
в Docker Swarm с репликами и rolling update.

## Что это

HTTP-сервис на Flask, использующий **Redis** как счётчик и **PostgreSQL**
как хранилище истории посещений. Демонстрирует:

- Multi-stage сборку Docker-образа (уменьшение размера).
- Конфигурацию через переменные окружения (без хардкода).
- Связку приложения с двумя хранилищами через именованную сеть.
- Сохранение данных Redis и Postgres через именованные volume.
- Оркестрацию в Docker Swarm: 3 реплики приложения, rolling update.

## Эндпоинты

| Метод | Путь       | Описание                                          |
|-------|------------|---------------------------------------------------|
| GET   | `/`        | HTML-страница «Hello, Docker!»                    |
| GET   | `/health`  | JSON: статус сервиса + подключения к Redis/Postgres |
| GET   | `/count`   | HTML-страница со счётчиком (инкремент в Redis)    |
| GET   | `/history` | HTML-таблица последних 20 посещений из PostgreSQL |

## Стек

- Python 3.11, Flask 3.0.3
- Redis 5.0.7 (клиент), Redis 7 (сервер)
- psycopg2-binary 2.9.9 (клиент), PostgreSQL 16 (сервер)
- Docker, Docker Compose, Docker Swarm

## Переменные окружения

| Переменная          | По умолчанию | Назначение                       |
|---------------------|--------------|----------------------------------|
| `PORT`              | `5000`       | Порт Flask                        |
| `REDIS_HOST`        | `redis`      | Хост Redis в сети Docker          |
| `REDIS_PORT`        | `6379`       | Порт Redis                        |
| `POSTGRES_HOST`     | `postgres`   | Хост PostgreSQL                   |
| `POSTGRES_PORT`     | `5432`       | Порт PostgreSQL                   |
| `POSTGRES_DB`       | `lab33`      | Имя базы данных                   |
| `POSTGRES_USER`     | `lab`        | Пользователь БД                   |
| `POSTGRES_PASSWORD` | `labpass`    | Пароль пользователя БД            |

## Запуск через Docker Compose

```bash
docker compose up
