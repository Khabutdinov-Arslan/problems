import db

db = db.Database()

with open('create_db.sql') as query_file:
    content = query_file.read()
    db.update_query(content)