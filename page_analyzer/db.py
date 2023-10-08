import os

import psycopg2


def get_connection():
    db_url = os.getenv('DATABASE_URL')
    if not db_url:
        raise ValueError('Not found $DATABASE_URL')

    try:
        connection = psycopg2.connect(db_url)
        connection.autocommit = True
        return connection
    except:
        raise RuntimeError('Ошибка подключении к базе данных')


def create_default_table(path):
    with get_connection() as connection:
        with connection.cursor() as cursor:
            with open(path) as sql_file:
                sql = sql_file.read()
                cursor.execute(sql)
