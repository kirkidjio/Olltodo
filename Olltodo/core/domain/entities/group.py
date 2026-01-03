class Group:
    def __init__(self, id_:int, leader_id:int, name:str, members_id:set[int]|None = None):
        self._id = id_
        self._leader = leader_id
        self._members:set[int] = set(members_id) if members_id != None else set()
        self._members.add(leader_id)
        self._name = name
        
        
        
    def add(self, actor:int, new_member:int):
        if actor != self._leader:
            raise PermissionError("Operation not allowed")
        elif new_member in self._members:
            raise ValueError("Member in group now")
        else:
            self._members.add(new_member)
        
        

    def rem(self, actor:int, member:int):
        if actor != self._leader:
            raise PermissionError("Operation not allowed")
        elif member not in self._members:
            raise ValueError("Member not in group now")
        else:
            self._members.remove(member)
        
        
    def change_name(self, actor:int, name:str):
        if actor != self._leader:
            raise PermissionError("Operation not allowed")
        
        else:
            self._name = name
           
    @property
    def members(self):
        return self._members
        
    @property
    def name(self):
        return self._name
        
    @property
    def id(self):
        return self._id
    
    @property
    def leader(self):
        return self._leader