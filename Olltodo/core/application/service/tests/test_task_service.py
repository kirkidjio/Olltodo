import pytest
from core.domain.entities.group import Group
from core.domain.models.tasklist import TaskList
from fake_repositories import FakeTaskRepository, FakeTaskListRepository, FakeGroupRepository
from core.application.service.tasks import CreateTask
from core.application.service.exceptions import *

@pytest.fixture()
def entities():
    return {
        'group' : Group(id_=1, leader_id=1, name="frontend team", members_id={2, 3}),
        'tasklist' : TaskList(id_=1, name="Authorization Form", group_id=1),

    }

@pytest.fixture()
def repos(entities):
    return {
        'task_rep' : FakeTaskRepository(),
        'group_rep' : FakeGroupRepository([entities['group']]),
        'tasklist_rep' : FakeTaskListRepository([entities['tasklist']])
    }


def test_creating_task(entities, repos):

    task_id = CreateTask().execute(actor_id=entities['group'].leader,
        performer_id=2,
        title="abc",
        tasklist_id=entities['tasklist'].id_,
        task_rep = repos['task_rep'],
        group_rep = repos['group_rep'],
        tasklist_rep = repos['tasklist_rep'])

    assert repos['task_rep'].get(task_id).title == "abc"
    assert repos['task_rep'].get(task_id).checker == entities['group'].leader



@pytest.mark.parametrize("leader, member, tasklist_id, expected", [(2,4,1,NotGroupLeader), (1,4,1, PerformerNotInGroup), (1,2,5,TaskListNotFound)])
def test_creating_task_errors(leader, member, tasklist_id ,expected, entities, repos):

    with pytest.raises(expected):
        task_id = CreateTask().execute(actor_id=leader,
            performer_id=member,
            title="abc",
            tasklist_id=tasklist_id,
            task_rep=repos['task_rep'],
            group_rep=repos['group_rep'],
            tasklist_rep=repos['tasklist_rep'])


