# from todo_project.models import Task, User
from todo_project.models import Task
from todo_project import db


def _add_task(auth_client, content='My task'):
    auth_client.post('/add_task', data={'task_name': content}, follow_redirects=True)
    return Task.query.filter_by(content=content).first()


def test_add_task_get(auth_client):
    assert auth_client.get('/add_task').status_code == 200


def test_add_task_creates(auth_client):
    resp = auth_client.post('/add_task', data={'task_name': 'Buy milk'},
                            follow_redirects=True)
    assert resp.status_code == 200
    assert b'Task Created' in resp.data
    assert Task.query.filter_by(content='Buy milk').first() is not None


def test_add_task_invalid_no_create(auth_client):
    auth_client.post('/add_task', data={'task_name': ''}, follow_redirects=True)
    assert Task.query.count() == 0


def test_all_tasks_lists(auth_client):
    _add_task(auth_client, 'Task A')
    resp = auth_client.get('/all_tasks')
    assert resp.status_code == 200
    assert b'Task A' in resp.data


def test_update_task_changes_content(auth_client):
    task = _add_task(auth_client, 'Old content')
    resp = auth_client.post(f'/all_tasks/{task.id}/update_task',
                            data={'task_name': 'New content'}, follow_redirects=True)
    assert resp.status_code == 200
    assert db.session.get(Task, task.id).content == 'New content'


def test_update_task_get_prefills(auth_client):
    task = _add_task(auth_client, 'Prefill me')
    resp = auth_client.get(f'/all_tasks/{task.id}/update_task')
    assert resp.status_code == 200
    assert b'Prefill me' in resp.data


def test_update_task_no_change(auth_client):
    task = _add_task(auth_client, 'Same content')
    resp = auth_client.post(f'/all_tasks/{task.id}/update_task',
                            data={'task_name': 'Same content'}, follow_redirects=True)
    assert b'No Changes Made' in resp.data


def test_update_task_not_found(auth_client):
    resp = auth_client.post('/all_tasks/9999/update_task',
                            data={'task_name': 'x'})
    assert resp.status_code == 404


def test_delete_task(auth_client):
    task = _add_task(auth_client, 'Delete me')
    resp = auth_client.get(f'/all_tasks/{task.id}/delete_task')
    assert resp.status_code == 302
    assert db.session.get(Task, task.id) is None


def test_delete_task_not_found(auth_client):
    resp = auth_client.get('/all_tasks/9999/delete_task')
    assert resp.status_code == 404
