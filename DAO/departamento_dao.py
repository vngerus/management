from typing import List, Optional
from .base_dao import BaseDAO
from DTO.departamento_dto import DepartamentoDTO

class DepartamentoDAO(BaseDAO):

    
    def crear(self, departamento_dto: DepartamentoDTO) -> bool:
        """Crea un nuevo departamento en la base de datos"""
        try:
            with self.connection.cursor() as cursor:
                sql = "INSERT INTO departamentos (nombre, gerente) VALUES (%s, %s)"
                cursor.execute(sql, (departamento_dto.nombre, departamento_dto.gerente))
                return True
        except Exception as e:
            print(f"Error al crear departamento: {e}")
            return False
    
    def obtener_por_id(self, id: int) -> Optional[DepartamentoDTO]:
        """Obtiene un departamento por su ID"""
        try:
            with self.connection.cursor() as cursor:
                sql = "SELECT * FROM departamentos WHERE id = %s"
                cursor.execute(sql, (id,))
                result = cursor.fetchone()
                
                if result:
                    return DepartamentoDTO.from_dict(result)
                return None
        except Exception as e:
            print(f"Error al obtener departamento: {e}")
            return None
    
    def obtener_todos(self) -> List[DepartamentoDTO]:
        """Obtiene todos los departamentos"""
        departamentos = []
        try:
            with self.connection.cursor() as cursor:
                sql = "SELECT * FROM departamentos"
                cursor.execute(sql)
                results = cursor.fetchall()
                
                for result in results:
                    departamento_dto = DepartamentoDTO.from_dict(result)
                    departamentos.append(departamento_dto)
        except Exception as e:
            print(f"Error al obtener departamentos: {e}")
        
        return departamentos
    
    def actualizar(self, departamento_dto: DepartamentoDTO) -> bool:
        """Actualiza un departamento existente"""
        try:
            with self.connection.cursor() as cursor:
                sql = "UPDATE departamentos SET nombre = %s, gerente = %s WHERE id = %s"
                cursor.execute(sql, (
                    departamento_dto.nombre,
                    departamento_dto.gerente,
                    departamento_dto.id
                ))
                return True
        except Exception as e:
            print(f"Error al actualizar departamento: {e}")
            return False
    
    def eliminar(self, id: int) -> bool:
        """Elimina un departamento por su ID"""
        try:
            with self.connection.cursor() as cursor:
                sql = "DELETE FROM departamentos WHERE id = %s"
                cursor.execute(sql, (id,))
                return True
        except Exception as e:
            print(f"Error al eliminar departamento: {e}")
            return False