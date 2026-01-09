import pytest
from conftests import api_client, users, group_in_db, tasklist_in_db, task_in_db
from core.repositories import TaskRepository, TaskListRepository, GroupRepository
from core import models


def test_create_group(db, users):
    data = {'name':'Cool Colds'}

    response = api_client.post('group/create', user=users['left_user'], json=data)
    print(response.json()['group_id'])
    assert response.status_code == 200
    assert GroupRepository().get(response.json()['group_id']).name == 'Cool Colds'

def test_add_new_member_group(db, users, group_in_db):

    response = api_client.post(f'group/{group_in_db.id}/add/{users['left_user'].id}', user=users['leader'])

    assert response.status_code == 200
    assert users['left_user'].id in GroupRepository().get(group_in_db.id).members

def test_remove_member_group(db, users, group_in_db):


    response = api_client.post(f'group/{group_in_db.id}/kick/{users['member'].id}', user=users['leader'])

    assert response.status_code == 200
    assert users['member'].id not in GroupRepository().get(group_in_db.id).members


def test_change_name_group(db,users, group_in_db):
    data = {'name' : 'dodiki'}

    response = api_client.post(f'group/{group_in_db.id}/change_name/', user=users['leader'], json=data)

    assert response.status_code == 200
    assert GroupRepository().get(group_in_db.id).name == 'dodiki'



