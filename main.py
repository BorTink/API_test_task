from aiohttp import web
import asyncpg
from loguru import logger
from app.auth import config
from app.forum.db_views import create_table_sql


def setup_routes(application):
    from app.forum.routes import setup_routes
    setup_routes(application)  # настраиваем url-пути приложения forum


# Функция инициализации веб-приложения со всеми Endpoints

async def init_app():
    app = web.Application()
    web.Response(text='Hello', status=200)
    app['pool'] = await asyncpg.create_pool(user=config.user, host=config.host, port=config.port, password=config.password,
                                            database=config.database)  # Создем БД
    setup_routes(app)  # Устанавливаем routes через routes.py
    try:
        await app['pool'].fetch(create_table_sql)
        logger.debug('Created "Users" table')
    except:
        pass
    return app


# Инициализация веб-приложения

app = init_app()
web.run_app(app)
