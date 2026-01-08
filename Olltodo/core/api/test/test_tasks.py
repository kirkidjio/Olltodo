import pytest
from conftests import api_client, users, group_in_db, tasklist_in_db, task_in_db
from core.repositories import TaskRepository
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


def test_create_task():
    data = {}

    response = api_client.post()
