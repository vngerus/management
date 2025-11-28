from typing import Optional

class DepartamentoDTO:    
    def __init__(self, id: Optional[int] = None, nombre: str = "", gerente: str = ""):
        self.id = id
        self.nombre = nombre
        self.gerente = gerente
        
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'nombre': self.nombre,
            'gerente': self.gerente
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data.get('id'),
            nombre=data.get('nombre', ''),
            gerente=data.get('gerente', '')
        )
    
    def __str__(self) -> str:
        return f"DepartamentoDTO(id={self.id}, nombre='{self.nombre}', gerente='{self.gerente}')"