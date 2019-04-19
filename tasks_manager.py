import db
import json

db = db.Database()


# name, topic, difficulty, statement, solution, answer

def add_task(*args):
    query = "INSERT INTO problems.tasks(name, topic, difficulty, statement, solution, answer) " \
            "VALUES ('{}', '{}', {}, '{}', '{}', '{}')".format(*args)
    return db.update_query(query)


def edit_task(*args):
    query = "UPDATE problems.tasks SET name ='" + args[1] + "', topic ='" + args[2] + "', difficulty = " + args[
        3] + ", statement = '" + args[4] + "', solution = '" + args[5] + "', answer ='" + args[6] + "' " \
                                                                                                    "WHERE task_id=" + \
            args[0]
    return db.update_query(query)


def delete_task(task_id):
    query = "DELETE FROM problems.tasks WHERE task_id = " + task_id
    return db.update_query(query)


def get_tasks_list(topic=None):
    if topic is None:
        query = "SELECT task_id, name, topic, difficulty FROM problems.tasks"
    else:
        query = "SELECT task_id, name, topic, difficulty FROM problems.tasks WHERE topic = '" + topic + "'"
    return db.select_query(query)


def get_task(task_id):
    query = "SELECT task_id, name, topic, difficulty, statement, solution, answer FROM problems.tasks WHERE task_id=" + task_id
    return db.select_query(query)


def user_has_task(task_id, login):
    query = "SELECT task_id, login FROM problems.users_tasks WHERE task_id=" + task_id + " and login = '" + login + "'"
    db_response = json.loads(db.select_query(query))
    return len(db_response['rows']) > 0


def check_task(task_id, login, answer):
    query = "SELECT answer FROM problems.tasks WHERE task_id=" + task_id
    db_response = json.loads(db.select_query(query))
    if db_response['code'] != 0:
        return json.dumps({'code': 2})
    reference = db_response['rows'][0][0]
    if answer == reference:
        if user_has_task(task_id, login):
            return json.dumps({'code': 3})
        else:
            query = "INSERT INTO problems.users_tasks(login, task_id) VALUES ('" + login + "', " + task_id + ")"
            db_response = json.loads(db.update_query(query))
            if db_response['code'] == 0:
                return json.dumps({'code': 0})
            else:
                return json.dumps({'code': 2})
    else:
        return json.dumps({'code': 1})
