from page_analyzer.UrlDto import UrlDto


class UrlRepository:
    def __init__(self, connection, db_name):
        self.connection = connection
        self.db_name = db_name

    def get_all(self):
        cursor = self.connection.cursor()

        cursor.execute(f"select * from {self.db_name} order by id desc")
        records = cursor.fetchall()

        records_dict = self.convert_to_dict(cursor.description, records)

        result = []
        for record in records_dict:
            url = UrlDto(**record)
            result.append(url)

        return result

    def add(self, url: UrlDto) -> UrlDto:
        cursor = self.connection.cursor()

        cursor.execute(f"insert into {self.db_name} (name, created_at) values (%s, %s) RETURNING id",
                       (url.name, url.created_at))
        url.id = cursor.fetchone()[0]

        return url

    def get_by_id(self, id):
        cursor = self.connection.cursor()

        cursor.execute(f"select * from {self.db_name} where id = %s", id)
        record = cursor.fetchone()

        record_dict = self.convert_to_dict(cursor.description, record)[0]

        url = UrlDto(**record_dict)

        return url

    def is_exists(self, name: str) -> bool:
        cursor = self.connection.cursor()

        cursor.execute(f"select * from {self.db_name} where name like '{name}'")
        record = cursor.fetchone()

        return record is not None


    def convert_to_dict(self, columns, results):
        all_results = []
        columns = [col.name for col in columns]
        if type(results) is list:
            for value in results:
                all_results.append(dict(zip(columns, value)))
            return all_results
        elif type(results) is tuple:
            all_results.append(dict(zip(columns, results)))
            return all_results
