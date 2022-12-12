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

#У редактирования 3 SQL кода, чтобы можно было вводить не все значения в запросе

db_edit_user_sql_first_name = """UPDATE users SET first_name=$2 WHERE id=$1"""

db_edit_user_sql_last_name = """UPDATE users SET last_name=$2 WHERE id=$1"""

db_edit_user_sql_gender = """UPDATE users SET gender=$2 WHERE id=$1"""

db_get_list_sql = """SELECT * FROM users ORDER BY id"""

db_deactivate_user_sql = """UPDATE users SET active=FALSE WHERE id=$1"""


# Сами функции для взаимодействия с БД (обозначены фразой "db_")

async def db_new_user(db_pool, first_name, last_name, gender):
    await db_pool.fetch(db_new_user_sql, first_name, last_name, gender)


async def db_select_user(db_pool, inserted_id):
    result = await db_pool.fetch(db_select_user_sql, inserted_id)
    return result


async def db_edit_user(db_pool, inserted_id, first_name='', last_name='', gender=''):
    if first_name != '':
        await db_pool.fetch(db_edit_user_sql_first_name, inserted_id, first_name)
    if last_name != '':
        await db_pool.fetch(db_edit_user_sql_last_name, inserted_id, last_name)
    if gender != '':
        await db_pool.fetch(db_edit_user_sql_gender, inserted_id, gender)
    result = await db_pool.fetch(db_select_user_sql, inserted_id)
    return result


async def db_get_list(db_pool):
    result = await db_pool.fetch(db_get_list_sql)
    return result


async def db_deactivate_user(db_pool, inserted_id):
    await db_pool.fetch(db_deactivate_user_sql, inserted_id)
