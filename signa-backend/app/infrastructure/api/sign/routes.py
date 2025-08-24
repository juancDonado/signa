from flask import Blueprint, request, jsonify
from ....domain.services import SignService
from ....infrastructure.repositories import SQLAlchemyUserRepository, SQLAlchemyUserCredentialsRepository, SQLAlchemySignRepository
from ....utils.auth_guard import require_auth

# Crear blueprint para rutas de signos
sign_bp = Blueprint('sign', __name__)

# Crear instancias de repositorios
user_repository = SQLAlchemyUserRepository()
credentials_repository = SQLAlchemyUserCredentialsRepository()
sign_repository = SQLAlchemySignRepository()

# Crear instancia de servicio
sign_service = SignService(sign_repository, user_repository, credentials_repository)

@sign_bp.route('/create', methods=['POST'])
@require_auth
def create_sign():
    """Endpoint para crear una marca con usuario asociado"""
    data = request.get_json()
    success, response_data, status_code = sign_service.create_sign_with_user(data)
    return jsonify(response_data), status_code

@sign_bp.route('/<int:sign_id>', methods=['PATCH'])
@require_auth
def update_sign(sign_id):
    """Endpoint para actualizar una marca (método PATCH)"""
    data = request.get_json()
    success, response_data, status_code = sign_service.update_sign(sign_id, data)
    return jsonify(response_data), status_code

@sign_bp.route('/list', methods=['GET'])
@require_auth
def get_all_signs():
    """Endpoint para obtener todas las marcas activas con información del usuario"""
    success, response_data, status_code = sign_service.get_all_signs()
    return jsonify(response_data), status_code

@sign_bp.route('/<int:sign_id>', methods=['GET'])
@require_auth
def get_sign_by_id(sign_id):
    """Endpoint para obtener una marca por ID con información del usuario"""
    success, response_data, status_code = sign_service.get_sign_by_id_validated(sign_id)
    return jsonify(response_data), status_code

@sign_bp.route('/<int:sign_id>', methods=['DELETE'])
@require_auth
def soft_delete_sign(sign_id):
    """Endpoint para eliminar suavemente una marca (soft delete)"""
    success, response_data, status_code = sign_service.soft_delete_sign(sign_id)
    return jsonify(response_data), status_code
