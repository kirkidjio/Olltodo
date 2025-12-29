import core.models
from core.domain.entites.group import Group

class GroupRepository:
    def _mapping(self, group_orm:models.Group) -> Group:
        return Group(
            id_ = group_orm.id,
            leader_id = group_orm.leader.id,
            name = group_orm.name, 
            members_id = set(group.members.all(flat=True))
        )
        
    def get(self, group_id):int:
        return self._mapping(model.Group.objects.get(id=group_id))
        
    
    def save(self, entity_group:Group):
        group_orm = None
        if entity_group.id == None:
            group_orm = models.Group()
        else:
            group_orm = models.Group.objects.get(id=entity_group.id)
           
        group_orm.leader = entity_group.leader
        group_orm.members.add(i for i in entity_group.members)
        group_orm.name = entity_group.name
        group_orm.save()
    