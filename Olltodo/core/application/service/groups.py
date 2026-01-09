from core.domain.entities import Group

class CreateGroup:
    def execute(self, actor_id, name, group_rep):
        new_group = Group(leader_id=actor_id, name=name)
        return group_rep.save(new_group)

class AddNewMemberGroup:
    def execute(self,group_id ,actor_id, new_member, group_rep):
        group = group_rep.get(group_id)
        group.add(actor_id, new_member)
        group_rep.save(group)

class RemoveMemberGroup:
    def execute(self, group_id, actor_id, member, group_rep):
        group = group_rep.get(group_id)
        group.rem(actor_id, member)
        group_rep.save(group)

class ChangeNameGroup:
    def execute(self, group_id, actor_id, name, group_rep):
        group = group_rep.get(group_id)
        group.change_name(actor_id, name)
        group_rep.save(group)
