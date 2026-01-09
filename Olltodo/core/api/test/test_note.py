import pytest
from conftests import api_client, users, group_in_db, tasklist_in_db, task_in_db, note_in_db
from core.repositories import TaskRepository, TaskListRepository, GroupRepository, NoteRepository
from core import models

def test_create_note(db, users, tasklist_in_db):
    data = {"title": "yasosubibu"}

    response = api_client.post(f'/tasklist/{tasklist_in_db.id}/create/note', json=data, user=users['member'])
    print("Error response: ",response.json())

    assert response.status_code == 201
    assert NoteRepository().get(response.json()['note_id']).title == 'yasosubibu'

def test_change_title_note(db, users, note_in_db):
    data = {'title': 'pepe'}

    response = api_client.post(f'/note/{note_in_db.id}/change/title', user=users['member'], json=data)

    assert response.status_code == 200
    assert NoteRepository().get(note_in_db.id).title == 'pepe'


def test_get_notes_by_performer(db,users, note_in_db, tasklist_in_db):

    response = api_client.get(f'/tasklist/{tasklist_in_db.id}/performer/{users['member'].id}', user=users['member2'])

    assert response.status_code == 200
