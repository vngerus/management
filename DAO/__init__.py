"""
Archivo __init__.py para el paquete DAO
Facilita la importación de todos los DAOs
"""

from .database import Database
from .base_dao import BaseDAO
from .empleado_dao import EmpleadoDAO
from .departamento_dao import DepartamentoDAO
from .proyecto_dao import ProyectoDAO
from .usuario_dao import UsuarioDAO

__all__ = ['Database', 'BaseDAO', 'EmpleadoDAO', 'DepartamentoDAO', 'ProyectoDAO', 'UsuarioDAO']