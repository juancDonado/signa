from typing import List, Optional, Dict, Any
from app.domain.repositories import UserRepository, UserCredentialsRepository, SignRepository
from app.domain.entities import User, UserCredentials, Sign
from .database.models import db, User as UserModel, UserCredentials as UserCredentialsModel, Sign as SignModel
from ..utils.transaction_service import TransactionService

class SQLAlchemyUserRepository(UserRepository):
    """Implementación concreta del repositorio de usuarios usando SQLAlchemy con transacciones"""

    def create(self, user: User) -> User:
        """Crea un nuevo usuario en la base de datos usando transacciones"""
        
        def create_user_transaction(session):
            db_user = UserModel(
                name=user.name,
                surname=user.surname,
                email=user.email,
                address=user.address,
                status=user.status
            )
            session.add(db_user)
            session.flush()  # Para obtener el ID asignado
            
            return User(
                id=db_user.id,
                name=db_user.name,
                surname=db_user.surname,
                email=db_user.email,
                address=db_user.address,
                status=db_user.status
            )
        
        return TransactionService.execute_in_transaction(create_user_transaction)

    def get_by_email(self, email: str) -> Optional[User]:
        """Obtiene un usuario por email usando transacciones de solo lectura"""
        
        def get_user_by_email_transaction(session):
            db_user = session.query(UserModel).filter_by(email=email, status=True).first()
            if not db_user:
                return None

            return User(
                id=db_user.id,
                name=db_user.name,
                surname=db_user.surname,
                email=db_user.email,
                address=db_user.address,
                status=db_user.status
            )
        
        return TransactionService.execute_read_only(get_user_by_email_transaction)

    def update(self, user_id: int, **kwargs) -> Optional[User]:
        """Actualiza un usuario usando transacciones"""
        
        def update_user_transaction(session):
            db_user = session.query(UserModel).filter_by(id=user_id, status=True).first()
            if not db_user:
                return None
            
            # Actualizar solo los campos proporcionados
            for key, value in kwargs.items():
                if hasattr(db_user, key):
                    setattr(db_user, key, value)
            
            session.flush()
            
            return User(
                id=db_user.id,
                name=db_user.name,
                surname=db_user.surname,
                email=db_user.email,
                address=db_user.address,
                status=db_user.status
            )
        
        return TransactionService.execute_in_transaction(update_user_transaction)

class SQLAlchemyUserCredentialsRepository(UserCredentialsRepository):
    """Implementación concreta del repositorio de credenciales usando SQLAlchemy con transacciones"""

    def create(self, credentials: UserCredentials) -> UserCredentials:
        """Crea nuevas credenciales de usuario en la base de datos usando transacciones"""
        
        def create_credentials_transaction(session):
            db_credentials = UserCredentialsModel(
                id=credentials.id,  # Mismo ID que el usuario
                username=credentials.username,
                password=credentials.password,
                status=credentials.status
            )
            session.add(db_credentials)
            session.flush()
            
            return UserCredentials(
                id=db_credentials.id,
                username=db_credentials.username,
                password=db_credentials.password,
                status=db_credentials.status
            )
        
        return TransactionService.execute_in_transaction(create_credentials_transaction)

    def get_by_username(self, username: str) -> Optional[UserCredentials]:
        """Obtiene credenciales por username usando transacciones de solo lectura"""
        
        def get_credentials_by_username_transaction(session):
            db_credentials = session.query(UserCredentialsModel).filter_by(username=username, status=True).first()
            if not db_credentials:
                return None

            return UserCredentials(
                id=db_credentials.id,
                username=db_credentials.username,
                password=db_credentials.password,
                status=db_credentials.status
            )
        
        return TransactionService.execute_read_only(get_credentials_by_username_transaction)

    def update(self, user_id: int, **kwargs) -> Optional[UserCredentials]:
        """Actualiza credenciales de usuario usando transacciones"""
        
        def update_credentials_transaction(session):
            db_credentials = session.query(UserCredentialsModel).filter_by(id=user_id, status=True).first()
            if not db_credentials:
                return None
            
            # Actualizar solo los campos proporcionados
            for key, value in kwargs.items():
                if hasattr(db_credentials, key):
                    setattr(db_credentials, key, value)
            
            session.flush()
            
            return UserCredentials(
                id=db_credentials.id,
                username=db_credentials.username,
                password=db_credentials.password,
                status=db_credentials.status
            )
        
        return TransactionService.execute_in_transaction(update_credentials_transaction)

class SQLAlchemySignRepository(SignRepository):
    """Implementación concreta del repositorio de signos usando SQLAlchemy con transacciones"""

    def create(self, sign: Sign) -> Sign:
        """Crea un nuevo signo en la base de datos usando transacciones"""
        
        def create_sign_transaction(session):
            db_sign = SignModel(
                sign_name=sign.sign_name,  # Cambiado de 'name' a 'sign_name'
                userId=sign.user_id,
                status=sign.status
            )
            session.add(db_sign)
            session.flush()
            
            return Sign(
                id=db_sign.id,
                sign_name=db_sign.sign_name,  # Cambiado de 'name' a 'sign_name'
                user_id=db_sign.userId,
                status=db_sign.status
            )
        
        return TransactionService.execute_in_transaction(create_sign_transaction)

    def get_all_active(self) -> List[Sign]:
        """Obtiene todos los signos activos usando transacciones de solo lectura"""
        
        def get_all_active_signs_transaction(session):
            db_signs = session.query(SignModel).filter_by(status=True).all()
            return [
                Sign(
                    id=db_sign.id,
                    sign_name=db_sign.sign_name,  # Cambiado de 'name' a 'sign_name'
                    user_id=db_sign.userId,
                    status=db_sign.status
                )
                for db_sign in db_signs
            ]
        
        return TransactionService.execute_read_only(get_all_active_signs_transaction)

    def get_by_id(self, sign_id: int) -> Optional[Sign]:
        """Obtiene un signo por ID usando transacciones de solo lectura"""
        
        def get_sign_by_id_transaction(session):
            db_sign = session.query(SignModel).filter_by(id=sign_id, status=True).first()
            if not db_sign:
                return None

            return Sign(
                id=db_sign.id,
                sign_name=db_sign.sign_name,  # Cambiado de 'name' a 'sign_name'
                user_id=db_sign.userId,
                status=db_sign.status
            )
        
        return TransactionService.execute_read_only(get_sign_by_id_transaction)

    def get_by_name(self, sign_name: str) -> Optional[Sign]:
        """Obtiene un signo por nombre (solo activos) usando transacciones de solo lectura"""
        
        def get_sign_by_name_transaction(session):
            db_sign = session.query(SignModel).filter_by(sign_name=sign_name, status=True).first()
            if not db_sign:
                return None

            return Sign(
                id=db_sign.id,
                sign_name=db_sign.sign_name,  # Cambiado de 'name' a 'sign_name'
                user_id=db_sign.userId,
                status=db_sign.status
            )
        
        return TransactionService.execute_read_only(get_sign_by_name_transaction)

    def update(self, sign_id: int, **kwargs) -> Optional[Sign]:
        """Actualiza un signo usando transacciones"""
        
        def update_sign_transaction(session):
            db_sign = session.query(SignModel).filter_by(id=sign_id, status=True).first()
            if not db_sign:
                return None

            # Actualizar solo los campos proporcionados
            for key, value in kwargs.items():
                if hasattr(db_sign, key):
                    setattr(db_sign, key, value)
            
            session.flush()
            
            return Sign(
                id=db_sign.id,
                sign_name=db_sign.sign_name,
                user_id=db_sign.userId,
                status=db_sign.status
            )
        
        return TransactionService.execute_in_transaction(update_sign_transaction)

    def soft_delete(self, sign_id: int) -> bool:
        """Elimina suavemente un signo (cambia status a False) usando transacciones"""
        
        def soft_delete_sign_transaction(session):
            db_sign = session.query(SignModel).filter_by(id=sign_id, status=True).first()
            if not db_sign:
                return False
            
            db_sign.status = False
            session.flush()
            return True
        
        return TransactionService.execute_in_transaction(soft_delete_sign_transaction)

    def get_all_active_with_users(self) -> List[Dict[str, Any]]:
        """Obtiene todos los signos activos con información del usuario usando JOINs"""
        
        def get_all_active_with_users_transaction(session):
            # Consulta con JOIN para traer signos y usuarios en una sola operación
            db_signs_with_users = session.query(
                SignModel, UserModel
            ).join(
                UserModel, SignModel.userId == UserModel.id
            ).filter(
                SignModel.status == True,
                UserModel.status == True
            ).all()
            
            result = []
            for db_sign, db_user in db_signs_with_users:
                sign_info = {
                    'sign': {
                        'id': db_sign.id,
                        'sign_name': db_sign.sign_name,
                        'status': db_sign.status
                    },
                    'user': {
                        'id': db_user.id,
                        'name': db_user.name,
                        'surname': db_user.surname,
                        'email': db_user.email,
                        'address': db_user.address,
                        'status': db_user.status
                    }
                }
                result.append(sign_info)
            
            return result
        
        return TransactionService.execute_read_only(get_all_active_with_users_transaction)

    def get_by_id_with_user(self, sign_id: int) -> Optional[Dict[str, Any]]:
        """Obtiene un signo por ID con información del usuario usando JOIN"""
        
        def get_sign_by_id_with_user_transaction(session):
            # Consulta con JOIN para traer signo y usuario en una sola operación
            db_result = session.query(
                SignModel, UserModel
            ).join(
                UserModel, SignModel.userId == UserModel.id
            ).filter(
                SignModel.id == sign_id,
                SignModel.status == True,
                UserModel.status == True
            ).first()
            
            if not db_result:
                return None
            
            db_sign, db_user = db_result
            
            return {
                'sign': {
                    'id': db_sign.id,
                    'sign_name': db_sign.sign_name,
                    'status': db_sign.status
                },
                'user': {
                    'id': db_user.id,
                    'name': db_user.name,
                    'surname': db_user.surname,
                    'email': db_user.email,
                    'address': db_user.address,
                    'status': db_user.status
                }
            }
        
        return TransactionService.execute_read_only(get_sign_by_id_with_user_transaction)
