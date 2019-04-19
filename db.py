import psycopg2
import config
import psycopg2.extras
import json


class Database:
    def __init__(self):
        with psycopg2.connect(dbname=config.DB_NAME, user=config.USER_NAME, password=config.USER_PASSWORD,
                              host=config.DB_HOST) as connection:
            self.connection = connection
            self.cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

    def update_query(self, query):
        try:
            self.cursor.execute(query)
            self.connection.commit()
        except Exception as e:
            return json.dumps({'code': 1, 'message': 'Database error' + str(e), 'rows': []})
        return json.dumps({'code': 0, 'message': 'Database succesfully updated', 'rows': []})

    def select_query(self, query):
        try:
            self.cursor.execute(query)
        except Exception as e:
            return json.dumps({'code': 1, 'message': 'Database error' + str(e), 'rows': []})
        if self.cursor.rowcount == 0:
            response_rows = []
        else:
            response_rows = self.cursor.fetchall()
        return json.dumps({'code': 0, 'message': 'Rows successfully selected', 'rows': response_rows})
