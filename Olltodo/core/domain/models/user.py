from dataclasses import dataclass

@dataclass(frozen=True)
class User:
    id_:int
    login:str
    first_name:str
    last_name:str
    email:str
    
    
 
    
 
    
