class TaskList:
    def __init__(self, id_: int, leader_id: int, tasks_id:set[int], notes_id:set[int], title:str):
        self._id = id_
        self._leader_id = leader_id
        self._title = title
        
        
        
    def change_title(self, actor_id:int, new_title:int)
        if actor_id != self._leader_id:
            raise PermissionError
        else: self._title = new_title
        
    @property
    def title(self):
        return self._title
    
