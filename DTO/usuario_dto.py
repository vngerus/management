from typing import Optional

class UsuarioDTO:
    def __init__(self, id: Optional[int] = None, username: str = "", 
                 password: str = "", rol: str = "admin"):
        self.id = id
        self.username = username
        self.password = password  # Será hasheado en la capa DAO
        self.rol = rol
        
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'username': self.username,
            'password': self.password,
            'rol': self.rol
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data.get('id'),
            username=data.get('username', ''),
            password=data.get('password', ''),
            rol=data.get('rol', 'admin')
        )
    
    def __str__(self) -> str:
        return f"UsuarioDTO(id={self.id}, username='{self.username}', rol='{self.rol}')"