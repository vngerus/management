from typing import List, Optional
from .base_dao import BaseDAO
from DTO.usuario_dto import UsuarioDTO
from utils.utils import hash_password, check_password

class UsuarioDAO(BaseDAO):
    def crear(self, usuario_dto: UsuarioDTO) -> bool:
        try:
            # Hashear la contraseña antes de guardar
            password_hash = hash_password(usuario_dto.password)
            
            with self.connection.cursor() as cursor:
                sql = "INSERT INTO usuarios (username, password_hash, rol) VALUES (%s, %s, %s)"
                cursor.execute(sql, (usuario_dto.username, password_hash, usuario_dto.rol))
                return True
        except Exception as e:
            print(f"Error al crear usuario: {e}")
            return False
    
    def obtener_por_id(self, id: int) -> Optional[UsuarioDTO]:
        try:
            with self.connection.cursor() as cursor:
                sql = "SELECT * FROM usuarios WHERE id = %s"
                cursor.execute(sql, (id,))
                result = cursor.fetchone()
                
                if result:
                    return self._convertir_a_dto(result)
                return None
        except Exception as e:
            print(f"Error al obtener usuario: {e}")
            return None
    
    def obtener_por_username(self, username: str) -> Optional[UsuarioDTO]:
        try:
            with self.connection.cursor() as cursor:
                sql = "SELECT * FROM usuarios WHERE username = %s"
                cursor.execute(sql, (username,))
                result = cursor.fetchone()
                
                if result:
                    return self._convertir_a_dto(result)
                return None
        except Exception as e:
            print(f"Error al obtener usuario por username: {e}")
            return None
    
    def validar_credenciales(self, username: str, password: str) -> Optional[UsuarioDTO]:
        try:
            with self.connection.cursor() as cursor:
                sql = "SELECT * FROM usuarios WHERE username = %s"
                cursor.execute(sql, (username,))
                result = cursor.fetchone()
                
                if result and check_password(password, result['password_hash']):
                    return self._convertir_a_dto(result)
                return None
        except Exception as e:
            print(f"Error al validar credenciales: {e}")
            return None
    
    def obtener_todos(self) -> List[UsuarioDTO]:
        usuarios = []
        try:
            with self.connection.cursor() as cursor:
                sql = "SELECT * FROM usuarios"
                cursor.execute(sql)
                results = cursor.fetchall()
                
                for result in results:
                    usuario_dto = self._convertir_a_dto(result)
                    usuarios.append(usuario_dto)
        except Exception as e:
            print(f"Error al obtener usuarios: {e}")
        
        return usuarios
    
    def actualizar(self, usuario_dto: UsuarioDTO) -> bool:
        try:
            with self.connection.cursor() as cursor:
                # Si se proporciona una nueva contraseña, hashearla
                if usuario_dto.password:
                    password_hash = hash_password(usuario_dto.password)
                    sql = "UPDATE usuarios SET username = %s, password_hash = %s, rol = %s WHERE id = %s"
                    cursor.execute(sql, (
                        usuario_dto.username,
                        password_hash,
                        usuario_dto.rol,
                        usuario_dto.id
                    ))
                else:
                    sql = "UPDATE usuarios SET username = %s, rol = %s WHERE id = %s"
                    cursor.execute(sql, (
                        usuario_dto.username,
                        usuario_dto.rol,
                        usuario_dto.id
                    ))
                return True
        except Exception as e:
            print(f"Error al actualizar usuario: {e}")
            return False
    
    def eliminar(self, id: int) -> bool:
        try:
            with self.connection.cursor() as cursor:
                sql = "DELETE FROM usuarios WHERE id = %s"
                cursor.execute(sql, (id,))
                return True
        except Exception as e:
            print(f"Error al eliminar usuario: {e}")
            return False
    
    def contar_usuarios(self) -> int:
        try:
            with self.connection.cursor() as cursor:
                sql = "SELECT COUNT(*) as total FROM usuarios"
                cursor.execute(sql)
                result = cursor.fetchone()
                return result['total'] if result else 0
        except Exception as e:
            print(f"Error al contar usuarios: {e}")
            return 0
    
    def _convertir_a_dto(self, db_record: dict) -> UsuarioDTO:
        return UsuarioDTO(
            id=db_record['id'],
            username=db_record['username'],
            password="",  
            rol=db_record['rol']
        )