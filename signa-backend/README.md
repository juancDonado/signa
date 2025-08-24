# 🚀 Signa Backend

Backend del sistema de gestión de marcas Signa, construido con Flask y arquitectura limpia.

## ✨ Características

- **🏗️ Arquitectura Limpia**: Separación clara de responsabilidades
- **🔐 Autenticación JWT**: Sistema seguro de tokens
- **🗄️ Base de Datos**: PostgreSQL con SQLAlchemy
- **🌐 API REST**: Endpoints organizados por funcionalidad
- **🔒 CORS Configurado**: Compatible con frontend Next.js
- **🐳 Docker Ready**: Configuración completa para contenedores
- **📊 Transacciones**: Sistema de transacciones atómico
- **🔄 Migraciones**: Gestión de esquemas de base de datos

## 🚀 Tecnologías

- **Framework**: Flask 2.3.3
- **Base de Datos**: PostgreSQL + SQLAlchemy
- **Autenticación**: JWT + bcrypt
- **CORS**: flask-cors para compatibilidad frontend
- **Contenedores**: Docker + Docker Compose
- **Python**: 3.9+

## 📁 Estructura del Proyecto

```
signa-backend/
├── app/
│   ├── domain/                 # Capa de dominio
│   │   ├── entities.py        # Entidades de negocio
│   │   ├── repositories.py    # Interfaces de repositorios
│   │   └── services.py        # Lógica de negocio (casos de uso)
│   ├── infrastructure/        # Capa de infraestructura
│   │   ├── database/          # Configuración de BD
│   │   │   └── models.py     # Modelos SQLAlchemy
│   │   ├── repositories/      # Implementaciones de repositorios
│   │   └── api/              # Controladores de API
│   │       ├── auth/         # Endpoints de autenticación
│   │       └── sign/         # Endpoints de marcas
│   └── utils/                 # Utilidades
│       ├── auth_guard.py     # Decorador de autenticación
│       ├── jwt_service.py    # Servicio JWT
│       ├── password_service.py # Servicio de contraseñas
│       ├── transaction_service.py # Servicio de transacciones
│       └── cors_config.py    # Configuración CORS
├── migrations/                # Gestor de migraciones
├── config.py                  # Configuración de la aplicación
├── requirements.txt           # Dependencias Python
├── docker-compose.yml         # Orquestación de contenedores
├── Dockerfile                 # Imagen del contenedor
├── run.py                     # Script principal de ejecución
├── run_migrations.py          # Script de migraciones
└── test_cors.py              # Script de prueba CORS
```

## 🛠️ Instalación

### Prerrequisitos

- Python 3.9+
- PostgreSQL (local o Docker)
- pip

### Instalación Local

1. **Clonar el repositorio**
   ```bash
   git clone <url-del-repositorio>
   cd signa-backend
   ```

2. **Crear entorno virtual**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   # o
   .venv\Scripts\activate     # Windows
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar base de datos**
   - Crear base de datos PostgreSQL
   - Actualizar `config.py` con la URL de conexión

5. **Ejecutar migraciones**
   ```bash
   python run_migrations.py
   ```

6. **Ejecutar la aplicación**
   ```bash
   python run.py
   ```

### Instalación con Docker

1. **Construir y ejecutar**
   ```bash
   docker-compose up --build
   ```

2. **Ejecutar migraciones**
   ```bash
   docker-compose exec web python run_migrations.py
   ```

## �� Configuración CORS

### **¿Qué es CORS?**
CORS (Cross-Origin Resource Sharing) es un mecanismo que permite que recursos restringidos en una página web sean solicitados desde otro dominio fuera del dominio desde el que se sirvió el primer recurso.

### **Configuración Automática**
El proyecto incluye configuración automática de CORS que:

- **Permite peticiones** desde `http://localhost:3000` (frontend Next.js)
- **Soporta métodos** HTTP estándar (GET, POST, PUT, PATCH, DELETE, OPTIONS)
- **Incluye headers** necesarios (Content-Type, Authorization)
- **Maneja preflight** requests automáticamente

### **Archivos de Configuración**
- **`app/utils/cors_config.py`**: Configuración principal de CORS
- **`config.py`**: Variables de entorno para CORS
- **`main.py`**: Aplicación de la configuración CORS

### **Variables de Entorno CORS**
```bash
# Orígenes permitidos (separados por coma)
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# Métodos HTTP permitidos
CORS_METHODS=GET,POST,PUT,PATCH,DELETE,OPTIONS

# Headers permitidos
CORS_ALLOW_HEADERS=Content-Type,Authorization,X-Requested-With
```

### **Prueba de CORS**
```bash
# Ejecutar script de prueba
python test_cors.py
```

## 🔐 Sistema de Autenticación

### **JWT (JSON Web Tokens)**
- **Algoritmo**: HS256
- **Expiración**: 30 minutos (configurable)
- **Almacenamiento**: localStorage en frontend

### **Endpoints de Autenticación**
- **`POST /api/auth/login`**: Iniciar sesión
- **`POST /api/auth/register`**: Registrar usuario

### **Protección de Rutas**
```python
from app.utils.auth_guard import require_auth

@app.route('/protected')
@require_auth
def protected_route():
    return jsonify({'message': 'Ruta protegida'})
```

## 🗄️ Base de Datos

### **Modelos Principales**
- **`User`**: Información de usuarios
- **`UserCredentials`**: Credenciales de autenticación
- **`Sign`**: Marcas registradas

### **Relaciones**
- **User ↔ UserCredentials**: 1:1 (comparten ID)
- **User ↔ Sign**: 1:N (un usuario puede tener múltiples marcas)

### **Transacciones**
```python
from app.utils.transaction_service import TransactionService

def create_user_transaction(session):
    # Lógica de creación
    pass

result = TransactionService.execute_in_transaction(create_user_transaction)
```

## 📊 API Endpoints

### **Autenticación**
- `POST /api/auth/login` - Login de usuario
- `POST /api/auth/register` - Registro de usuario

### **Marcas (Signs)**
- `POST /api/sign/create` - Crear marca
- `GET /api/sign/list` - Listar marcas
- `GET /api/sign/<id>` - Obtener marca por ID
- `PATCH /api/sign/<id>` - Actualizar marca
- `DELETE /api/sign/<id>` - Eliminar marca (soft delete)

## 🐳 Docker

### **Servicios**
- **`db`**: PostgreSQL 14
- **`web`**: Aplicación Flask

### **Puertos**
- **Backend**: `5000:5000`
- **PostgreSQL**: `5433:5432`

### **Volúmenes**
- **`postgres_data`**: Datos persistentes de PostgreSQL

## 🔧 Scripts Disponibles

```bash
# Ejecutar aplicación
python run.py

# Ejecutar migraciones
python run_migrations.py

# Probar CORS
python test_cors.py

# Desarrollo interactivo
python dev.py
```

## 🌍 Variables de Entorno

### **Archivo `.env` (crear manualmente)**
```bash
# Base de datos
DATABASE_URL=postgresql://signa:signa_pass@localhost:5433/signa_db

# Seguridad
SECRET_KEY=tu-clave-secreta-aqui
JWT_SECRET_KEY=tu-clave-jwt-aqui

# CORS
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
CORS_METHODS=GET,POST,PUT,PATCH,DELETE,OPTIONS
CORS_ALLOW_HEADERS=Content-Type,Authorization,X-Requested-With

# Configuración
FLASK_ENV=development
FLASK_DEBUG=True
BCRYPT_LOG_ROUNDS=12
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## 🧪 Testing

### **Prueba de CORS**
```bash
python test_cors.py
```

### **Prueba de Endpoints**
```bash
# Usar Postman, curl o similar
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -H "Origin: http://localhost:3000" \
  -d '{"username":"admin@signa.com","password":"admin123"}'
```

## 🚀 Despliegue

### **Desarrollo Local**
```bash
python run.py
```

### **Docker**
```bash
docker-compose up --build
```

### **Producción**
- Configurar variables de entorno de producción
- Usar servidor WSGI (gunicorn, uwsgi)
- Configurar proxy reverso (nginx)
- Configurar CORS para dominio de producción

## 🔒 Seguridad

- **JWT Tokens**: Autenticación stateless
- **bcrypt**: Hashing seguro de contraseñas
- **CORS**: Control de orígenes permitidos
- **Validación**: Validación de datos en entrada
- **Transacciones**: Operaciones atómicas de BD

## 🤝 Contribución

1. Fork el proyecto
2. Crear rama feature (`git checkout -b feature/AmazingFeature`)
3. Commit cambios (`git commit -m 'Add AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

## 📞 Soporte

- **Issues**: [GitHub Issues](link-al-repo)
- **Documentación**: [Wiki del Proyecto](link-al-wiki)
- **Email**: soporte@signa.com

---

**Desarrollado con ❤️ por el equipo Signa**