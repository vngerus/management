from abc import ABC, abstractmethod
from typing import List, Optional, Any

class BaseDAO(ABC):
    
    def __init__(self, connection):
        self.connection = connection
    
    @abstractmethod
    def crear(self, dto: Any) -> bool:      
        pass
    
    @abstractmethod
    def obtener_por_id(self, id: int) -> Optional[Any]:
        pass
    
    @abstractmethod
    def obtener_todos(self) -> List[Any]:
        pass
    
    @abstractmethod
    def actualizar(self, dto: Any) -> bool:
        pass
    
    @abstractmethod
    def eliminar(self, id: int) -> bool:
        pass