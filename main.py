from aiohttp import web
import json
import asyncpg


# SQL код, необходимый для попытки создания таблицы пользователей в БД при инициализации веб-приложения

create_table_sql = """CREATE TABLE users (
    id BIGSERIAL NOT NULL PRIMARY KEY,
	first_name VARCHAR(50) NOT NULL ,
	last_name VARCHAR(50) NOT NULL,
	gender VARCHAR(50) NOT NULL,
	active BOOLEAN NOT NULL
);"""


# Функция инициализации веб-приложения со всеми Endpoints

async def init_app():
    app = web.Application()
    web.Response(text='Hello', status=200)
    app['pool'] = await asyncpg.create_pool(user='postgres')  # Создаю БД у пользователя postgres (по умолчанию)
    try:
        await app['pool'].fetch(create_table_sql)
        print('Created "Users" table')
    except:
        pass
    return app


# Инициализация веб-приложения

app = init_app()
web.run_app(app)