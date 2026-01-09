from dataclasses import dataclass

@dataclass
class TaskList:
    id_:int|None
    name:str
    group_id:int
    
