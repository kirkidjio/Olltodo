from core.domain.models import TaskList
from core.application.service.exceptions import *
from core.repositories import GroupRepository


class CreateTaskList:
    def execute(self, group_id, actor_id, name, group_rep, tasklist_rep):

        group = group_rep.get(group_id)

        if group.leader != actor_id: raise NotGroupLeader("Actor no have permission for create tasklist")

        return tasklist_rep.save(TaskList(id_=None,name=name,group_id = group_id))