# Signa Backend

Backend simplificado para gestión de marcas/signos con arquitectura limpia.

## �� Inicio Rápido

### Opción 1: Desarrollo Local (Recomendado para desarrollo)

#### 1. Activar entorno virtual
```bash
.venv\Scripts\activate
```

#### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

#### 3. Configurar base de datos PostgreSQL
- Instalar PostgreSQL localmente
- Crear base de datos `signa_db`
- Actualizar `config.py` con credenciales locales

#### 4. Ejecutar migraciones (solo la primera vez o cambios en BD)
```bash
python run_migrations.py
```

#### 5. Ejecutar la aplicación
```bash
python run.py
```

### Opción 2: Con Docker (Recomendado para despliegue)

#### 1. Levantar solo la base de datos
```bash
docker-compose up db -d
```

#### 2. Ejecutar migraciones
```bash
python run_migrations.py
```

#### 3. Ejecutar la aplicación
```bash
python run.py
```

#### 4. O ejecutar todo con Docker
```bash
docker-compose up --build
```

La aplicación estará disponible en: http://localhost:5000

## 📋 Scripts Disponibles

| Comando | Descripción |
|---------|-------------|
| `python run.py` | 🏃 Ejecutar aplicación (sin migraciones) |
| `python run_migrations.py` | 📋 Ejecutar migraciones de BD |
| `python dev.py` | 🎯 Script interactivo con opciones |

## 🐳 Comandos Docker

| Comando | Descripción |
|---------|-------------|
| `docker-compose up db -d` | 🗄️ Levantar solo PostgreSQL |
| `docker-compose up --build` | 🚀 Levantar aplicación completa |
| `docker-compose down` | 🛑 Detener todos los servicios |
| `docker-compose logs -f` | 📋 Ver logs en tiempo real |

## 🏗️ Arquitectura

- **Domain Layer**: Entidades y servicios de negocio
- **Infrastructure Layer**: Base de datos y API REST
- **Clean Architecture**: Separación clara de responsabilidades

## 🔑 Endpoints Disponibles

- **Auth**: `/api/auth/register`, `/api/auth/login`
- **Signs**: `/api/sign/create`, `/api/sign/<id>`, `/api/sign/list`

## 🗄️ Base de Datos

- **PostgreSQL** con SQLAlchemy ORM
- **Transacciones automáticas** para consistencia
- **Soft delete** con campo `status`
- **Docker**: Puerto 5433 (evita conflictos con PostgreSQL local)

## 🔧 Configuración

### Variables de Entorno (Docker)
- `POSTGRES_USER`: signa
- `POSTGRES_PASSWORD`: signa_pass
- `POSTGRES_DB`: signa_db
- `DATABASE_URL`: postgresql://signa:signa_pass@db/signa_db

### Configuración Local
Editar `config.py` para conectar a PostgreSQL local:
```python
SQLALCHEMY_DATABASE_URI = "postgresql://usuario:contraseña@localhost:5432/signa_db"
```

## 🚀 Despliegue

### Desarrollo
```bash
python run.py
```

### Producción con Docker
```bash
docker-compose -f docker-compose.yml up --build -d
```

### Solo Base de Datos
```bash
docker-compose up db -d
```