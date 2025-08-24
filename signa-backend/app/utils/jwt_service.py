import jwt
import datetime
from typing import Optional, Dict, Any
from flask import current_app

class JWTService:
    """Servicio para manejo de tokens JWT"""
    
    # Clave secreta para firmar tokens (en producción usar variable de entorno)
    SECRET_KEY = "signa_super_secret_key_change_in_production"
    
    # Algoritmo de firma
    ALGORITHM = "HS256"
    
    # Tiempo de expiración del token (24 horas)
    ACCESS_TOKEN_EXPIRE_MINUTES = 24 * 60
    
    @classmethod
    def create_access_token(cls, data: Dict[str, Any]) -> str:
        """Crea un token de acceso JWT"""
        to_encode = data.copy()
        
        # Agregar tiempo de expiración
        expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=cls.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        
        # Crear token
        encoded_jwt = jwt.encode(to_encode, cls.SECRET_KEY, algorithm=cls.ALGORITHM)
        return encoded_jwt
    
    @classmethod
    def verify_token(cls, token: str) -> Optional[Dict[str, Any]]:
        """Verifica y decodifica un token JWT"""
        try:
            # Decodificar token
            payload = jwt.decode(token, cls.SECRET_KEY, algorithms=[cls.ALGORITHM])
            
            # Verificar que no haya expirado
            if datetime.datetime.utcnow() > datetime.datetime.fromtimestamp(payload["exp"]):
                return None
            
            return payload
            
        except jwt.ExpiredSignatureError:
            # Token expirado
            return None
        except jwt.JWTError:
            # Token inválido
            return None
        except Exception:
            # Otros errores
            return None
    
    @classmethod
    def get_user_id_from_token(cls, token: str) -> Optional[int]:
        """Extrae el user_id del token JWT"""
        payload = cls.verify_token(token)
        if payload and "user_id" in payload:
            return payload["user_id"]
        return None
    
    @classmethod
    def get_username_from_token(cls, token: str) -> Optional[str]:
        """Extrae el username del token JWT"""
        payload = cls.verify_token(token)
        if payload and "username" in payload:
            return payload["username"]
        return None
