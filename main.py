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


# SQL код, который будет в дальнейшем использоваться в соответственных им функциях

db_new_user_sql = """INSERT INTO users (first_name, last_name, gender, active) VALUES($1, $2, $3, TRUE)"""

db_select_user_sql = """SELECT * FROM users WHERE id=$1;"""


# Сами функции для взаимодействия с БД (обозначены фразой "db_")

async def db_new_user(db_pool, first_name, last_name, gender):
    await db_pool.fetch(db_new_user_sql, first_name, last_name, gender)


async def db_select_user(db_pool, inserted_id):
    result = await db_pool.fetch(db_select_user_sql, inserted_id)
    return result


async def new_user(request):
    try:
        db_pool = request.app['pool']
        first_name = request.query['first_name']
        last_name = request.query['last_name']
        gender = request.query['gender']
        print('Creating a new user:', first_name, last_name, gender)

        await db_new_user(db_pool, first_name, last_name, gender)

        response_obj = {'status': 'success', 'message': 'user successfully created'}
        print(response_obj['message'])
        return web.Response(text=json.dumps(response_obj), status=200)
    except Exception as e:
        response_obj = {'status': 'failed', 'message': str(e)}
        print(response_obj['message'])
        return web.Response(text=json.dumps(response_obj), status=500)


async def select_user(request):
    try:
        db_pool = request.app['pool']
        inserted_id = int(request.query['id'])
        print('Selecting a user with id =', inserted_id)
        result = await db_select_user(db_pool, inserted_id)
        result = str(result[0])
        print(result)
        return web.Response(body=result)
    except Exception as e:   #Выведем также ошибку, если она произойдет
        response_obj = {'status': 'failed', 'message': str(e)}
        print(response_obj['message'])
        return web.Response(text=json.dumps(response_obj), status=500)
# Функция инициализации веб-приложения со всеми Endpoints


async def init_app():
    app = web.Application()
    web.Response(text='Hello', status=200)
    app['pool'] = await asyncpg.create_pool(user='postgres')  # Создаю БД у пользователя postgres (по умолчанию)
    app.router.add_post('/new', new_user)
    app.router.add_get('/select', select_user)
    try:
        await app['pool'].fetch(create_table_sql)
        print('Created "Users" table')
    except:
        pass
    return app


# Инициализация веб-приложения

app = init_app()
web.run_app(app)