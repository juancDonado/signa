import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuración de la aplicación"""
    
    # Configuración de la base de datos
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://signa:signa_pass@localhost:5433/signa_db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Clave secreta para sesiones y JWT
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Configuración de CORS
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:3000,http://127.0.0.1:3000').split(',')
    CORS_METHODS = os.getenv('CORS_METHODS', 'GET,POST,PUT,PATCH,DELETE,OPTIONS').split(',')
    CORS_ALLOW_HEADERS = os.getenv('CORS_ALLOW_HEADERS', 'Content-Type,Authorization,X-Requested-With').split(',')
    
    # Configuración JWT
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production')
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRE_MINUTES', 30))
    
    # Configuración de seguridad
    BCRYPT_LOG_ROUNDS = int(os.getenv('BCRYPT_LOG_ROUNDS', 12))
    
    # Configuración de la aplicación
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'