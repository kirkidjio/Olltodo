from core import models
from core.domain.entities.group import Group
from core.repositories.interfaces import IRepository

class GroupRepository(IRepository):
    def _mapping(self, group_orm:models.Group) -> Group:
        return Group(
            id_ = group_orm.id,
            leader_id = group_orm.leader_id,
            name = group_orm.name, 
            members_id = set(group_orm.members.all())
        )
        
    def get(self, group_id:int) -> Group:
        return self._mapping(models.Group.objects.get(id=group_id))
        
    
    def save(self, entity_group:Group):
        group_orm = None
        if entity_group.id == None:
            group_orm = models.Group()
        else:
            group_orm = models.Group.objects.get(id=entity_group.id)
           
        group_orm.leader_id = entity_group.leader
        group_orm.name = entity_group.name
        group_orm.save()
        group_orm.members.set(entity_group.members)
        
    