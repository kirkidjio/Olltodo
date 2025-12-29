from core import models
from core.domain.entities.task import Task, TaskStatus, TaskPriority

class TaskRepository:
        
    def _mapping(self, orm_task:model.Task):
        return Task(
            id_ = orm_task.id
            checker = orm_task.tasklist.group.leader.id
            performer = orm_task.performer.id
            status = TaskStatus(orm_task.status)
            priority = TaskPriority(orm_task.priority)
            title = orm_task.title
        )
        
   
        
    def get_by_tasklist(self, tasklist_id) -> list[Task]:
        obj = model.Task.objects.filter(tasklist=tasklist_id, flat=True)
        return [self._mapping(i) for i in obj]
    
    def save(self, task:Task, tasklist_id:int):
        orm_task = None
        if task.id == None:
            orm_task = model.Task()
            orm_task.tasklist = tasklist_id
        else:
            orm_task = model.Task.get(id=task.id)
        
        orm_task.performer = task.performer
        orm_task.title = task.title
        orm_task.status = task.status.value
        orm_task.priority = task.priority.value

        orm_task.save()