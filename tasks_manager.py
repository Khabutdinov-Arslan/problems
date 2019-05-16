import db
import json

db = db.Database()


# name, topic, difficulty, statement, solution, answer

def add_task(*args):
    query = "INSERT INTO problems.tasks(name, topic, difficulty, statement, solution, answer) " \
            "VALUES (%s, %s, %s, %s, %s, %s)"
    params = [i for i in args]
    return db.update_query(query, params)


def edit_task(*args):
    query = "UPDATE problems.tasks " \
            "SET name = %s, topic = %s, difficulty = %s, statement = %s, solution = %s, answer = %s " \
            "WHERE task_id=%s"
    params = [args[i] for i in range(1, 7)]
    params.append(args[0])
    return db.update_query(query, params)


def delete_task(task_id):
    query = "DELETE FROM problems.tasks WHERE task_id = %s"
    params = [task_id,]
    return db.update_query(query, params)


def get_tasks_list(topic=None):
    params = []
    if topic is None:
        query = "SELECT task_id, name, topic, difficulty FROM problems.tasks"
    else:
        query = "SELECT task_id, name, topic, difficulty FROM problems.tasks " \
                "WHERE topic = %s"
        params.append(topic)
    return db.select_query(query, params)


def get_task(task_id):
    query = "SELECT task_id, name, topic, difficulty, statement, solution, answer FROM problems.tasks WHERE task_id=%s"
    params = [task_id,]
    return db.select_query(query, params)


def user_has_task(task_id, login):
    query = "SELECT task_id, login FROM problems.users_tasks WHERE task_id=%s and login = %s"
    params = [task_id, login]
    db_response = json.loads(db.select_query(query, params))
    return len(db_response['rows']) > 0


def check_task(task_id, login, answer):
    query = "SELECT answer FROM problems.tasks WHERE task_id=%s"
    params = [task_id,]
    db_response = json.loads(db.select_query(query, params))
    if db_response['code'] != 0:
        return json.dumps({'code': 2})
    reference = db_response['rows'][0][0]
    if answer == reference:
        if user_has_task(task_id, login):
            return json.dumps({'code': 3})
        else:
            query = "INSERT INTO problems.users_tasks(login, task_id) VALUES (%s, %s)"
            params = [login, task_id]
            db_response = json.loads(db.update_query(query, params))
            if db_response['code'] == 0:
                return json.dumps({'code': 0})
            else:
                return json.dumps({'code': 2})
    else:
        return json.dumps({'code': 1})


def get_topics_list():
    query = "SELECT topic_id, name FROM problems.topics"
    return db.select_query(query, ())
