import pytest

from core.domain.models import TaskList
from core.domain.entities import Note, Group
from fake_repositories import FakeNoteRepository, FakeGroupRepository, FakeTaskListRepository
from core.application.service.notes import CreateNote, ChangeTitleNote, ChangeContentNote

LEADER = 1
MEMBER = 2
SECOND_MEMBER = 3
THIRD_PERSON = 5

TASKLIST_EXISTING = 1
TASKLIST_NOT_EXISTING = 999

GROUP_EXISTING = 1

@pytest.fixture()
def entities():
    return {
        'group' : Group(id_=GROUP_EXISTING, leader_id=LEADER, name="frontend team", members_id={MEMBER, SECOND_MEMBER}),
        'tasklist' : TaskList(id_=TASKLIST_EXISTING, name="Authorization Form", group_id=GROUP_EXISTING),
        'note': Note(MEMBER, 'how to fix this', id_=1)
    }

@pytest.fixture()
def repos(entities):
    return {
        'note_rep' : FakeNoteRepository([[entities['note'], TASKLIST_EXISTING]]),
        'group_rep' : FakeGroupRepository([entities['group']]),
        'tasklist_rep' : FakeTaskListRepository([entities['tasklist']])
    }

def test_creating_note_happy_path(repos):

    CreateNote().execute(actor_id=MEMBER,
        title="abc",
        tasklist_id=TASKLIST_EXISTING,
        note_rep = repos['note_rep'],
        group_rep = repos['group_rep'],
        tasklist_rep = repos['tasklist_rep'])

    print (repos['note_rep']._database[1][1])
    assert repos['note_rep'].get(2).title == "abc"
    assert repos['note_rep'].get(2).creator == MEMBER


def test_creating_note_permission_errors(repos):
    with pytest.raises(PermissionError):
        CreateNote().execute(actor_id=THIRD_PERSON,
                             title="abc",
                             tasklist_id=TASKLIST_EXISTING,
                             note_rep=repos['note_rep'],
                             group_rep=repos['group_rep'],
                             tasklist_rep=repos['tasklist_rep'])


def test_change_note_title_happy_path(repos):
    ChangeTitleNote().execute(
        note_id=1,
        actor_id=MEMBER,
        title="bebra",
        note_rep=repos['note_rep']
    )

    assert repos['note_rep'].get(1).title == 'bebra'

def test_change_note_title_permission_errors(repos):
    with pytest.raises(PermissionError):
        ChangeTitleNote().execute(
            note_id=1,
            actor_id=SECOND_MEMBER,
            title="bebra",
            note_rep=repos['note_rep']
        )

def test_change_content(repos):
    ChangeContentNote().execute(
        note_id=1,
        actor_id=MEMBER,
        content="bebra",
        note_rep=repos['note_rep']
    )
    assert repos['note_rep'].get(1).content == 'bebra'

