from functools import wraps
from flask import request, jsonify, g
from .jwt_service import JWTService

def require_auth(f):
    """Decorador para proteger rutas que requieren autenticación"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Obtener token del header Authorization
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            return jsonify({'error': 'Token de autorización requerido'}), 401
        
        # Verificar formato del header (Bearer <token>)
        try:
            scheme, token = auth_header.split()
            if scheme.lower() != 'bearer':
                return jsonify({'error': 'Formato de autorización inválido. Use: Bearer <token>'}), 401
        except ValueError:
            return jsonify({'error': 'Formato de autorización inválido. Use: Bearer <token>'}), 401
        
        # Verificar token
        payload = JWTService.verify_token(token)
        if not payload:
            return jsonify({'error': 'Token inválido o expirado'}), 401
        
        # Almacenar información del usuario en g para uso posterior
        g.user_id = payload.get('user_id')
        g.username = payload.get('username')
        g.user_data = payload
        
        return f(*args, **kwargs)
    
    return decorated_function

def get_current_user_id() -> int:
    """Obtiene el ID del usuario autenticado actualmente"""
    return g.user_id

def get_current_username() -> str:
    """Obtiene el username del usuario autenticado actualmente"""
    return g.username

def get_current_user_data() -> dict:
    """Obtiene todos los datos del usuario autenticado actualmente"""
    return g.user_data
