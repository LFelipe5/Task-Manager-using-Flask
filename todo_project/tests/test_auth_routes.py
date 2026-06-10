from todo_project.models import User


def test_about_pages_ok(client):
    assert client.get('/').status_code == 200
    assert client.get('/about').status_code == 200


def test_register_get(client):
    resp = client.get('/register')
    assert resp.status_code == 200


def test_register_creates_user(client):
    resp = client.post('/register', data={
        'username': 'fresh', 'password': 'pw', 'confirm_password': 'pw'},
        follow_redirects=True)
    assert resp.status_code == 200
    assert User.query.filter_by(username='fresh').first() is not None


def test_register_duplicate_rejected(client, make_user):
    make_user(username='dupe')
    client.post('/register', data={
        'username': 'dupe', 'password': 'pw', 'confirm_password': 'pw'})
    assert User.query.filter_by(username='dupe').count() == 1


def test_login_get(client):
    assert client.get('/login').status_code == 200


def test_login_success(client, make_user):
    make_user(username='loginuser', password='mypassword')
    resp = client.post('/login', data={
        'username': 'loginuser', 'password': 'mypassword'},
        follow_redirects=True)
    assert resp.status_code == 200
    assert b'Login Successfull' in resp.data


def test_login_wrong_password(client, make_user):
    make_user(username='loginuser', password='mypassword')
    resp = client.post('/login', data={
        'username': 'loginuser', 'password': 'wrong'},
        follow_redirects=True)
    assert b'Login Unsuccessful' in resp.data


def test_login_unknown_user(client):
    resp = client.post('/login', data={
        'username': 'ghost', 'password': 'whatever'},
        follow_redirects=True)
    assert b'Login Unsuccessful' in resp.data


def test_logout_redirects(auth_client):
    resp = auth_client.get('/logout')
    assert resp.status_code == 302


def test_authenticated_register_redirects(auth_client):
    resp = auth_client.get('/register')
    assert resp.status_code == 302


def test_authenticated_login_redirects(auth_client):
    resp = auth_client.get('/login')
    assert resp.status_code == 302


def test_protected_routes_redirect_when_anonymous(client):
    for route in ['/all_tasks', '/add_task', '/account', '/account/change_password']:
        resp = client.get(route)
        assert resp.status_code == 302
