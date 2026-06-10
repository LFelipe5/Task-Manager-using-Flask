from todo_project import db
from todo_project.models import User, Task, load_user


def test_user_repr(make_user):
    user = make_user(username='alice')
    assert repr(user) == "User('alice')"


def test_task_repr_and_author_relationship(make_user):
    user = make_user(username='bob')
    task = Task(content='Write tests', author=user)
    db.session.add(task)
    db.session.commit()

    assert task.content == 'Write tests'
    assert task.user_id == user.id
    assert task.author == user
    assert user.tasks == [task]
    assert repr(task) == f"Task('Write tests', '{task.date_posted}', '{user.id}')"


def test_task_has_default_date(make_user):
    user = make_user(username='carol')
    task = Task(content='Dated task', author=user)
    db.session.add(task)
    db.session.commit()
    assert task.date_posted is not None


def test_load_user_returns_user(make_user):
    user = make_user(username='dave')
    loaded = load_user(str(user.id))
    assert loaded is not None
    assert loaded.id == user.id


def test_load_user_unknown_returns_none(app):
    assert load_user('99999') is None
