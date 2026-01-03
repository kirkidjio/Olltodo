from core.repositories.interfaces import IRepository
from dataclasses import dataclass

@dataclass
class FakeGroupModelORM:
    id_:int
    leader_id:int
    members_id:set[int]
    name:str
 

class FakeGroupRepository(IRepository):

    def __init__(self):
        self._database = []

    def _mapping(self, group_orm:FakeGroupModelORM) -> Group:
        return Group(
            id_ = group_orm.id_,
            leader_id = group_orm.leader_id,
            name = group_orm.name, 
            members_id = group_orm.members_id
        )
        
    def _get(self, group_id:int) -> Group:
        for i in self._database:
            if i.id_ == group_id: return i
            else: raise ValueError
            
    def get(self, group_id:int) -> Group:
        for i in self._database:
            if i.id_ == group_id: return self._mapping(i)
            else: raise ValueError
        
    
    def save(self, entity_group:Group):
        group_orm = None
        if entity_group.id == None:
            group_orm = FakeGroupModelORM()
            group_orm.id_ = len(self._database) + 1
        else:
            group_orm = self._get(group_id=entity_group.id)
           
        group_orm.leader_id = entity_group.leader
        group_orm.name = entity_group.name
        group_orm.members_id = entity_group.members