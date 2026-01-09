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


def test_mapping(db):
    user = User.objects.create(username="leader2004")
    user2 = User.objects.create(username="member")
    user3 = User.objects.create(username="member2")

    group_orm = models.Group.objects.create(name="lala", leader=user)
    group_orm.members.set([user2,user3,user])

    mapped_group = GroupRepository().get(group_orm.id)
    assert mapped_group.leader == group_orm.leader.id
    assert mapped_group.name == group_orm.name

    assert mapped_group.members == set(i.id for i in group_orm.members.all())
    