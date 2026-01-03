from core.domain.models.tasklist import TaskList
from core import models
from django.contrib.auth.models import User

class TaskListRepository:
    def _mapping(self, tasklist_orm:models.TaskList) -> TaskList:
        return TaskList(
            id_ = tasklist_orm.id,
            name = tasklist_orm.name,
            group_id = tasklist_orm.group_id
        )
        
    def get(self, tasklist_id:int) -> TaskList:
        return self._mapping(models.TaskList.objects.get(id=tasklist_id))
        
    
    def save(self, model_tasklist:TaskList, group_id:int):
        
        tasklist_orm = models.TaskList()   
        tasklist_orm.group_id = model_tasklist.group_id
        tasklist_orm.name = model_tasklist.name
        
        tasklist_orm.save()
    
        


