import secrets
import string
import bcrypt

class PasswordService:
    """Servicio para manejo seguro de contraseñas usando bcrypt"""
    
    @staticmethod
    def generate_random_password(length: int = 12) -> str:
        """Genera una contraseña aleatoria segura"""
        # Usar solo caracteres seguros (evitar caracteres confusos)
        alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
        return ''.join(secrets.choice(alphabet) for _ in range(length))
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hashea una contraseña usando bcrypt"""
        # Convertir password a bytes y generar salt
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt(rounds=12)  # 12 rounds es muy seguro
        
        # Generar hash
        hashed = bcrypt.hashpw(password_bytes, salt)
        
        # Retornar como string
        return hashed.decode('utf-8')
    
    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        """Verifica si una contraseña coincide con su hash"""
        try:
            password_bytes = password.encode('utf-8')
            hashed_bytes = hashed_password.encode('utf-8')
            return bcrypt.checkpw(password_bytes, hashed_bytes)
        except Exception:
            return False
    
    @staticmethod
    def needs_rehash(hashed_password: str) -> bool:
        """Verifica si un hash necesita ser regenerado (por cambios en configuración)"""
        # bcrypt no tiene un método directo para esto, pero podemos verificar los rounds
        try:
            hashed_bytes = hashed_password.encode('utf-8')
            # Si los rounds son menores a 12, necesita rehash
            return bcrypt.get_parameter_count(hashed_bytes) < 12
        except Exception:
            return True
