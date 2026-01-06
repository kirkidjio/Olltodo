from enum import Enum, StrEnum, IntEnum

class TaskStatus(StrEnum):
    OPEN = "open"
    SUBMITTED = "submitted"
    ACCEPTED = "accepted"
    REJECTED = "rejected"

   
class TaskPriority(IntEnum):
    HIGH = 3
    MEDIUM = 2
    LOW = 1
    NONE = 0



class Task:
    def __init__(self, checker_id:int, performer_id:int, title:str, id_:int = None, status = TaskStatus.OPEN, priority=TaskPriority.NONE):
        self._id : int = id_
        self._title = title
        self._checker_id = checker_id
        self._performer_id = performer_id
        self._status = status
        self._priority = priority
        
    def __gt__(self, other):
        return self._priority > other._priority
        
        
    def submit(self, performer):
        if performer != self._performer_id: raise PermissionError("Only performer can submit his task")
        elif self._status not in [TaskStatus.OPEN, TaskStatus.REJECTED]: raise ValueError("Task cant do this operation having his status")
        else: self._status = TaskStatus.SUBMITTED
        
    def accept(self, leader):
        if leader != self._checker_id: raise PermissionError("Only leader can accept task")
        elif self._status != TaskStatus.SUBMITTED: raise ValueError("Task cant do this operation having his status")
        else: self._status = TaskStatus.ACCEPTED
        
    def reject(self, leader):
        if leader != self._checker_id: raise PermissionError("Only leader can reject task")
        elif self._status != TaskStatus.SUBMITTED: raise ValueError("Task cant do this operation having his status")
        else: self._status = TaskStatus.REJECTED
        
    def change_title(self, leader, new_title:str):
        if leader != self._checker_id: raise PermissionError("Only leader can change title")
        else:
            self._title = new_title
        
    def change_priority(self, leader, new_priority:TaskPriority):
        if leader != self._checker_id: raise PermissionError("Only leader can change priority")
        elif self._status == TaskStatus.ACCEPTED: raise PermissionError("You cant change priority in accepted tasks")
        else: self._priority = new_priority
        
    @property    
    def title(self):
        return self._title
        
    @property
    def checker(self):
        return self._checker_id
        
    @property
    def performer(self):
        return self._performer_id
        
    @property
    def status(self):
        return self._status.value
        
    @property
    def priority(self):
        return self._priority
    
    @property
    def id(self):
        return self._id
   
