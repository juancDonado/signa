from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """Modelo de base de datos para Usuario (información personal)"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    address = db.Column(db.String(100), nullable=False)
    status = db.Column(db.Boolean, default=True, nullable=False)  # True = activo, False = eliminado

    # Relación 1:1 con UserCredentials usando el mismo ID
    credentials = db.relationship('UserCredentials', backref='user', uselist=False, cascade='all, delete-orphan')
    
    # Relación 1:N con Sign
    signs = db.relationship('Sign', backref='user', lazy='dynamic')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'surname': self.surname,
            'email': self.email,
            'address': self.address,
            'status': self.status,
            'username': self.credentials.username if self.credentials else None
        }

class UserCredentials(db.Model):
    """Modelo de base de datos para Credenciales de Usuario"""
    __tablename__ = 'user_credentials'

    # El ID será igual al ID del usuario (relación 1:1)
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    status = db.Column(db.Boolean, default=True, nullable=False)  # True = activo, False = eliminado

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'status': self.status
        }

class Sign(db.Model):
    """Modelo de base de datos para Signo/Marca"""
    __tablename__ = 'signs'

    id = db.Column(db.Integer, primary_key=True)
    sign_name = db.Column(db.String(100), nullable=False)  # Cambiado de 'name' a 'sign_name'
    userId = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.Boolean, default=True, nullable=False)  # True = activo, False = eliminado

    def to_dict(self):
        return {
            'id': self.id,
            'sign_name': self.sign_name,  # Cambiado de 'name' a 'sign_name'
            'userId': self.userId,
            'status': self.status
        }
