def create_default_table(connection, path):
    with open(path) as sql_file:
        with connection.cursor() as cursor:
            sql = sql_file.read()
            cursor.execute(sql)