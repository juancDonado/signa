from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from .entities import User, UserCredentials, Sign

class UserRepository(ABC):
    """Interfaz abstracta para el repositorio de usuarios"""

    @abstractmethod
    def create(self, user: User) -> User:
        """Crea un nuevo usuario"""
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        """Obtiene un usuario por email"""
        pass

    @abstractmethod
    def update(self, user_id: int, **kwargs) -> Optional[User]:
        """Actualiza un usuario"""
        pass

class UserCredentialsRepository(ABC):
    """Interfaz abstracta para el repositorio de credenciales de usuario"""

    @abstractmethod
    def create(self, credentials: UserCredentials) -> UserCredentials:
        """Crea nuevas credenciales de usuario"""
        pass

    @abstractmethod
    def get_by_username(self, username: str) -> Optional[UserCredentials]:
        """Obtiene credenciales por username"""
        pass

    @abstractmethod
    def update(self, user_id: int, **kwargs) -> Optional[UserCredentials]:
        """Actualiza credenciales de usuario"""
        pass

class SignRepository(ABC):
    """Interfaz abstracta para el repositorio de signos"""

    @abstractmethod
    def create(self, sign: Sign) -> Sign:
        """Crea un nuevo signo"""
        pass

    @abstractmethod
    def get_all_active(self) -> List[Sign]:
        """Obtiene todos los signos activos"""
        pass

    @abstractmethod
    def get_by_id(self, sign_id: int) -> Optional[Sign]:
        """Obtiene un signo por ID"""
        pass

    @abstractmethod
    def get_by_name(self, name: str) -> Optional[Sign]:
        """Obtiene un signo por nombre (solo activos)"""
        pass

    @abstractmethod
    def update(self, sign_id: int, **kwargs) -> Optional[Sign]:
        """Actualiza un signo"""
        pass

    @abstractmethod
    def soft_delete(self, sign_id: int) -> bool:
        """Elimina suavemente un signo (cambia status a False)"""
        pass

    @abstractmethod
    def get_all_active_with_users(self) -> List[Dict[str, Any]]:
        """Obtiene todos los signos activos con información del usuario usando JOINs"""
        pass

    @abstractmethod
    def get_by_id_with_user(self, sign_id: int) -> Optional[Dict[str, Any]]:
        """Obtiene un signo por ID con información del usuario usando JOIN"""
        pass
