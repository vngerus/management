
from typing import List, Optional
from .base_dao import BaseDAO
from DTO.proyecto_dto import ProyectoDTO

class ProyectoDAO(BaseDAO):
    def crear(self, proyecto_dto: ProyectoDTO) -> bool:
        try:
            with self.connection.cursor() as cursor:
                sql = "INSERT INTO proyectos (nombre, descripcion, fecha_inicio) VALUES (%s, %s, %s)"
                fecha = proyecto_dto.fecha_inicio if proyecto_dto.fecha_inicio else "NOW()"
                cursor.execute(sql, (proyecto_dto.nombre, proyecto_dto.descripcion, fecha))
                return True
        except Exception as e:
            print(f"Error al crear proyecto: {e}")
            return False
    
    def obtener_por_id(self, id: int) -> Optional[ProyectoDTO]:
        try:
            with self.connection.cursor() as cursor:
                sql = "SELECT * FROM proyectos WHERE id = %s"
                cursor.execute(sql, (id,))
                result = cursor.fetchone()
                
                if result:
                    return ProyectoDTO.from_dict(result)
                return None
        except Exception as e:
            print(f"Error al obtener proyecto: {e}")
            return None
    
    def obtener_todos(self) -> List[ProyectoDTO]:
        proyectos = []
        try:
            with self.connection.cursor() as cursor:
                sql = "SELECT * FROM proyectos"
                cursor.execute(sql)
                results = cursor.fetchall()
                
                for result in results:
                    proyecto_dto = ProyectoDTO.from_dict(result)
                    proyectos.append(proyecto_dto)
        except Exception as e:
            print(f"Error al obtener proyectos: {e}")
        
        return proyectos
    
    def actualizar(self, proyecto_dto: ProyectoDTO) -> bool:
        try:
            with self.connection.cursor() as cursor:
                sql = "UPDATE proyectos SET nombre = %s, descripcion = %s WHERE id = %s"
                cursor.execute(sql, (
                    proyecto_dto.nombre,
                    proyecto_dto.descripcion,
                    proyecto_dto.id
                ))
                return True
        except Exception as e:
            print(f"Error al actualizar proyecto: {e}")
            return False
        except Exception as e:
            print(f"Error al actualizar proyecto: {e}")
            return False
    
    def eliminar(self, id: int) -> bool:
        try:
            with self.connection.cursor() as cursor:
                sql = "DELETE FROM proyectos WHERE id = %s"
                cursor.execute(sql, (id,))
                return True
        except Exception as e:
            print(f"Error al eliminar proyecto: {e}")
            return False
    
    def asignar_empleado(self, empleado_id: int, proyecto_id: int) -> bool:
        try:
            with self.connection.cursor() as cursor:
                sql = "INSERT INTO empleado_proyecto (empleado_id, proyecto_id) VALUES (%s, %s)"
                cursor.execute(sql, (empleado_id, proyecto_id))
                return True
        except Exception as e:
            print(f"Error al asignar empleado a proyecto: {e}")
            return False
    
    def registrar_tiempo(self, empleado_id: int, proyecto_id: int, horas: float, descripcion: str) -> bool:
        try:
            with self.connection.cursor() as cursor:
                sql = """INSERT INTO registro_tiempo (empleado_id, proyecto_id, fecha, horas, descripcion) 
                        VALUES (%s, %s, NOW(), %s, %s)"""
                cursor.execute(sql, (empleado_id, proyecto_id, horas, descripcion))
                return True
        except Exception as e:
            print(f"Error al registrar tiempo: {e}")
            return False
    
    def obtener_reporte_tiempos(self) -> List[dict]:
        try:
            with self.connection.cursor() as cursor:
                sql = """
                SELECT rt.fecha, e.nombre as empleado, p.nombre as proyecto, rt.horas, rt.descripcion 
                FROM registro_tiempo rt
                JOIN empleados e ON rt.empleado_id = e.id
                JOIN proyectos p ON rt.proyecto_id = p.id
                ORDER BY rt.fecha DESC
                """
                cursor.execute(sql)
                return cursor.fetchall()
        except Exception as e:
            print(f"Error al obtener reporte de tiempos: {e}")
            return []