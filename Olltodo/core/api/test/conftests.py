import pytest
from ninja.testing import TestClient
from django.contrib.auth.models import User
from core.api.ninja_init import api

from core import models


api_client = TestClient(api)

@pytest.fixture
def users(db):
    return {'leader':User.objects.create_user('leader', 'leader@bebra.com', 'qwerty123'),
            'member': User.objects.create_user('member', 'member@bebra.com', 'qwerty123'),
            'member2': User.objects.create_user('member2', 'member2@bebra.com', 'qwerty123'),
            'left_user': User.objects.create_user('left_user', 'left_user@bebra.com', 'qwerty123')}

@pytest.fixture
def group_in_db(db, users):
    group = models.Group.objects.create(leader=users['leader'], name='Cool Colds')
    group.members.set([users['leader'], users['member'], users['member2']])
    return group

@pytest.fixture
def tasklist_in_db(db, group_in_db):
    tasklist = models.TaskList.objects.create(name='create auth form', group=group_in_db)
    return tasklist

@pytest.fixture
def task_in_db(db, users, tasklist_in_db):
    task1 = models.Task.objects.create(performer=users['member'], title='Berba', tasklist=tasklist_in_db, status='open', priority=0)
    task2 = models.Task.objects.create(performer=users['member2'], title='Pepe', tasklist=tasklist_in_db, status='open', priority=0)


