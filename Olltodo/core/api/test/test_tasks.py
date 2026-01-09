import pytest
from conftests import api_client, users, group_in_db, tasklist_in_db, task_in_db
from core.repositories import TaskRepository, TaskListRepository
from core import models


def test_get_tasks_by_tasklist(db, users, task_in_db):

    response = api_client.get('/tasklist/1', user=users['member'])

    assert response.status_code == 200
    assert response.json()[0]['id'] == 1
    assert response.json()[0]['status'] == 'open'

def test_get_task_by_performer(db, users, task_in_db):

    response = api_client.get('/tasklist/1/performer/2', user=users['member'])

    assert response.status_code == 200
    for i in response.json():
        assert i['performer'] == 2


@pytest.mark.parametrize("actor, task_status, action, expected", [('member', 'open', 'submit', 'submitted'),
                                                                 ('leader', 'submitted', 'accept', 'accepted'),
                                                                 ('leader', 'submitted', 'reject', 'rejected'),
                                                                 ('member', 'rejected', 'submit', 'submitted')])
def test_change_task_status(db,users, actor, task_status, action, expected, tasklist_in_db):
    task = models.Task.objects.create(performer=users['member'], title="asdf", tasklist=tasklist_in_db, status=task_status, priority=0)

    response = api_client.patch(f'task/{task.id}/{action}', user=users[actor])

    assert TaskRepository().get(task.id).status == expected


def test_create_task(db, users, task_in_db, tasklist_in_db):
    data = {"title": "yasosubibu", "performer":users['member'].id, "priority":0}

    response = api_client.post(f'/tasklist/{tasklist_in_db.id}/create/task', json=data, user=users['leader'])
    print("Error response: ",response.json())

    assert response.status_code == 201
    assert TaskRepository().get(response.json()['task_id']).title == 'yasosubibu'


def test_change_priority_task(db, users, task_in_db):
    data = {"priority" : 3}
    response = api_client.post(f'task/{task_in_db['task1'].id}/change/priority', user=users['leader'], json=data)

    assert response.status_code == 200
    assert TaskRepository().get(task_in_db['task1'].id).priority == 3


def test_change_title_task(db, users, task_in_db):
    data = {"title" : 'bebra'}
    response = api_client.post(f'task/{task_in_db['task1'].id}/change/title', user=users['leader'], json=data)

    assert response.status_code == 200
    assert TaskRepository().get(task_in_db['task1'].id).title == 'bebra'

