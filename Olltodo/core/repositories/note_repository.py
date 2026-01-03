from core.domain.entities.note import Note
from core import models

class NoteRepository:
    def _mapping(self, orm_note:models.Note):
        return Note(
            id_ = orm_note.id,
            creator_id = orm_note.creator.id,
            title = orm_note.title,
            content = orm_note.content
        )
        
    def get_by_tasklist(self, tasklist_id:int) -> list[Note]:
        return [self._mapping(i) for i in models.Note.objects.filter(tasklist=tasklist_id)]
        
    def save(self, entity_note:Note, tasklist_id:int):
        note_orm = None
        if entity_note.id == None:
            note_orm = models.Note()
            note_orm.tasklist_id = tasklist_id
        else:
            if tasklist_id != None: raise ValueError("You cant change tasklist for note")
            note_orm = models.Note.objects.get(id=entity_note.id)
           
        note_orm.title = entity_note.title
        note_orm.content = entity_note.content
        note_orm.creator_id = entity_note.creator
        note_orm.save()
    