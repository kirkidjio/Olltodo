from core import models
from core.domain.entities.group import Group
from core.domain.entities.note import Note
from core.domain.models.tasklist import TaskList
from core.repositories.note_repository import NoteRepository
from django.contrib.auth.models import User



def test_can_add_and_get_note(db):
    
    user = User.objects.create(username="u")
    
    group = models.Group.objects.create(name="gh", leader=user)
    group.members.add(user)
    
    tasklist = models.TaskList.objects.create(name="Juniors Frontend", group=group)
    
    rep = NoteRepository()
    
    note = Note(id_=None, creator_id=user.id, title="I dont know how to fix this just look", content="bebra bebra bebra")
    
    rep.save(note, tasklist.id)
    note_from_rep = rep.get_by_tasklist(1)
    
    assert note_from_rep[-1].title == note.title
    assert note_from_rep[-1].content == note.content