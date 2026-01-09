from core.domain.entities import Task, Note

class Tasklist:
    def __init__(self, name, id_=None, tasks:list[Task]=None, notes:list[Note]=None):
        self._name = name
        self._id = id_
        self._tasks = tasks if tasks is not None else []
        self._notes = notes if notes is not None else []

    def create_task(self, title, checker, performer):
        self._tasks.append(Task(checker_id=checker, performer_id=performer, title=title))

    def remove_task(self, id_):
        for i in self._tasks:
            if i.id == id_: self._tasks.remove(i)

    def create_note(self, title, creator):
        self._notes.append(Note(creator_id=creator, title=title))

    def remove_note(self, id_):
        for i in self._notes:
            if i.id == id_: self._notes.remove(i)
