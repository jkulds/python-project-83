from page_analyzer.UrlDto import UrlDto
from page_analyzer.db import get_connection


class UrlRepository:
    def get_all(self):
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("select * from urls order by id desc;")
                records = cursor.fetchall()

                records_dict = self._convert_to_dict(cursor.description, records)

                return [UrlDto(**record) for record in records_dict]

    def add(self, url: UrlDto) -> UrlDto:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("insert into urls (name, created_at) values (%s, %s) RETURNING id;",
                               (url.name, url.created_at))
                url.id = cursor.fetchone()[0]

                return url

    def get_by_id(self, id):
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("select * from urls where id = %s;", id)
                record_dict = self._convert_to_dict(cursor.description, cursor.fetchone())[0]

                return UrlDto(**record_dict)

    def is_exists(self, name: str) -> bool:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(f"select * from urls where name like '{name}';")
                record = cursor.fetchone()

                return record is not None

    def _convert_to_dict(self, columns, results):
        all_results = []
        columns = [col.name for col in columns]
        if type(results) is list:
            for value in results:
                all_results.append(dict(zip(columns, value)))
            return all_results
        elif type(results) is tuple:
            all_results.append(dict(zip(columns, results)))
            return all_results
