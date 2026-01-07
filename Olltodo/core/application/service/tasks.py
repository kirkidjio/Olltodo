from core.domain.entities import Task
from core.domain.models.tasklist import TaskList

from .exceptions import *

class CreateTask:
    def execute(self, actor_id, performer_id, title, tasklist_id, task_rep, group_rep, tasklist_rep):
        try: tasklist = tasklist_rep.get(tasklist_id)
        except: raise TaskListNotFound

        group = group_rep.get(tasklist_rep.get(tasklist_id).group_id)

        if group.leader != actor_id: raise NotGroupLeader("Actor no have permission for create task")
        if performer_id not in group.members: raise PerformerNotInGroup

        return task_rep.save(Task(actor_id, performer_id, title), tasklist_id)


class ChangeTaskStatus:
    def execute(self, task_id, actor_id, action, task_rep):
        task = task_rep.get(task_id)
        commands = {'submit': task.submit, 'reject':task.reject, 'accept':task.accept}
        commands[action](actor_id)
        return task_rep.save(task)

class ChangeTaskPriority:
    def execute(self, actor_id, task_id, priority, task_rep):
        task = task_rep.get(task_id)
        task.change_priority(actor_id, priority)
        task_rep.save(task)


class ChangeTaskTitle:
    def execute(self, actor_id, task_id, title, task_rep):
        task = task_rep.get(task_id)
        task.change_title(actor_id, title)
        task_rep.save(task)

class GetTasksByTasklist:
    def execute(self, tasklist_id, actor_id, tasklist_rep, task_rep, group_rep):
        tasklist = tasklist_rep.get(tasklist_id)
        group = group_rep.get(tasklist.group_id)

        if actor_id not in group.members: raise PermissionError("Actor cant receive tasks because his not in group")
        tasks = task_rep.get_by_tasklist(tasklist_id)

        return [{'id': task.id,
                 'checker':task.checker,
                 'performer':task.performer,
                 'status':task.status,
                 'priority':task.priority,
                 'title':task.title} for task in tasks]

