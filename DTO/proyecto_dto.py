from datetime import date
from typing import Optional

class ProyectoDTO:
    def __init__(self, id: Optional[int] = None, nombre: str = "", 
                 descripcion: str = "", fecha_inicio: Optional[date] = None):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.fecha_inicio = fecha_inicio
        
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'fecha_inicio': self.fecha_inicio
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data.get('id'),
            nombre=data.get('nombre', ''),
            descripcion=data.get('descripcion', ''),
            fecha_inicio=data.get('fecha_inicio')
        )
    
    def __str__(self) -> str:
        return f"ProyectoDTO(id={self.id}, nombre='{self.nombre}', fecha_inicio={self.fecha_inicio})"