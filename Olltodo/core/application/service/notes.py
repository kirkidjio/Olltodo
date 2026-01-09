from core.domain.entities import Note

class CreateNote:
    def execute(self, actor_id, title, tasklist_id, note_rep, group_rep, tasklist_rep):
        tasklist = tasklist_rep.get(tasklist_id)
        group = group_rep.get(tasklist.group_id)

        if actor_id not in group.members: raise PermissionError(f"User cant create note for this group")

        note = Note(creator_id=actor_id, title=title)
        return note_rep.save(note, tasklist_id)

class ChangeTitleNote:
    def execute(self, note_id, actor_id, title, note_rep):
        note = note_rep.get(note_id)
        note.change_title(actor_id, title)
        note_rep.save(note)

class ChangeContentNote:
    def execute(self, note_id, actor_id, content, note_rep):
        note = note_rep.get(note_id)
        note.change_content(actor_id, content)
        note_rep.save(note)

class GetNotesByTasklist:
    def execute(self, tasklist_id, actor_id, tasklist_rep, note_rep, group_rep):
        tasklist = tasklist_rep.get(tasklist_id)
        group = group_rep.get(tasklist.group_id)

        if actor_id not in group.members: raise PermissionError("Actor cant receive tasks because his not in group")
        notes = note_rep.get_by_tasklist(tasklist_id)

        return [{'id': note.id,
                 'creator':note.creator,
                 'title':note.title,
                 'content':note.content} for note in notes]

class GetNotesByPerformer:
    def execute(self, tasklist_id,performer_id ,actor_id, tasklist_rep, note_rep, group_rep):
        tasklist = tasklist_rep.get(tasklist_id)
        group = group_rep.get(tasklist.group_id)

        if actor_id not in group.members: raise PermissionError("Actor cant receive tasks because his not in group")
        notes = note_rep.get_in_tasklist_by_performer(tasklist_id, performer_id)

        return [{'id': note.id,
                 'creator':note.creator,
                 'title':note.title,
                 'content':note.content} for note in notes]