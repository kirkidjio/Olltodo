from core import models
from core.domain.entities.task import Task, TaskStatus, TaskPriority
from core.repositories.interfaces import IRepositoryForTaskAndNotes

class TaskRepository(IRepositoryForTaskAndNotes):

    @staticmethod
    def _mapping(orm_task:models.Task):
        return Task(
            id_ = orm_task.id,
            checker_id = orm_task.tasklist.group.leader.id,
            performer_id = orm_task.performer.id,
            status = TaskStatus(orm_task.status),
            priority = TaskPriority(orm_task.priority),
            title = orm_task.title,
        )
        
    def get(self, task_id):
        return self._mapping(models.Task.objects.get(id=task_id))
    
        
    def get_by_tasklist(self, tasklist_id) -> list[Task]:
        obj = models.Task.objects.filter(tasklist=tasklist_id)
        return [self._mapping(i) for i in obj]


    def get_in_tasklist_by_performer(self, performer_id, tasklist_id):
        obj = models.Task.objects.filter(performer_id=performer_id, tasklist_id=tasklist_id)
        return [self._mapping(i) for i in obj]

    def save(self, task:Task, tasklist_id:int = None):
        orm_task = None
        if task.id is None and tasklist_id is not None:
            orm_task = models.Task()
            orm_task.tasklist_id = tasklist_id
        else:
            orm_task = models.Task.objects.get(id=task.id)
        
        orm_task.performer_id = task.performer
        orm_task.title = task.title
        orm_task.status = task.status
        orm_task.priority = task.priority

        orm_task.save()
        
        
    def delete(self, task_id):
        pass