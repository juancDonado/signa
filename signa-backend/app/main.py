from flask import Flask
from .infrastructure.database.models import db
from .infrastructure.api.auth.routes import auth_bp
from .infrastructure.api.sign.routes import sign_bp
from .utils.cors_config import configure_cors
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Configurar CORS usando la configuración avanzada
    configure_cors(app)
    
    db.init_app(app)
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(sign_bp, url_prefix='/api/sign')
    
    with app.app_context():
        db.create_all()
    
    return app
