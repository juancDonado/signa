import secrets
import string
from typing import List, Optional, Dict, Any, Tuple
from .entities import User, UserCredentials, Sign
from .repositories import UserRepository, UserCredentialsRepository, SignRepository
from ..utils.password_service import PasswordService

class SignService:
    """Servicio de dominio para gestión de marcas/signos - Casos de uso"""
    
    def __init__(self, sign_repository: SignRepository, user_repository: UserRepository, credentials_repository: UserCredentialsRepository):
        self.sign_repository = sign_repository
        self.user_repository = user_repository
        self.credentials_repository = credentials_repository
        self.password_service = PasswordService()
    
    # CASO DE USO: Crear marca con usuario
    def create_sign_with_user(self, sign_data: Dict[str, Any]) -> Tuple[bool, Dict[str, Any], int]:
        """
        Caso de uso: Crear una marca y su usuario asociado
        Returns: (success, data, status_code)
        """
        try:
            # Validar datos requeridos para la marca
            if 'sign_name' not in sign_data:
                return False, {'error': 'El nombre de la marca (sign_name) es obligatorio'}, 400
            
            # Validar datos requeridos para el usuario
            user_fields = ['name', 'surname', 'email', 'address']
            for field in user_fields:
                if field not in sign_data:
                    return False, {'error': f'Campo requerido para usuario: {field}'}, 400
            
            # Verificar si la marca ya existe (solo activas)
            existing_sign = self.sign_repository.get_by_name(sign_data['sign_name'])
            if existing_sign:
                return False, {'error': f"Ya existe una marca con el nombre '{sign_data['sign_name']}'"}, 400
            
            # Verificar si el usuario ya existe
            existing_user = self.user_repository.get_by_email(sign_data['email'])
            
            if existing_user:
                # Usar usuario existente
                user = existing_user
                user_created = False
                credentials_created = False
            else:
                # Crear nuevo usuario
                user = User(
                    id=None,
                    name=sign_data['name'],
                    surname=sign_data['surname'],
                    email=sign_data['email'],
                    address=sign_data['address'],
                    status=True
                )
                user = self.user_repository.create(user)
                user_created = True
                
                # Generar contraseña aleatoria y crear credenciales
                plain_password = self.password_service.generate_random_password()
                hashed_password = self.password_service.hash_password(plain_password)
                
                credentials = UserCredentials(
                    id=user.id,
                    username=sign_data['email'],
                    password=hashed_password,
                    status=True
                )
                self.credentials_repository.create(credentials)
                credentials_created = True
            
            # Crear la marca
            sign = Sign(
                id=None,
                sign_name=sign_data['sign_name'],
                user_id=user.id,
                status=True
            )
            sign = self.sign_repository.create(sign)
            
            response_data = {
                'message': 'Marca creada exitosamente',
                'sign': {
                    'id': sign.id,
                    'sign_name': sign.sign_name,
                    'status': sign.status
                },
                'user': {
                    'id': user.id,
                    'name': user.name,
                    'surname': user.surname,
                    'email': user.email,
                    'address': user.address,
                    'status': user.status
                }
            }
            
            # Agregar información sobre si se creó usuario y credenciales
            if user_created:
                response_data['user_created'] = True
                response_data['credentials_created'] = True
                response_data['note'] = f"Usuario y credenciales creados. Contraseña: {plain_password}"
            else:
                response_data['user_created'] = False
                response_data['credentials_created'] = False
                response_data['note'] = "Usuario existente reutilizado"
            
            return True, response_data, 201
            
        except Exception as e:
            return False, {'error': 'Error interno del servidor'}, 500
    
    # CASO DE USO: Actualizar marca
    def update_sign(self, sign_id: int, update_data: Dict[str, Any]) -> Tuple[bool, Dict[str, Any], int]:
        """
        Caso de uso: Actualizar una marca y/o usuario asociado
        Returns: (success, data, status_code)
        """
        try:
            if not update_data:
                return False, {'error': 'No se proporcionaron datos para actualizar'}, 400
            
            # Separar datos por entidad
            sign_data = {}
            user_data = {}
            credentials_data = {}
            
            # Campos de la marca
            if 'sign_name' in update_data:
                sign_data['sign_name'] = update_data['sign_name']
            
            # Campos del usuario
            user_fields = ['name', 'surname', 'email', 'address']
            for field in user_fields:
                if field in update_data:
                    user_data[field] = update_data[field]
            
            # Campos de credenciales
            if 'password' in update_data:
                credentials_data['password'] = update_data['password']
            
            # Actualizar marca si hay datos
            if sign_data:
                updated_sign = self._update_sign_fields(sign_id, sign_data)
                if not updated_sign:
                    return False, {'error': 'Marca no encontrada'}, 404
            
            # Actualizar usuario si hay datos
            if user_data:
                updated_user = self._update_user_fields(sign_id, user_data)
                if not updated_user:
                    return False, {'error': 'Usuario no encontrado'}, 404
            
            # Actualizar credenciales si hay datos
            if credentials_data:
                updated_credentials = self._update_credentials_fields(sign_id, credentials_data)
                if not updated_credentials:
                    return False, {'error': 'Credenciales no encontradas'}, 404
            
            # Obtener la información completa actualizada
            complete_sign_info = self.get_sign_by_id(sign_id)
            
            response_data = {
                'message': 'Marca actualizada exitosamente',
                'sign': complete_sign_info['sign'],
                'user': complete_sign_info['user']
            }
            
            return True, response_data, 200
            
        except ValueError as e:
            return False, {'error': str(e)}, 400
        except Exception as e:
            return False, {'error': 'Error interno del servidor'}, 500
    
    # CASO DE USO: Obtener todas las marcas
    def get_all_signs(self) -> Tuple[bool, Dict[str, Any], int]:
        """
        Caso de uso: Obtener todas las marcas activas con información del usuario
        Returns: (success, data, status_code)
        """
        try:
            signs = self.sign_repository.get_all_active_with_users()
            
            response_data = {
                'message': 'Marcas obtenidas exitosamente',
                'total': len(signs),
                'signs': signs
            }
            
            return True, response_data, 200
            
        except Exception as e:
            return False, {'error': 'Error interno del servidor'}, 500
    
    # CASO DE USO: Obtener marca por ID
    def get_sign_by_id(self, sign_id: int) -> Optional[Dict[str, Any]]:
        """
        Caso de uso: Obtener una marca por ID con información del usuario
        Returns: Dict con información de la marca o None si no existe
        """
        return self.sign_repository.get_by_id_with_user(sign_id)
    
    # CASO DE USO: Obtener marca por ID con validación
    def get_sign_by_id_validated(self, sign_id: int) -> Tuple[bool, Dict[str, Any], int]:
        """
        Caso de uso: Obtener una marca por ID con validación
        Returns: (success, data, status_code)
        """
        try:
            sign = self.get_sign_by_id(sign_id)
            
            if not sign:
                return False, {'error': 'Marca no encontrada'}, 404
            
            response_data = {
                'message': 'Marca obtenida exitosamente',
                'sign': sign
            }
            
            return True, response_data, 200
            
        except Exception as e:
            return False, {'error': 'Error interno del servidor'}, 500
    
    # CASO DE USO: Soft delete marca
    def soft_delete_sign(self, sign_id: int) -> Tuple[bool, Dict[str, Any], int]:
        """
        Caso de uso: Eliminar suavemente una marca
        Returns: (success, data, status_code)
        """
        try:
            success = self.sign_repository.soft_delete(sign_id)
            
            if not success:
                return False, {'error': 'Marca no encontrada o ya eliminada'}, 404
            
            response_data = {
                'message': 'Marca eliminada exitosamente',
            }
            
            return True, response_data, 200
            
        except Exception as e:
            return False, {'error': 'Error interno del servidor'}, 500
    
    # Métodos privados para lógica interna
    def _update_sign_fields(self, sign_id: int, sign_data: Dict[str, Any]) -> Optional[Sign]:
        """Actualiza campos de la marca"""
        # Verificar si la marca existe
        existing_sign = self.sign_repository.get_by_id(sign_id)
        if not existing_sign:
            return None
        
        # Si se está cambiando el nombre, verificar que no exista otra marca con ese nombre
        if 'sign_name' in sign_data and sign_data['sign_name'] != existing_sign.sign_name:
            duplicate_sign = self.sign_repository.get_by_name(sign_data['sign_name'])
            if duplicate_sign:
                raise ValueError(f"Ya existe una marca con el nombre '{sign_data['sign_name']}'")
        
        # Actualizar solo los campos proporcionados
        return self.sign_repository.update(sign_id, **sign_data)
    
    def _update_user_fields(self, sign_id: int, user_data: Dict[str, Any]) -> Optional[User]:
        """Actualiza campos del usuario"""
        # Obtener la marca
        sign = self.sign_repository.get_by_id(sign_id)
        if not sign:
            return None
        
        # Actualizar usuario
        return self.user_repository.update(sign.user_id, **user_data)
    
    def _update_credentials_fields(self, sign_id: int, credentials_data: Dict[str, Any]) -> Optional[UserCredentials]:
        """Actualiza campos de las credenciales"""
        # Obtener la marca
        sign = self.sign_repository.get_by_id(sign_id)
        if not sign:
            return None
        
        # Si se está cambiando la contraseña, hashearla
        if 'password' in credentials_data:
            credentials_data['password'] = self.password_service.hash_password(credentials_data['password'])
        
        # Actualizar credenciales
        return self.credentials_repository.update(sign.user_id, **credentials_data)

class UserService:
    """Servicio de dominio para gestión de usuarios (solo autenticación)"""
    
    def __init__(self, user_repository: UserRepository, credentials_repository: UserCredentialsRepository):
        self.user_repository = user_repository
        self.credentials_repository = credentials_repository
        self.password_service = PasswordService()
    
    def create_user(self, name: str, surname: str, email: str, address: str) -> User:
        """Crea un nuevo usuario con credenciales"""
        # Verificar si el usuario ya existe
        existing_user = self.user_repository.get_by_email(email)
        if existing_user:
            raise ValueError(f"Ya existe un usuario con el email '{email}'")
        
        # Crear usuario
        user = User(
            id=None,
            name=name,
            surname=surname,
            email=email,
            address=address,
            status=True
        )
        user = self.user_repository.create(user)
        
        # Generar contraseña aleatoria y crear credenciales
        plain_password = self.password_service.generate_random_password()
        hashed_password = self.password_service.hash_password(plain_password)
        
        credentials = UserCredentials(
            id=user.id,
            username=email,  # Username será igual al email
            password=hashed_password,
            status=True
        )
        self.credentials_repository.create(credentials)
        
        return user
    
    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """Autentica un usuario con username y password"""
        # Obtener credenciales
        credentials = self.credentials_repository.get_by_username(username)
        if not credentials:
            return None
        
        # Verificar contraseña
        if not self.password_service.verify_password(password, credentials.password):
            return None
        
        # Obtener usuario
        user = self.user_repository.get_by_email(username)  # username es el email
        return user
