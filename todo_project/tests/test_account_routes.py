from flask import abort

from todo_project import app as flask_app, bcrypt
from todo_project.models import User


@flask_app.route('/_force_403')
def _force_403():
    abort(403)


@flask_app.route('/_force_500')
def _force_500():
    abort(500)


def test_account_get_prefills_username(auth_client):
    resp = auth_client.get('/account')
    assert resp.status_code == 200
    assert b'tester' in resp.data


def test_account_updates_username(auth_client):
    resp = auth_client.post('/account', data={'username': 'renamed'},
                            follow_redirects=True)
    assert resp.status_code == 200
    assert b'Username Updated Successfully' in resp.data
    assert User.query.filter_by(username='renamed').first() is not None


def test_account_same_username_no_message(auth_client):
    resp = auth_client.post('/account', data={'username': 'tester'},
                            follow_redirects=True)
    assert resp.status_code == 200
    assert b'Username Updated Successfully' not in resp.data


def test_change_password_get(auth_client):
    assert auth_client.get('/account/change_password').status_code == 200


def test_change_password_success(auth_client):
    resp = auth_client.post('/account/change_password', data={
        'old_password': 'secret123', 'new_password': 'brandnew'},
        follow_redirects=True)
    assert b'Password Changed Successfully' in resp.data
    user = User.query.filter_by(username='tester').first()
    assert bcrypt.check_password_hash(user.password, 'brandnew')


def test_change_password_wrong_old(auth_client):
    resp = auth_client.post('/account/change_password', data={
        'old_password': 'wrongold', 'new_password': 'brandnew'},
        follow_redirects=True)
    assert b'Please Enter Correct Password' in resp.data


def test_error_404(client):
    resp = client.get('/this-route-does-not-exist')
    assert resp.status_code == 404


def test_error_403_handler(app):
    resp = app.test_client().get('/_force_403')
    assert resp.status_code == 403


def test_error_500_handler(app):
    app.config['TESTING'] = False
    app.config['PROPAGATE_EXCEPTIONS'] = False
    try:
        resp = app.test_client().get('/_force_500')
        assert resp.status_code == 500
    finally:
        app.config['TESTING'] = True
        app.config['PROPAGATE_EXCEPTIONS'] = None
