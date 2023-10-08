from page_analyzer.models.UrlCkeckDto import UrlCheckDto
from page_analyzer.models.UrlDto import UrlDto
from page_analyzer.db import get_connection


class UrlRepository:
    def get_all(self) -> list[UrlDto]:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "select * from urls u "
                    "   left join "
                    "       (select url_id, title, description, status_code, created_at, h1 "
                    "           from url_checks "
                    "               where id in "
                    "                   (select max(id) as id from url_checks group by url_id)) uc "
                    "       on u.id = uc.url_id "
                    "       order by u.id desc;")
                records_dict_list = self._convert_to_dict(cursor.description, cursor.fetchall())

                return [UrlDto(**record) for record in records_dict_list]

    def add(self, url: UrlDto) -> UrlDto:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("insert into urls (name, created_at) values (%s, %s) RETURNING id;",
                               (url.name, url.created_at))
                url.id = cursor.fetchone()[0]

                return url

    def get_by_id(self, id: int) -> UrlDto:
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

    def add_check(self, url_check: UrlCheckDto) -> UrlCheckDto:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "insert into url_checks (url_id, h1, title, description, status_code, created_at) " +
                    "values (%s, %s, %s, %s, %s, %s) returning id;",
                    (url_check.url_id,
                     url_check.h1,
                     url_check.title,
                     url_check.description,
                     url_check.status_code,
                     url_check.created_at))
                url_check.id = cursor.fetchone()[0]

                return url_check

    def get_checks_by_url_id(self, url_id) -> list[UrlCheckDto]:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("select * from url_checks where url_id = %s order by id desc", url_id)
                records_dict_list = self._convert_to_dict(cursor.description, cursor.fetchall())

                return [UrlCheckDto(**record) for record in records_dict_list]

    @staticmethod
    def _convert_to_dict(columns, results) -> list[dict]:
        all_results = []
        columns = [col.name for col in columns]
        if type(results) is list:
            for value in results:
                all_results.append(dict(zip(columns, value)))
            return all_results
        elif type(results) is tuple:
            all_results.append(dict(zip(columns, results)))
            return all_results
