from core.domain.entities.group import Group

import pytest

@pytest.fixture
def group_and_some_users():
    leader = 1
    operating_member = 2
    stranger = 3
    group = Group(1, leader, "UI/UX Designers", set())
    
    return leader, operating_member, stranger, group

def test_leader_and_stranger_can_add_member(group_and_some_users):
    leader, operating_member, stranger, group = group_and_some_users
    group.add(leader, operating_member)
    assert operating_member in group.members

    with pytest.raises(PermissionError):
        group.add(operating_member, stranger)
    
    
    
def test_leader_and_stranger_can_rem_member(group_and_some_users):
    leader, operating_member, stranger, group = group_and_some_users
    group.add(leader, operating_member)
    group.rem(leader, operating_member)
    assert bool(operating_member not in group.members)
    group.add(leader, stranger)
    

    with pytest.raises(PermissionError):
        group.rem(operating_member, stranger)




def test_leader_and_member_can_change_name(group_and_some_users):
    leader, operating_member, stranger, group = group_and_some_users
    
    group.change_name(leader, "someName")
    
    assert group.name == "someName"
    
    with pytest.raises(PermissionError):
        group.change_name(operating_member, "BEBRA")
    
    
    
def test_can_leader_add_one_member_more_then_one_time(group_and_some_users):
    leader, operating_member, stranger, group = group_and_some_users
    
    group.add(leader, operating_member)
    
    with pytest.raises(ValueError):
        group.add(leader, operating_member)
        

