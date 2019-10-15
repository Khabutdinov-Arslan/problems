import db
import json
from flask import request

db = db.Database()
credentials_cache = {}


def user_exists(login):
    query = "SELECT * FROM problems.users WHERE login = %s"
    params = [login, ]
    res = json.loads(db.select_query(query, params))
    if len(res["rows"]) > 0:
        return True
    else:
        return False


def add_user(*args):
    if user_exists(args[0]):
        return json.dumps({"code": 3, "message": "Логин занят"})

    query = "INSERT INTO problems.users(login, password, name, surname, role) " \
            "VALUES (%s, %s, %s, %s, %s)"
    params = [i for i in args]
    print(params)
    db_response = json.loads(db.update_query(query, params))
    if db_response['code'] == 0:
        return json.dumps({"code": 0, "message": "Успешная регистрация"})
    else:
        return json.dumps({"code": 4, "message": db_response["message"]})


def users_list():
    query = "SELECT login, name, surname, role FROM problems.users"
    db_response = json.loads(db.select_query(query, ()))
    return json.dumps(db_response)


def get_overall_rating():
    query = "SELECT problems.users.login, COUNT(task_id) FROM problems.users " \
            "INNER JOIN problems.users_tasks ON problems.users.login = problems.users_tasks.login " \
            "GROUP BY problems.users.login"
    db_response = json.loads(db.select_query(query, ()))
    return json.dumps(db_response)


def check_credentials(login, password):
    query = "SELECT password, role FROM problems.users WHERE login=%s"
    params = [login,]
    res = json.loads(db.select_query(query, params))
    if len(res["rows"]) == 0:
        resp = {"code": 1, "message": "Неверный логин", "role": -1}
    else:
        if password == res["rows"][0][0]:
            resp = {"code": 0, "message": "Успешная авторизация", "role": res["rows"][0][1]}
        else:
            resp = {"code": 2, "message": "Неверный пароль", "role": -1}
    return json.dumps(resp)


def get_credentials():
    if ('problems_login' in request.cookies) and ('problems_password' in request.cookies):
        login = request.cookies.get('problems_login')
        password = request.cookies.get('problems_password')
        credentials = login, password
        if credentials in credentials_cache:
            return credentials_cache[credentials]
        else:
            login_response = json.loads(check_credentials(login, password))
            if login_response['code'] == 0:
                credentials_cache[credentials] = login_response
                return login_response
            else:
                return None
    else:
        return None


def get_role():
    resp = get_credentials()
    if resp is None:
        return -1
    else:
        return resp['role']


def change_role(login, role):
    query = "UPDATE problems.users SET role = %s WHERE login = %s"
    params = [role, login]
    resp = json.loads(db.update_query(query, params))
    return json.dumps(resp)


def is_admin():
    resp = get_credentials()
    return resp is not None and resp['role'] == 2


def is_student():
    resp = get_credentials()
    return resp is not None and resp['role'] == 0


def is_teacher():
    resp = get_credentials()
    return resp is not None and resp['role'] == 1


def is_logged():
    return get_credentials() is not None
