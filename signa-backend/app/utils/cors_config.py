"""
Configuración de CORS para la aplicación Flask
"""

from flask_cors import CORS

def configure_cors(app):
    """
    Configura CORS para la aplicación Flask
    
    Args:
        app: Instancia de Flask
    """
    
    # Configuración simple y efectiva de CORS
    CORS(app, 
         origins=["http://localhost:3000", "http://127.0.0.1:3000"],
         methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
         allow_headers=["Content-Type", "Authorization", "X-Requested-With"],
         supports_credentials=True,
         expose_headers=["Content-Type", "Authorization"])
