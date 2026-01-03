from core import models
from core.domain.models.tasklist import TaskList
from django.contrib.auth.models import User
from core.repositories.tasklist_repository import TaskListRepository


def test_can_add_and_get_tasklist(db):
    
    user = User.objects.create(username="u")
    
    group = models.Group.objects.create(name="gh", leader=user)
    group.members.add(user)
    
    rep = TaskListRepository()
    
    tasklist = TaskList(id_=None, name="Authorization form", group_id=group.id)
    rep.save(tasklist, group.id)
    tasklist_from_db = rep.get(1)
    assert tasklist.name == tasklist_from_db.name and tasklist.group_id == tasklist_from_db.group_id
    