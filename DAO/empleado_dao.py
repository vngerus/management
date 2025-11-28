from typing import List, Optional
from .base_dao import BaseDAO
from DTO.empleado_dto import EmpleadoDTO
from utils.utils import encriptar_dato, desencriptar_dato

class EmpleadoDAO(BaseDAO):
    def crear(self, empleado_dto: EmpleadoDTO) -> bool:
        try:
            direccion_enc = encriptar_dato(empleado_dto.direccion) if empleado_dto.direccion else None
            telefono_enc = encriptar_dato(empleado_dto.telefono) if empleado_dto.telefono else None
            
            with self.connection.cursor() as cursor:
                sql = """INSERT INTO empleados (nombre, email, direccion_enc, telefono_enc, 
                        inicio_contrato, salario, departamento_id) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s)"""
                
                cursor.execute(sql, (
                    empleado_dto.nombre,
                    empleado_dto.email,
                    direccion_enc,
                    telefono_enc,
                    empleado_dto.inicio_contrato,
                    empleado_dto.salario,
                    empleado_dto.departamento_id
                ))
                return True
        except Exception as e:
            print(f"Error al crear empleado: {e}")
            return False
    
    def obtener_por_id(self, id: int) -> Optional[EmpleadoDTO]:
        """Obtiene un empleado por su ID"""
        try:
            with self.connection.cursor() as cursor:
                sql = "SELECT * FROM empleados WHERE id = %s"
                cursor.execute(sql, (id,))
                result = cursor.fetchone()
                
                if result:
                    return self._convertir_a_dto(result)
                return None
        except Exception as e:
            print(f"Error al obtener empleado: {e}")
            return None
    
    def obtener_todos(self) -> List[EmpleadoDTO]:
        """Obtiene todos los empleados"""
        empleados = []
        try:
            with self.connection.cursor() as cursor:
                sql = "SELECT * FROM empleados"
                cursor.execute(sql)
                results = cursor.fetchall()
                
                for result in results:
                    empleado_dto = self._convertir_a_dto(result)
                    if empleado_dto:
                        empleados.append(empleado_dto)
        except Exception as e:
            print(f"Error al obtener empleados: {e}")
        
        return empleados
    
    def obtener_con_departamento(self) -> List[dict]:
        """Obtiene empleados con información del departamento"""
        try:
            with self.connection.cursor() as cursor:
                sql = """SELECT e.id, e.nombre, e.email, e.salario, 
                        d.nombre as departamento_nombre
                        FROM empleados e 
                        LEFT JOIN departamentos d ON e.departamento_id = d.id"""
                cursor.execute(sql)
                return cursor.fetchall()
        except Exception as e:
            print(f"Error al obtener empleados con departamento: {e}")
            return []
    
    def actualizar(self, empleado_dto: EmpleadoDTO) -> bool:
        """Actualiza un empleado existente"""
        try:
            # Encriptar datos sensibles si están presentes
            direccion_enc = encriptar_dato(empleado_dto.direccion) if empleado_dto.direccion else None
            telefono_enc = encriptar_dato(empleado_dto.telefono) if empleado_dto.telefono else None
            
            with self.connection.cursor() as cursor:
                sql = """UPDATE empleados SET nombre = %s, email = %s, 
                        direccion_enc = %s, telefono_enc = %s, salario = %s, 
                        departamento_id = %s WHERE id = %s"""
                
                cursor.execute(sql, (
                    empleado_dto.nombre,
                    empleado_dto.email,
                    direccion_enc,
                    telefono_enc,
                    empleado_dto.salario,
                    empleado_dto.departamento_id,
                    empleado_dto.id
                ))
                return True
        except Exception as e:
            print(f"Error al actualizar empleado: {e}")
            return False
    
    def asignar_departamento(self, empleado_id: int, departamento_id: int) -> bool:
        """Asigna un empleado a un departamento"""
        try:
            with self.connection.cursor() as cursor:
                sql = "UPDATE empleados SET departamento_id = %s WHERE id = %s"
                cursor.execute(sql, (departamento_id, empleado_id))
                return True
        except Exception as e:
            print(f"Error al asignar departamento: {e}")
            return False
    
    def eliminar(self, id: int) -> bool:
        """Elimina un empleado por su ID"""
        try:
            with self.connection.cursor() as cursor:
                sql = "DELETE FROM empleados WHERE id = %s"
                cursor.execute(sql, (id,))
                return True
        except Exception as e:
            print(f"Error al eliminar empleado: {e}")
            return False
    
    def _convertir_a_dto(self, db_record: dict) -> Optional[EmpleadoDTO]:
        """Convierte un registro de BD a EmpleadoDTO"""
        try:
            # Desencriptar datos sensibles
            direccion = desencriptar_dato(db_record.get('direccion_enc')) if db_record.get('direccion_enc') else ""
            telefono = desencriptar_dato(db_record.get('telefono_enc')) if db_record.get('telefono_enc') else ""
            
            return EmpleadoDTO(
                id=db_record['id'],
                nombre=db_record['nombre'],
                email=db_record['email'],
                direccion=direccion,
                telefono=telefono,
                salario=float(db_record['salario']) if db_record.get('salario') else 0.0,
                inicio_contrato=db_record.get('inicio_contrato'),
                departamento_id=db_record.get('departamento_id')
            )
        except Exception as e:
            print(f"Error al convertir registro a DTO: {e}")
            return None