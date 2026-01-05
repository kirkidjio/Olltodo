from core.domain.entities.task import Task, TaskStatus

import pytest

@pytest.fixture
def users():
    leader = 1
    performer = 2
    stranger = 3
    
    return leader, performer, stranger

def test_can_user_submit_his_task(users):
    leader, performer, stranger = users
    task = Task(leader, performer, "abc")
    task.submit(performer)
    
    assert task._status == TaskStatus.SUBMITTED
    
    
def test_can_user_submit_not_his_task(users):
    leader, performer, stranger = users
    task = Task(leader, performer, "abc")
    
    
    with pytest.raises(PermissionError):
        task.submit(stranger)
    
    
def test_can_leader_reject_task(users):
    leader, performer, stranger = users
    task = Task(leader, performer, "abc")
    task.submit(performer)
    task.reject(leader)

    assert task._status == TaskStatus.REJECTED


def test_can_leader_accept_task(users):
    leader, performer, stranger = users
    task = Task(leader, performer, "abc")
    task.submit(performer)
    task.accept(leader)

    assert task._status == TaskStatus.ACCEPTED

def test_can_not_leader_accept_task(users):
    leader, performer, stranger = users
    task = Task(leader, performer, "abc")
    task.submit(performer)
    

    with pytest.raises(PermissionError):
        task.accept(stranger)