from core import models
from core.domain.entities.task import Task, TaskStatus, TaskPriority

class TaskRepository:
        
    def _mapping(self, orm_task:models.Task):
        return Task(
            id_ = orm_task.id,
            checker_id = orm_task.tasklist.group.leader.id,
            performer_id = orm_task.performer.id,
            status = TaskStatus(orm_task.status),
            priority = TaskPriority(orm_task.priority),
            title = orm_task.title,
        )
        
   
        
    def get_by_tasklist(self, tasklist_id) -> list[Task]:
        obj = models.Task.objects.filter(tasklist=tasklist_id)
        return [self._mapping(i) for i in obj]
    
    def save(self, task:Task, tasklist_id:int = None):
        orm_task = None
        if task.id == None:
            orm_task = models.Task()
            orm_task.tasklist_id = tasklist_id
        else:
            if tasklist_id != None: raise PermissionError("You cant change tasklist for task")
            orm_task = models.Task.get(id=task.id)
        
        orm_task.performer_id = task.performer
        orm_task.title = task.title
        orm_task.status = task.status
        orm_task.priority = task.priority

        orm_task.save()