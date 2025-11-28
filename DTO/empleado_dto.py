from datetime import date
from typing import Optional

class EmpleadoDTO:
    def __init__(self, id: Optional[int] = None, nombre: str = "", email: str = "", 
                 direccion: str = "", telefono: str = "", salario: float = 0.0, 
                 inicio_contrato: Optional[date] = None, departamento_id: Optional[int] = None):
        self.id = id
        self.nombre = nombre
        self.email = email
        self.direccion = direccion  
        self.telefono = telefono    
        self.salario = salario
        self.inicio_contrato = inicio_contrato
        self.departamento_id = departamento_id
        
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'nombre': self.nombre,
            'email': self.email,
            'direccion': self.direccion,
            'telefono': self.telefono,
            'salario': self.salario,
            'inicio_contrato': self.inicio_contrato,
            'departamento_id': self.departamento_id
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data.get('id'),
            nombre=data.get('nombre', ''),
            email=data.get('email', ''),
            direccion=data.get('direccion', ''),
            telefono=data.get('telefono', ''),
            salario=data.get('salario', 0.0),
            inicio_contrato=data.get('inicio_contrato'),
            departamento_id=data.get('departamento_id')
        )
    
    def __str__(self) -> str:
        return f"EmpleadoDTO(id={self.id}, nombre='{self.nombre}', email='{self.email}')"