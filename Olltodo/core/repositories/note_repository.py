from core.domain.entities import Note
import core.models

class NoteRepository:
    def _mapping(self, orm_note:models.Note):
        Note(
            id_ = orm_note.id
            creator_id = orm_note.creator.id
            title = orm_note.title
            content = orm_note.content
        )
        
    def get_notes_by_tasklist(self, tasklist_id:int) -> list[Note]:
        return [self._mapping(i) for i in models.Note.objects.filter(tasklist=tasklist_id)]
        
    def save(self, entity_note:Note):
        note_orm = None
        if entity_note.id == None:
            note_orm = models.Note()
        else:
            note_orm = models.Note.objects.get(id=entity_note.id)
           
        note_orm.title = entity_note.title
        note_orm.content = entity_note.content
        note_orm.creator = entity_note.creator
        note_orm.save()
    