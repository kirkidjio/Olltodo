from dataclasses import dataclass

@dataclass(frozen=True)
class User:
    id_:int
    login:str
    
