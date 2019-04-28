from flask import Flask
from flask import request
from flask import render_template
from flask import make_response
from flask import redirect
from flask import session
from flask import url_for
import json
import tasks_manager
import users_manager
import notifiers

app = Flask(__name__)
app.secret_key = 'mellon'


@app.context_processor
def common_properties():
    data = dict()
    data['topics'] = {'geometry': 'геометрия', 'number_theory': 'теория чисел'}
    if users_manager.is_logged():
        data['login'] = request.cookies.get('problems_login')
        data['role'] = users_manager.get_role()
    else:
        data['role'] = -1
    if 'notification' in session:
        data['notification'] = session['notification']
        session.pop('notification')
    return data


@app.route('/', methods=['GET', 'POST'])
def main_page():
    return render_template('index.html')


@app.route('/login')
def login_form():
    return render_template('login.html')


@app.route('/logout')
def logout():
    resp = make_response(redirect(url_for('main_page')))
    resp.set_cookie('problems_login', '', max_age=0)
    resp.set_cookie('problems_password', '', max_age=0)
    return resp


@app.route('/login_handler', methods=['POST'])
def login():
    resp = redirect(url_for('main_page'))
    login_result = json.loads(users_manager.check_credentials(request.form['login'], request.form['password']))
    if login_result['code'] == 0:
        resp.set_cookie('problems_login', request.form['login'], max_age=60 * 60 * 24 * 7)
        resp.set_cookie('problems_password', request.form['password'], max_age=60 * 60 * 24 * 7)
    else:
        notifiers.wrong_credentials()
    return resp


@app.route('/register')
def registration_form():
    return render_template('register.html')


@app.route('/registration_handler', methods=['POST'])
def registration_handler():
    resp = json.loads(users_manager.add_user(request.form['login'], request.form['password'], request.form['name'],
                                             request.form['surname'], 0, 0))
    if resp['code'] == 0:
        notifiers.user_registered()
    else:
        notifiers.notify_error(resp['message'])
    return redirect(url_for('main_page'))


@app.route('/users')
def users_list():
    if not users_manager.is_admin():
        notifiers.permission_denied()
        return redirect(url_for('main_page'))
    db_response = json.loads(users_manager.users_list())
    if db_response['code'] != 0:
        notifiers.db_error()
        return redirect(url_for('main_page'))
    return render_template('users.html', users_list=db_response['rows'])


@app.route('/change_role', methods=['POST'])
def change_role():
    if not users_manager.is_admin():
        notifiers.permission_denied()
        return redirect(url_for('main_page'))
    resp = json.loads(users_manager.change_role(request.form['login'], request.form['role']))
    if resp['code'] != 0:
        notifiers.db_error()
    else:
        notifiers.role_changed()
    return json.dumps(resp)


@app.route('/tasks', defaults={'topic': None})
@app.route('/tasks/<topic>')
def tasks_list(topic=None):
    db_response = json.loads(tasks_manager.get_tasks_list(topic))
    if db_response['code'] != 0:
        notifiers.db_error()
        return redirect(url_for('main_page'))

    return render_template('tasks.html', tasks_list=db_response['rows'], topic=topic)


@app.route('/task/<task_id>')
def view_task(task_id=None):
    db_response = json.loads(tasks_manager.get_task(task_id))
    if db_response['code'] != 0:
        notifiers.db_error()
        return redirect(url_for('main_page'))

    if len(db_response['rows']) == 0:
        notifiers.no_task()
        return redirect(url_for(tasks_list))
    if users_manager.is_logged():
        return render_template('task.html', task=db_response['rows'][0],
                               solved=tasks_manager.user_has_task(task_id, request.cookies.get('problems_login')))
    else:
        return render_template('task.html', task=db_response['rows'][0])


@app.route('/check_task', methods=['POST'])
def check_task():
    if users_manager.is_student():
        resp = json.loads(tasks_manager.check_task(request.form['task_id'], request.cookies.get('problems_login'),
                                                   request.form['answer']))

        if resp['code'] == 0:
            notifiers.task_accepted()
        elif resp['code'] == 1:
            notifiers.task_rejected()
        else:
            notifiers.db_error()
        return json.dumps(resp)
    else:
        notifiers.permission_denied()
        return redirect(url_for('tasks_list'))


@app.route('/delete/<task_id>')
def delete_task(task_id=None):
    if users_manager.is_admin():
        db_response = json.loads(tasks_manager.delete_task(task_id))
        if db_response['code'] == 0:
            notifiers.task_deleted()
        else:
            notifiers.db_error()
    else:
        notifiers.permission_denied()
    return redirect(url_for('tasks_list'))


@app.route('/add_task')
def add_task():
    return render_template('add_task.html')


@app.route('/add_task_handler', methods=['POST'])
def add_task_form():
    if not users_manager.is_admin():
        notifiers.permission_denied()
        return redirect(url_for('login_form'))
    db_response = json.loads(
        tasks_manager.add_task(request.form['name'], request.form['topic'], request.form['difficulty'],
                               request.form['statement'], request.form['solution'], request.form['answer']))
    if db_response['code'] != 0:
        notifiers.db_error()
        return redirect(url_for('main_page'))

    notifiers.task_added()
    return redirect(url_for('tasks_list'))


@app.route('/edit/<task_id>')
def edit_task_form(task_id):
    if not users_manager.is_admin():
        notifiers.permission_denied()
        return redirect(url_for('login_form'))
    db_response = json.loads(tasks_manager.get_task(task_id))
    if len(db_response['rows']) == 0:
        notifiers.db_error()
        return redirect(url_for('tasks_list'))
    task = db_response['rows'][0]
    return render_template('edit_task.html', task=task)


@app.route('/edit_task_handler', methods=['POST'])
def edit_task():
    if not users_manager.is_admin():
        notifiers.permission_denied()
        return redirect(url_for('login_form'))
    db_response = json.loads(
        tasks_manager.edit_task(request.form['task_id'], request.form['name'], request.form['topic'],
                                request.form['difficulty'],
                                request.form['statement'], request.form['solution'], request.form['answer']))
    if db_response['code'] != 0:
        notifiers.db_error()
    return redirect(url_for('tasks_list'))


@app.route('/rating')
def rating():
    resp = json.loads(users_manager.get_overall_rating())
    if resp['code'] != 0:
        notifiers.db_error()
        return redirect(url_for('main_page'))
    return render_template('rating.html', users_list=resp['rows'])
