from core.repositories.task_repository import TaskRepository
from core.domain.entities.task import Task, TaskStatus, TaskPriority
from core.models import TaskList, Group
from django.contrib.auth.models import User
import pytest



def test_can_add_and_get_tasks(db):
    
    user = User.objects.create(username="u")
    
    group = Group.objects.create(name="gh", leader=user)
    group.members.add(user)
    
    tasklist = TaskList.objects.create(name="Juniors Frontend", group=group)
    
    rep = TaskRepository()
    
    task = Task(checker_id=1, performer_id=1, title="Do authorization form", id_ = None)
    
    rep.save(task, 1)
    task_from_rep = rep.get_by_tasklist(1)
    
    assert task_from_rep[-1].title == task.title
    assert task_from_rep[-1].status == task.status
    
    
    