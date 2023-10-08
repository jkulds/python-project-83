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


def create_default_table(connection, path):
    with open(path) as sql_file:
        with connection.cursor() as cursor:
            sql = sql_file.read()
            cursor.execute(sql)
