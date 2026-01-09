import pytest
from conftests import api_client, users, group_in_db, tasklist_in_db, task_in_db, note_in_db
from core.repositories import TaskRepository, TaskListRepository, GroupRepository, NoteRepository
from core import models

def test_create_tasklist(db,users,group_in_db):
    data = {'name':'pepe'}
    response = api_client.post(f'/group/{group_in_db.id}/create/tasklist', user=users['leader'], json=data)

    assert response.status_code == 200
    assert TaskListRepository().get(response.json()['tasklist_id']).group_id == group_in_db.id

