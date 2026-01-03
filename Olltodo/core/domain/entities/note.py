from dataclasses import dataclass


class Note:
    def __init__(self, creator_id:int, title:str, content:str = None, id_:int = None):
        self._id = id_
        self._creator_id = creator_id
        self._title = title
        self._content = content
        
    def change_title(self, actor_id:int, new_title:str):
        if actor != self._creator_id:
            raise PermissionError
        else:
            self._title = new_title
            
    def change_content(self, actor_id:int, new_content:str):
        if actor != self._creator_id:
            raise PermissionError
        else:
            self._content = new_content

    @property
    def title(self):
        return self._title
    
    @property
    def content(self):
        return self._content
    
    @property
    def creator(self):
        return self._creator_id
        
    @property
    def id(self):
        return self._id