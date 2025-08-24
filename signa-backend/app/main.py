from flask import Flask
from .infrastructure.database.models import db
from .infrastructure.api.auth.routes import auth_bp
from .infrastructure.api.sign.routes import sign_bp
from config import Config

def create_app():
    """Factory function para crear la aplicación Flask"""
    app = Flask(__name__)
    
    app.config.from_object(Config)
    db.init_app(app)
    
    # Registrar blueprints organizados por funcionalidad
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(sign_bp, url_prefix='/api/sign')
    
    with app.app_context():
        # Solo crear las tablas si no existen (sin ejecutar migraciones)
        db.create_all()
        
        # NOTA: Las migraciones solo se ejecutan con: python run_migrations.py
        # print("ℹ️  Para ejecutar migraciones use: python run_migrations.py")
    
    return app
