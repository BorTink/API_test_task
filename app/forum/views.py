import json
from aiohttp import web
from loguru import logger
from db_views import db_get_list, db_new_user, db_select_user, db_edit_user, db_deactivate_user

# Функции для взаимодействия с БД, только направленные на обработку реквестов с сервера
# в зависимости от запроса и конкретного Endpont'а

async def new_user(request):
    try:
        db_pool = request.app['pool']
        first_name = request.query['first_name']
        last_name = request.query['last_name']
        gender = request.query['gender']
        logger.debug('Creating a new user:', first_name, last_name, gender)
        await db_new_user(db_pool, first_name, last_name, gender)
        response_obj = {'status': 'success', 'message': 'user successfully created'}
        logger.info(response_obj['message'])
        return web.Response(text=json.dumps(response_obj), status=200)
    except Exception as e:
        response_obj = {'status': 'failed', 'message': str(e)}
        logger.error(response_obj['message'])
        return web.Response(text=json.dumps(response_obj), status=500)


async def select_user(request):
    try:
        db_pool = request.app['pool']
        inserted_id = int(request.query['id'])
        logger.debug('Selecting a user with id =', inserted_id)
        result = await db_select_user(db_pool, inserted_id)
        result = str(result[0])
        logger.info(result)
        return web.Response(body=result)
    except Exception as e:   #Выведем также ошибку, если она произойдет
        response_obj = {'status': 'failed', 'message': str(e)}
        logger.error(response_obj['message'])
        return web.Response(text=json.dumps(response_obj), status=500)


async def edit_user(request):
    try:
        db_pool = request.app['pool']
        inserted_id = int(request.query['id'])
        first_name = request.query['first_name']
        last_name = request.query['last_name']
        gender = request.query['gender']
        logger.debug('Editing a user with id =', inserted_id)
        result = await db_edit_user(db_pool, inserted_id, first_name, last_name, gender)
        result = str(result[0])
        logger.info(result)
        return web.Response(body=result)
    except Exception as e:
        response_obj = {'status': 'failed', 'message': str(e)}
        logger.error(response_obj['message'])
        return web.Response(text=json.dumps(response_obj), status=500)


async def get_list(request):
    try:
        db_pool = request.app['pool']
        logger.debug('Getting full list')
        result = await db_get_list(db_pool)
        result = str(result)
        logger.info(result)
        return web.Response(body=result)
    except Exception as e:
        response_obj = {'status': 'failed', 'message': str(e)}
        logger.error(response_obj['message'])
        return web.Response(text=json.dumps(response_obj), status=500)


async def deactivate_user(request):
    try:
        db_pool = request.app['pool']
        inserted_id = int(request.query['id'])
        logger.debug('Deleted a user with id =', inserted_id)
        await db_deactivate_user(db_pool, inserted_id)
        response_obj = {'status': 'success', 'message': 'user successfully deleted'}
        # Пишу "deleted", а не "deactivated", потому что по ТЗ метод называется "удаление пользователя"
        logger.info(response_obj['message'])
        return web.Response(text=json.dumps(response_obj), status=200)
    except Exception as e:
        response_obj = {'status': 'failed', 'message': str(e)}
        logger.error(response_obj['message'])
        return web.Response(text=json.dumps(response_obj), status=500)