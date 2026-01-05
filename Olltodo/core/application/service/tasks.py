from core.domain.entities import Task
from core.domain.models.tasklist import TaskList

from .exceptions import TaskListNotFound, NotGroupLeader, PerformerNotInGroup

class CreateTask:
    def execute(self, actor_id, performer_id, title, tasklist_id, task_rep, group_rep, tasklist_rep):
        try: tasklist = tasklist_rep.get(tasklist_id)
        except: raise TaskListNotFound

        group = group_rep.get(tasklist_rep.get(tasklist_id).group_id)

        if group.leader != actor_id: raise NotGroupLeader("Actor no have permission for create task")
        if performer_id not in group.members: raise PerformerNotInGroup

        return task_rep.save(Task(actor_id, performer_id, title), tasklist_id)

