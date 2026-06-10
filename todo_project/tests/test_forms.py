from flask_login import login_user

from todo_project.forms import (RegistrationForm, LoginForm, UpdateUserInfoForm,
                                UpdateUserPassword, TaskForm, UpdateTaskForm)


def _form(app, form_cls, data):
    with app.test_request_context(method='POST', data=data):
        form = form_cls(meta={'csrf': False})
        form.validate()
        return form


def test_registration_form_valid(app):
    form = _form(app, RegistrationForm, {
        'username': 'newuser', 'password': 'pw', 'confirm_password': 'pw'})
    assert not form.errors


def test_registration_form_password_mismatch(app):
    form = _form(app, RegistrationForm, {
        'username': 'newuser', 'password': 'pw', 'confirm_password': 'other'})
    assert 'confirm_password' in form.errors


def test_registration_form_username_too_short(app):
    form = _form(app, RegistrationForm, {
        'username': 'ab', 'password': 'pw', 'confirm_password': 'pw'})
    assert 'username' in form.errors


def test_registration_form_duplicate_username(app, make_user):
    make_user(username='taken')
    form = _form(app, RegistrationForm, {
        'username': 'taken', 'password': 'pw', 'confirm_password': 'pw'})
    assert 'username' in form.errors
    assert any('Exists' in m for m in form.username.errors)


def test_login_form_requires_fields(app):
    form = _form(app, LoginForm, {'username': '', 'password': ''})
    assert 'username' in form.errors
    assert 'password' in form.errors


def test_update_user_info_same_username_ok(app, make_user):
    user = make_user(username='sameone')
    with app.test_request_context(method='POST', data={'username': 'sameone'}):
        login_user(user)
        form = UpdateUserInfoForm(meta={'csrf': False})
        assert form.validate()


def test_update_user_info_duplicate_username(app, make_user):
    current = make_user(username='current')
    make_user(username='other')
    with app.test_request_context(method='POST', data={'username': 'other'}):
        login_user(current)
        form = UpdateUserInfoForm(meta={'csrf': False})
        assert not form.validate()
        assert any('Exists' in m for m in form.username.errors)


def test_update_user_password_requires_fields(app):
    form = _form(app, UpdateUserPassword, {'old_password': '', 'new_password': ''})
    assert 'old_password' in form.errors
    assert 'new_password' in form.errors


def test_task_form_requires_name(app):
    form = _form(app, TaskForm, {'task_name': ''})
    assert 'task_name' in form.errors


def test_task_form_valid(app):
    form = _form(app, TaskForm, {'task_name': 'Do something'})
    assert not form.errors


def test_update_task_form_valid(app):
    form = _form(app, UpdateTaskForm, {'task_name': 'Changed'})
    assert not form.errors
