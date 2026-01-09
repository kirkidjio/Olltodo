from ninja import NinjaAPI
from ninja.security import django_auth
from ninja import Schema
from typing import List
from ninja.responses import Response

from core.application.service.groups import *
from core.application.service.notes import *
from core.application.service.tasklist import *

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

class TaskCreateIn(Schema):
    title:str
    performer:int
    priority:int

class TaskCreateOut(Schema):
    task_id:int

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

@api.post('tasklist/{tasklist_id}/create/task')
def create_task(request, tasklist_id, data:TaskCreateIn):

    task_id = CreateTask().execute(actor_id=request.user.id,
                         performer_id = data.performer,
                         title=data.title,
                         tasklist_id=tasklist_id,
                         task_rep=TaskRepository(),
                         group_rep=GroupRepository(),
                         tasklist_rep=TaskListRepository())

    print(data.title)
    print(data.performer)
    return Response({'task_id':task_id}, status=201)


class ChangeTaskPriorityIn(Schema):
    priority:int

@api.post('task/{task_id}/change/priority')
def change_task_priority(request, task_id, data:ChangeTaskPriorityIn):
    ChangeTaskPriority().execute(actor_id=request.user.id,
                                 task_id=task_id,
                                 priority=data.priority,
                                 task_rep=TaskRepository())

    return 201

class ChangeTaskTitleIn(Schema):
    title:str

@api.post('task/{task_id}/change/title')
def change_task_title(request, task_id, data:ChangeTaskTitleIn):
    ChangeTaskTitle().execute(actor_id=request.user.id, task_id=task_id, title=data.title, task_rep=TaskRepository())


class CreateGroupIn(Schema):
    name:str

@api.post('group/create')
def create_group(request, data:CreateGroupIn):
    new_group=CreateGroup().execute(actor_id=request.user.id, name=data.name, group_rep=GroupRepository())

    return Response({'group_id':new_group})

@api.post('group/{group_id}/add/{member_id}')
def group_add_new_member(request, group_id, member_id):
    AddNewMemberGroup().execute(group_id=group_id,
                                actor_id=request.user.id,
                                new_member=member_id,
                                group_rep=GroupRepository())


@api.post('group/{group_id}/kick/{member_id}')
def group_add_rem_member(request, group_id:int, member_id:int):
    RemoveMemberGroup().execute(group_id=group_id,
                                actor_id=request.user.id,
                                member=member_id,
                                group_rep=GroupRepository())

class NewNameIn(Schema):
    name : str

@api.post('group/{group_id}/change_name/')
def group_change_name(request, group_id:int, data:NewNameIn):
    ChangeNameGroup().execute(group_id=group_id, actor_id=request.user.id, name=data.name, group_rep=GroupRepository())


class NoteCreateIn(Schema):
    title:str

@api.post('tasklist/{tasklist_id}/create/note')
def create_note(request, tasklist_id, data:NoteCreateIn):
    new_note = CreateNote().execute(actor_id=request.user.id,
                         title=data.title,
                         tasklist_id=tasklist_id,
                         note_rep=NoteRepository(),
                         group_rep=GroupRepository(),
                         tasklist_rep=TaskListRepository())

    return Response({'note_id':new_note}, status=201)

@api.post('note/{note_id}/change/title')
def change_title_note(request, note_id, data:NoteCreateIn):
    ChangeTitleNote().execute(note_id=1,
        actor_id=request.user.id,
        title=data.title,
        note_rep=NoteRepository())

class NotesOut(Schema):
    id:int
    creator:int
    title:str
    content:str

@api.get('tasklist/{tasklist_id}/performer/{performer_id}', response=list[NotesOut])
def get_notes_by_performer(request, tasklist_id, performer_id):
     notes = GetNotesByPerformer().execute(tasklist_id = tasklist_id,
                                  performer_id=performer_id,
                                  actor_id=request.user.id,
                                  tasklist_rep=TaskListRepository(),
                                  note_rep=NoteRepository(),
                                  group_rep=GroupRepository())

     return notes

class CreateTaskListIn(Schema):
    name:str

@api.post('group/{group_id}/create/tasklist')
def create_tasklist(request, group_id, data:CreateTaskListIn):
    new_tasklist = CreateTaskList().execute(group_id=group_id,
                             actor_id=request.user.id,
                             name=data.name,
                             group_rep=GroupRepository(),
                             tasklist_rep=TaskListRepository())

    return Response({'tasklist_id':new_tasklist})