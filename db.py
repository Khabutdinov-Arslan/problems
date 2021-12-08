import psycopg2
import config
import psycopg2.extras
import json
import sys


class Database:
    def __init__(self):
        with psycopg2.connect(dbname=config.DB_NAME, user=config.USER_NAME, password=config.USER_PASSWORD,
                              host=config.DB_HOST) as connection:
            self.connection = connection
            self.cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

    def update_query(self, query, params):
        try:
            self.cursor.execute(query, params)
            self.connection.commit()
        except Exception as e:
            sys.stderr.write(str(e))
            return json.dumps({'code': 1, 'message': 'Database error' + str(e), 'rows': []})
        resp = json.dumps({'code': 0, 'message': 'Database succesfully updated', 'rows': []})
        return resp

    def select_query(self, query, params):
        try:
            self.cursor.execute(query, params)
        except Exception as e:
            sys.stderr.write(str(e))
            return json.dumps({'code': 1, 'message': 'Database error' + str(e), 'rows': []})
        if self.cursor.rowcount == 0:
            response_rows = []
        else:
            response_rows = self.cursor.fetchall()
        resp = json.dumps({'code': 0, 'message': 'Rows successfully selected', 'rows': response_rows})
        return resp
