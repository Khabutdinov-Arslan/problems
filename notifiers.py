from flask import session
from flask import redirect
from flask import url_for


def notify_error(message):
    session['notification'] = {'type': 'alert-danger', 'message': message}


def notify_success(message):
    session['notification'] = {'type': 'alert-success', 'message': message}


def permission_denied():
    notify_error('Доступ запрещен')


def wrong_credentials():
    notify_error('Неверный логин или пароль')


def db_error():
    notify_error('Ошибка базы данных')


def task_added():
    notify_success('Задача добавлена')


def task_deleted():
    notify_success('Задача удалена')


def user_logout():
    notify_success('Успешный выход')


def user_registered():
    notify_success('Регистрация успешна')


def no_task():
    notify_error('Нет такой задачи')


def role_changed():
    notify_success('Роль изменена')


def task_accepted():
    notify_success('Ответ верный')


def task_rejected():
    notify_error('Ответ неверный')


def task_already_solved():
    notify_success('Задача уже решена')
