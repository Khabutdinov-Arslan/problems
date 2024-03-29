import db
import json
import notifiers

db = db.Database()


def view_cart(login):
    query = "SELECT problems.tasks.task_id, problems.tasks.name FROM problems.cart " \
            "INNER JOIN problems.tasks ON problems.cart.task_id = problems.tasks.task_id " \
            "WHERE problems.cart.login = %s"
    params = [login,]
    return db.select_query(query, params)


def remove_from_cart(task_id, login):
    query = "DELETE FROM problems.cart WHERE login=%s"
    params = [login,]
    if task_id is not None:
        query += " AND task_id=" + task_id
    resp = json.loads(db.update_query(query, params))
    if resp['code'] == 0:
        return True
    else:
        return False


def in_cart(task_id, login):
    query = "SELECT * FROM problems.cart WHERE login=%s AND task_id=%s"
    params = [login, task_id]
    db_response = json.loads(db.select_query(query, params))
    if db_response['code'] == 0 and len(db_response['rows']) == 0:
        return False
    else:
        return True


def add_to_cart(task_id, login):
    if in_cart(task_id, login):
        return True
    else:
        query = "INSERT INTO problems.cart (task_id, login) VALUES (%s,%s)"
        params = [task_id, login]
        db_response = json.loads(db.update_query(query, params))
        if db_response['code'] == 0:
            return True
        else:
            return False
