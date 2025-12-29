from enum import Enum

class TaskStatus(Enum):
    OPEN = "open"
    SUBMITTED = "submitted"
    ACCEPTED = "accepted"
    REJECTED = "rejected"

   
class TaskPriority(Enum):
    HIGH = 3
    MEDIUM = 2
    LOW = 1
    NONE = 0



class Task:
    def __init__(self, checker:int, performer_id:int, title:str, id_:int = None):
        self.id : int = id_
        self._title = title
        self._checker = checker
        self._performer = performer_id
        self._status:TaskStatus = TaskStatus.OPEN
        self._priority:TaskPriority = TaskPriority.NONE
        
    def __gt__(self, other):
        return self._priority.value > other._priority.value
        
    def submit(self, performer:User):
        if performer != self._performer: raise PermissionError("Only performer can submit his task")
        elif self._status not in [TaskStatus.OPEN, TaskStatus.REJECTED]: raise ValueError("Task cant do this operation having his status")
        else: self._status = TaskStatus.SUBMITTED
        
    def accept(self, leader:User):
        if leader != self._checker: raise PermissionError("Only leader can accept task")
        elif self._status != TaskStatus.SUBMITTED: raise ValueError("Task cant do this operation having his status")
        else: self._status = TaskStatus.ACCEPTED
        
    def reject(self, leader:User):
        if leader != self._checker: raise PermissionError("Only leader can reject task")
        elif self._status != TaskStatus.SUBMITTED: raise ValueError("Task cant do this operation having his status")
        else: self._status = TaskStatus.REJECTED
        
    def change_title(self, leader:User, new_title:str):
        if leader != self._checker: raise PermissionError("Only leader can change title")
        else:
            self._title = new_title
        
    def change_priority(self, leader:User, new_priority:TaskPriority):
        if leader != self._checker: raise PermissionError("Only leader can change priority")
        elif self._status == TaskStatus.ACCEPTED: raise PermissionError("You cant change priority in accepted tasks")
        else: self._priority = new_priority
        
    @property    
    def title():
        return self._title
        
    @property
    def performer():
        return self._performer_id
        
    @property
    def status():
        return self._status.value
        
    @property
    def priority():
        return self._priority.value
    
    @property
    def id():
        return self._id
   
