import os
import sys
from datetime import datetime
from app.infrastructure.database.models import db
from app.domain.entities import User, UserCredentials
from app.infrastructure.repositories import SQLAlchemyUserRepository, SQLAlchemyUserCredentialsRepository
from app.utils.password_service import PasswordService

class MigrationManager:
    """Gestor de migraciones para la base de datos"""
    
    def __init__(self):
        self.migrations = []
        self._register_migrations()
        self.password_service = PasswordService()
    
    def _register_migrations(self):
        """Registra todas las migraciones disponibles"""
        self.migrations = [
            {
                'id': '001_create_admin_user',
                'description': 'Crear usuario administrador por defecto',
                'function': self._create_admin_user
            },
            {
                'id': '002_update_database_structure',
                'description': 'Actualizar estructura de BD con campos status y sign_name',
                'function': self._update_database_structure
            }
        ]
    
    def run_migrations(self):
        """Ejecuta todas las migraciones pendientes"""
        print("🚀 Iniciando migraciones...")
        
        for migration in self.migrations:
            try:
                print(f"📋 Ejecutando migración: {migration['id']}")
                print(f"📝 Descripción: {migration['description']}")
                
                migration['function']()
                
                print(f"✅ Migración {migration['id']} completada exitosamente")
                print("-" * 50)
                
            except Exception as e:
                print(f"❌ Error en migración {migration['id']}: {str(e)}")
                raise
    
    def _create_admin_user(self):
        """Migración: Crear usuario administrador por defecto"""
        # Verificar si ya existe un usuario admin
        user_repo = SQLAlchemyUserRepository()
        credentials_repo = SQLAlchemyUserCredentialsRepository()
        
        existing_user = user_repo.get_by_email('admin@signa.com')
        if existing_user:
            print("ℹ️  Usuario admin ya existe, saltando migración")
            return
        
        # Crear usuario admin (solo información personal)
        admin_user = User(
            id=None,
            name="Administrador",
            surname="Sistema",
            email="admin@signa.com",
            address="Sistema",
            status=True
        )
        
        # Guardar usuario en la base de datos
        saved_user = user_repo.create(admin_user)
        
        # Contraseña por defecto para admin
        plain_password = 'admin123'
        
        # Hashear la contraseña usando bcrypt
        hashed_password = self.password_service.hash_password(plain_password)
        
        # Crear credenciales con el mismo ID del usuario
        admin_credentials = UserCredentials(
            id=saved_user.id,  # Mismo ID que el usuario
            username="admin@signa.com",  # Username será igual al email
            password=hashed_password,
            status=True
        )
        
        # Guardar credenciales
        credentials_repo.create(admin_credentials)
        
        print(f"👤 Usuario admin creado con ID: {saved_user.id}")
        print(f"📧 Email: {saved_user.email}")
        print(f"👤 Username: {admin_credentials.username}")
        print(f"🔑 Contraseña: {plain_password}")
        print(f"🔒 Contraseña hasheada con bcrypt (12 rounds, muy segura)")
        print("⚠️  IMPORTANTE: Cambia esta contraseña en producción")
    
    def _update_database_structure(self):
        """Migración: Actualizar estructura de BD con campos status y sign_name"""
        print("🔄 Actualizando estructura de base de datos...")
        
        # Crear tablas si no existen (esto incluirá los nuevos campos)
        db.create_all()
        
        print("✅ Estructura de base de datos actualizada")
        print("📋 Campos agregados:")
        print("   - users.status (boolean, default True)")
        print("   - user_credentials.status (boolean, default True)")
        print("   - signs.status (boolean, default True)")
        print("   - signs.sign_name (string, nullable=False)")

def run_migrations():
    """Función principal para ejecutar migraciones"""
    try:
        from app.main import create_app
        
        # Crear aplicación Flask
        app = create_app()
        
        with app.app_context():
            # Crear tablas si no existen
            db.create_all()
            
            # Ejecutar migraciones
            migration_manager = MigrationManager()
            migration_manager.run_migrations()
            
        print("🎉 Todas las migraciones completadas exitosamente!")
        
    except Exception as e:
        print(f"❌ Error ejecutando migraciones: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    run_migrations()
