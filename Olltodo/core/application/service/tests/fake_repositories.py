from core.repositories.interfaces import IRepository, IRepositoryForTaskAndNotes
from dataclasses import dataclass
from core.domain.entities.group import Group
from core.domain.models.tasklist import TaskList
from core.domain.entities.task import Task


class FakeGroupRepository(IRepository):

    def __init__(self, entities_groups:list[Group]):
        self._database = entities_groups

    def get(self, id_):
        for i in self._database:
            if i.id == id_: return i
        return None


    def save(self, entity_group):
        for i in range(0,len(self._database)):
            if self._database[i].id == entity_group.id:
                self._database[i] = entity_group
                return

        entity_group.id_ = self._database[-1].id + 1
        self._database.append(entity_group)


    def delete(self, id_):
        pass



class FakeTaskListRepository(IRepository):
    def __init__(self, models_tasklists:list[TaskList]):
        self._database = models_tasklists

    def get(self, id_):
        for i in self._database:
            if i.id_ == id_: return i
        raise ValueError


    def save(self, model_tasklist):
        for i in range(0,len(self._database)):
            if self._database[i].id_ == model_tasklist.id:
                self._database[i] = model_tasklist
                return

        model_tasklist.id_ = self._database[-1].id_ + 1
        self._database.append(model_tasklist)

    def delete(self, id_):
        pass




class FakeTaskRepository(IRepositoryForTaskAndNotes):

    def __init__(self, entities_tasks = []):
        self._database = entities_tasks


    def get(self, id_):
        for i in self._database:
            if i[0].id == id_: return i[0]
        return None

    def get_by_tasklist(self, id_):
        for i in self._database:
            if i[1].id == id_: return i
        return None

    def save(self, entity_task, tasklist_id):
        for i in range(0, len(self._database)):
            if self._database[i][0].id == entity_task.id:
                self._database[i][0] = entity_task
                return entity_task.id

        entity_task.id_ = self._database[-1].id_ + 1 if len(self._database) > 0 else 1
        self._database.append([entity_task, tasklist_id])
        return entity_task.id

    def delete(self, id_):
        pass