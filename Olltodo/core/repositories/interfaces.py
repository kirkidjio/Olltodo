from abc import ABC, abstractmethod


class IRepository(ABC):
    @abstractmethod
    def get(self, id_):
        pass
        
    def save(self, entity_obj):
        pass
        
    def delete(self, id_):
        pass
        
        
class IRepositoryForTaskAndNotes(ABC):
    @abstractmethod
    def get(self, id_):
        pass
        
    def get_by_tasklist(self, id_):
        pass
        
    def save(self, entity_obj, tasklist_id):
        pass
        
    def delete(self, id_):
        pass
    