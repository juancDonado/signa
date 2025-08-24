from flask import Blueprint, request, jsonify
from ....domain.services import UserService
from ....infrastructure.repositories import SQLAlchemyUserRepository, SQLAlchemyUserCredentialsRepository
from ....utils.jwt_service import JWTService

# Crear blueprint para rutas de autenticación
auth_bp = Blueprint('auth', __name__)

# Crear instancias de repositorios
user_repository = SQLAlchemyUserRepository()
credentials_repository = SQLAlchemyUserCredentialsRepository()

# Crear instancia de servicio
user_service = UserService(user_repository, credentials_repository)

@auth_bp.route('/register', methods=['POST'])
def register():
    """Endpoint público para registrar nuevos usuarios"""
    try:
        data = request.get_json()
        
        # Validar datos requeridos
        required_fields = ['name', 'surname', 'email', 'address']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Campo requerido: {field}'}), 400
        
        # Crear usuario usando el servicio de dominio
        user = user_service.create_user(
            name=data['name'],
            surname=data['surname'],
            email=data['email'],
            address=data['address']
        )
        
        return jsonify({
            'message': 'Usuario registrado exitosamente',
            'user_id': user.id,
            'username': user.email,  # El username es el email
            'note': 'La contraseña se genera automáticamente y se hashea con bcrypt (12 rounds). Usa /login para obtener tu token JWT.'
        }), 201
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Error interno del servidor'}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """Endpoint para autenticar usuarios y obtener token JWT"""
    try:
        data = request.get_json()
        
        # Validar datos requeridos
        if 'username' not in data or 'password' not in data:
            return jsonify({'error': 'Username y password son requeridos'}), 400
        
        # Autenticar usuario
        user = user_service.authenticate_user(data['username'], data['password'])
        
        if not user:
            return jsonify({'error': 'Credenciales inválidas'}), 401
        
        # Crear token JWT
        token_data = {
            'user_id': user.id,
            'username': data['username'],
            'name': user.name,
            'surname': user.surname,
            'email': user.email
        }
        
        access_token = JWTService.create_access_token(token_data)
        
        return jsonify({
            'message': 'Login exitoso',
            'access_token': access_token,
            'user': {
                'id': user.id,
                'name': user.name,
                'surname': user.surname,
                'email': user.email,
                'username': data['username']
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Error interno del servidor'}), 500

@auth_bp.route('/logout', methods=['POST'])
def logout():
    """Endpoint para cerrar sesión"""
    return jsonify({'message': 'Logout exitoso'}), 200
