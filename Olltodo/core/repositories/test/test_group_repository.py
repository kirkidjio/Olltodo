from core.domain.entities.group import Group
from core import models
from django.contrib.auth.models import User
from core.repositories.group_repository import GroupRepository

def test_can_get_and_save_group(db):
    user = User.objects.create(username="leader2004")
    group = Group(id_=None, leader_id=1, name="Cool Colds team")
    
    rep = GroupRepository()
    rep.save(group)

    group_from_database = rep.get(1)
    assert group.name == group_from_database.name
    assert group.leader == group_from_database.leader
    