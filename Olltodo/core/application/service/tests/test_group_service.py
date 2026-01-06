import pytest

from core.domain.entities import Group
from fake_repositories import FakeGroupRepository
from core.application.service.groups import CreateGroup, AddNewMemberGroup, RemoveMemberGroup, ChangeNameGroup

LEADER = 1
MEMBER = 2
SECOND_MEMBER=3
THIRD_PERSON=4


@pytest.fixture
def group_rep():
    return FakeGroupRepository([Group(id_=1, leader_id=LEADER, name="frontend team", members_id={MEMBER, SECOND_MEMBER})])


def test_group_creating_happy_path(group_rep):


    CreateGroup().execute(actor_id=THIRD_PERSON,
                          name='backend team',
                          group_rep=group_rep)

    new_group = group_rep.get(2)

    assert new_group.name == 'backend team'
    assert new_group.leader == THIRD_PERSON


def test_group_add_new_members(group_rep):

    AddNewMemberGroup().execute(group_id=1 ,actor_id=LEADER, new_member=THIRD_PERSON, group_rep=group_rep)

    assert THIRD_PERSON in group_rep.get(1).members

def test_group_remove_member(group_rep):

    RemoveMemberGroup().execute(group_id=1, actor_id=LEADER, member=MEMBER, group_rep=group_rep)

    assert MEMBER not in group_rep.get(1).members

def test_group_change_name(group_rep):


    ChangeNameGroup().execute(group_id=1, actor_id=LEADER, name="backend team", group_rep=group_rep)

    assert group_rep.get(1).name == 'backend team'