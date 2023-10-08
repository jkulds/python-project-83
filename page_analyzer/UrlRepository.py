from page_analyzer.models.UrlCkeckDto import UrlCheckDto
from page_analyzer.models.UrlDto import UrlDto
from page_analyzer.db_utils import get_connection


class UrlRepository:
    def get_all(self) -> list[UrlDto]:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """select distinct on (urls.id)
                            urls.id,
                            urls.name,
                            url_checks.created_at,
                            url_checks.status_code
                       from urls left join url_checks
                            ON urls.id = url_checks.url_id
                       order by urls.id desc, url_checks.id desc;""")
                records_dict_list = self._convert_to_dict(cursor.description,
                                                          cursor.fetchall())

                return [UrlDto(**record) for record in records_dict_list]

    def add(self, url: UrlDto) -> UrlDto:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "insert into urls (name, created_at) "
                    "values (%s, %s) RETURNING id;",
                    (url.name, url.created_at))
                url.id = cursor.fetchone()[0]

                return url

    def get_by_id(self, id: int) -> UrlDto:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(f"select * from urls where id = {id};")
                record = cursor.fetchone()
                record_dict = \
                    self._convert_to_dict(cursor.description, record)[0]

                return UrlDto(**record_dict)

    def get_by_name(self, name: str) -> UrlDto | None:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(f"select * from urls where name like '{name}';")
                record = cursor.fetchone()
                if record:
                    record_dict = \
                        self._convert_to_dict(cursor.description, record)[0]

                    return UrlDto(**record_dict)
                else:
                    return None

    def add_check(self, url_check: UrlCheckDto) -> UrlCheckDto:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "insert into url_checks "
                    "(url_id, h1, title, description, status_code, created_at)"
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
                cursor.execute(
                    "select * from url_checks "
                    f"where url_id = {url_id} order by id desc")
                records_dict_list = self._convert_to_dict(cursor.description,
                                                          cursor.fetchall())

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
