"""
Archivo __init__.py para el paquete DTO
Facilita la importación de todos los DTOs
"""

from .empleado_dto import EmpleadoDTO
from .departamento_dto import DepartamentoDTO
from .proyecto_dto import ProyectoDTO
from .usuario_dto import UsuarioDTO

__all__ = ['EmpleadoDTO', 'DepartamentoDTO', 'ProyectoDTO', 'UsuarioDTO']