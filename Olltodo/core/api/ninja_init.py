from ninja import NinjaAPI
from ninja.security import django_auth
from ninja import Schema
from typing import List

api = NinjaAPI(auth=django_auth)

from core.application.service.tasks import *
from core.repositories import *


class TaskOut(Schema):
    id: int
    checker: int
    performer: int
    status: str
    priority: int
    title: str


@api.get('/tasklist/{tasklist_id}', response=List[TaskOut])
def get_tasks_by_tasklist(request, tasklist_id):
    tasks = GetTasksByTasklist().execute(tasklist_id=tasklist_id,
                                         actor_id=request.user.id,
                                         task_rep=TaskRepository(),
                                         group_rep=GroupRepository(),
                                         tasklist_rep=TaskListRepository()
                                         )
    return tasks



@api.get('/tasklist/{tasklist_id}/performer/{performer_id}', response=List[TaskOut])
def get_tasks_by_performer_in_tasklist(request, tasklist_id, performer_id):
    tasks = GetTasksByPerformer().execute(tasklist_id=tasklist_id,
                                          performer_id=performer_id,
                                         actor_id=request.user.id,
                                         task_rep=TaskRepository(),
                                         group_rep=GroupRepository(),
                                         tasklist_rep=TaskListRepository())
    return tasks

@api.patch('/task/{task_id}/{action}')
def change_task_status(request, task_id, action):
    ChangeTaskStatus().execute(task_id=task_id,
                               actor_id=request.user.id,
                               action=action,
                               task_rep=TaskRepository())

@api.post('tasklist/{}/create/task')
def create_task(request)