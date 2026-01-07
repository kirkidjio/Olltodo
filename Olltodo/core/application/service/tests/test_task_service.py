import pytest

from core.domain.entities.task import TaskStatus
from core.domain.entities import Group, Task
from core.domain.models.tasklist import TaskList
from fake_repositories import FakeTaskRepository, FakeTaskListRepository, FakeGroupRepository
from core.application.service.tasks import CreateTask, ChangeTaskStatus, ChangeTaskPriority, ChangeTaskTitle, GetTasksByTasklist
from core.application.service.exceptions import *


LEADER = 1
MEMBER = 2
SECOND_MEMBER=3
THIRD_PERSON=4

TASKLIST_EXISTING = 1
TASKLIST_NOT_EXISTING = 999


@pytest.fixture()
def entities():
    return {
        'group' : Group(id_=1, leader_id=LEADER, name="frontend team", members_id={MEMBER, SECOND_MEMBER}),
        'tasklist' : TaskList(id_=1, name="Authorization Form", group_id=1),

    }

@pytest.fixture()
def repos(entities):
    return {
        'task_rep' : FakeTaskRepository([[Task(checker_id=LEADER, performer_id=MEMBER, title="abc", id_=1), TASKLIST_EXISTING]]),
        'group_rep' : FakeGroupRepository([entities['group']]),
        'tasklist_rep' : FakeTaskListRepository([entities['tasklist']])
    }


def test_creating_task(entities, repos):

    task_id = CreateTask().execute(actor_id=entities['group'].leader,
        performer_id=MEMBER,
        title="abc",
        tasklist_id=entities['tasklist'].id_,
        task_rep = repos['task_rep'],
        group_rep = repos['group_rep'],
        tasklist_rep = repos['tasklist_rep'])

    assert repos['task_rep'].get(task_id).title == "abc"
    assert repos['task_rep'].get(task_id).checker == entities['group'].leader



@pytest.mark.parametrize("leader, member, tasklist_id, expected", [(MEMBER,THIRD_PERSON,TASKLIST_EXISTING,NotGroupLeader),
                                                                   (LEADER,THIRD_PERSON,TASKLIST_EXISTING, PerformerNotInGroup),
                                                                   (LEADER,MEMBER,TASKLIST_NOT_EXISTING,TaskListNotFound)])
def test_creating_task_errors(leader, member, tasklist_id ,expected, entities, repos):

    with pytest.raises(expected):
        task_id = CreateTask().execute(actor_id=leader,
            performer_id=member,
            title="abc",
            tasklist_id=tasklist_id,
            task_rep=repos['task_rep'],
            group_rep=repos['group_rep'],
            tasklist_rep=repos['tasklist_rep'])

@pytest.mark.parametrize("actor, task_status ,action, expected", [(LEADER,TaskStatus.SUBMITTED,'accept',TaskStatus.ACCEPTED),
                                                     (LEADER, TaskStatus.SUBMITTED,'reject', TaskStatus.REJECTED),
                                                     (MEMBER, TaskStatus.OPEN, 'submit', TaskStatus.SUBMITTED),
                                                     (MEMBER, TaskStatus.REJECTED, 'submit', TaskStatus.SUBMITTED)
                                                     ])
def test_change_status_task_happy_path(entities, repos, actor,action,expected, task_status):
    task = FakeTaskRepository([[Task(checker_id=LEADER, performer_id=MEMBER, title="abc", id_=1, status=task_status), TASKLIST_EXISTING]])

    status_changed_task = ChangeTaskStatus().execute(
            task_id=1,
            actor_id=actor,
            action = action,
            task_rep=task,
            )

    task_status=task.get(1).status
    assert task_status == expected


@pytest.mark.parametrize("actor, action, expected", [(LEADER,'submit',PermissionError),
                                                     (MEMBER, 'accept', PermissionError),
                                                     (MEMBER, 'reject', PermissionError),
                                                     ])

def test_change_status_task_permission_errors(entities ,repos, actor, action, expected):

    with pytest.raises(expected):
        status_changed_task = ChangeTaskStatus().execute(
            task_id=1,
            actor_id=actor,
            action=action,
            task_rep=repos['task_rep'],
            )


def test_change_task_priority_happy_path(entities, repos):
    new_priority =2

    ChangeTaskPriority().execute(
        actor_id=LEADER,
        task_id=1,
        priority=new_priority,
        task_rep=repos['task_rep']
    )
    assert repos['task_rep'].get(1).priority == new_priority



def test_change_task_title_happy_path(entities, repos):
    new_title = 'create authorization form'

    ChangeTaskTitle().execute(
        actor_id=LEADER,
        task_id=1,
        title=new_title,
        task_rep=repos['task_rep']
    )
    assert repos['task_rep'].get(1).title == new_title


def test_get_task_by_tasklist_dict(repos):
    task_info = GetTasksByTasklist().execute(tasklist_id=TASKLIST_EXISTING,
                        actor_id=MEMBER,
                        task_rep=repos['task_rep'],
                        group_rep=repos['group_rep'],
                        tasklist_rep=repos['tasklist_rep']
    )
    task = repos['task_rep'].get_by_tasklist(TASKLIST_EXISTING)

    assert task_info[0]['id'] == task[0].id
    assert task_info[0]['checker'] == task[0].checker