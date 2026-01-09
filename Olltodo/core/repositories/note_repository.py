from core.domain.entities.note import Note
from core import models
from core.repositories.interfaces import IRepositoryForTaskAndNotes

class NoteRepository(IRepositoryForTaskAndNotes):
    @staticmethod
    def _mapping(orm_note:models.Note):
        return Note(
            id_ = orm_note.id,
            creator_id = orm_note.creator.id,
            title = orm_note.title,
            content = orm_note.content
        )
        
    def get_by_tasklist(self, tasklist_id:int) -> list[Note]:
        return [self._mapping(i) for i in models.Note.objects.filter(tasklist=tasklist_id)]
        
    def get(self, note_id):
        return self._mapping(models.Note.objects.get(id=note_id))

    def get_in_tasklist_by_performer(self, performer_id, tasklist_id):
        obj = models.Note.objects.filter(performer_id=performer_id, tasklist_id=tasklist_id)
        return [self._mapping(i) for i in obj]

    def save(self, entity_note:Note, tasklist_id:int = None):
        note_orm = None
        if entity_note.id is None and tasklist_id is not None:
            note_orm = models.Note()
            note_orm.tasklist_id = tasklist_id
        else:
            note_orm = models.Note.objects.get(id=entity_note.id)
           
        note_orm.title = entity_note.title
        note_orm.content = entity_note.content
        note_orm.creator_id = entity_note.creator
        note_orm.save()
        return note_orm.id
        
    def delete(self, note_id):
        pass
    