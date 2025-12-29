from dataclasses import dataclass

@dataclass
class TaskList:
    id_:int
    title:str
    tasks_id:set[int]
    
