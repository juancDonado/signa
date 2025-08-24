from dataclasses import dataclass
from typing import Optional

@dataclass
class User:
    """Entidad de dominio para Usuario (información personal)"""
    id: Optional[int]
    name: str
    surname: str
    email: str
    address: str
    status: bool = True  # True = activo, False = eliminado

    def __post_init__(self):
        if not self.name or not self.surname or not self.email or not self.address:
            raise ValueError("Todos los campos son obligatorios")

        if '@' not in self.email:
            raise ValueError("Email debe ser válido")

@dataclass
class UserCredentials:
    """Entidad de dominio para Credenciales de Usuario"""
    id: Optional[int]  # Será igual al ID del usuario (relación 1:1)
    username: str  # Será igual al email del usuario
    password: str  # Contraseña generada aleatoriamente
    status: bool = True  # True = activo, False = eliminado

    def __post_init__(self):
        if not self.username or not self.password:
            raise ValueError("Username y password son obligatorios")

@dataclass
class Sign:
    """Entidad de dominio para Signo/Marca"""
    id: Optional[int]
    sign_name: str  # Cambiado de 'name' a 'sign_name'
    user_id: int
    status: bool = True  # True = activo, False = eliminado

    def __post_init__(self):
        if not self.sign_name:
            raise ValueError("El nombre del signo es obligatorio")
        if not self.user_id:
            raise ValueError("El ID del usuario es obligatorio")
