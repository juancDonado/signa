# 🎨 Signa Frontend

Frontend moderno para el sistema de gestión de marcas Signa, construido con Next.js 14, TypeScript y Tailwind CSS.

## ✨ Características

- **🔐 Autenticación JWT**: Sistema de login seguro con tokens
- **📱 Diseño Responsivo**: Optimizado para móviles y escritorio
- **🎯 Stepper Intuitivo**: Proceso de 3 pasos para registro de marcas
- **🎨 UI Moderna**: Diseño limpio y minimalista con Tailwind CSS
- **⚡ Next.js 14**: App Router y Server Components
- **🔒 Protección de Rutas**: Middleware de autenticación
- **📊 Dashboard Interactivo**: Estadísticas y acciones rápidas
- **🔄 Gestión de Estado**: Hook personalizado para autenticación
- **🌐 CORS Configurado**: Headers automáticos para desarrollo

## 🚀 Tecnologías

- **Framework**: Next.js 14 (App Router)
- **Lenguaje**: TypeScript
- **Estilos**: Tailwind CSS
- **Iconos**: Heroicons
- **Estado**: React Hooks + Custom Hooks
- **Navegación**: Next.js Navigation
- **Autenticación**: JWT + localStorage

## 📁 Estructura del Proyecto

```
src/
├── app/                    # App Router de Next.js
│   ├── dashboard/         # Página del dashboard
│   ├── register-sign/    # Página de registro de marcas
│   ├── signs/        # Página de gestión de marcas
│   ├── layout.tsx         # Layout principal
│   └── page.tsx           # Página de login
├── components/            # Componentes reutilizables
│   ├── ui/               # Componentes de UI base
│   ├── forms/            # Formularios
│   └── layout/           # Componentes de layout
├── services/              # Servicios de API
├── hooks/                 # Hooks personalizados (useAuth)
├── types/                 # Tipos TypeScript
└── lib/                   # Utilidades y helpers
```

## 🛠️ Instalación

### Prerrequisitos

- Node.js 18+ 
- npm o yarn
- Backend Signa ejecutándose en `http://localhost:5000`

### Pasos de Instalación

1. **Clonar el repositorio**
   ```bash
   git clone <url-del-repositorio>
   cd signa-frontend
   ```

2. **Instalar dependencias**
   ```bash
   npm install
   ```

3. **Configurar variables de entorno**
   ```bash
   # Crear archivo .env.local
   NEXT_PUBLIC_API_URL=http://localhost:5000/api
   ```

4. **Ejecutar en desarrollo**
   ```bash
   npm run dev
   ```

5. **Abrir en el navegador**
   ```
   http://localhost:3000
   ```

## 🔧 Scripts Disponibles

```bash
# Desarrollo
npm run dev          # Ejecutar en modo desarrollo
npm run build        # Construir para producción
npm run start        # Ejecutar en modo producción
npm run lint         # Ejecutar ESLint
npm run type-check   # Verificar tipos TypeScript
```

## 🔐 Sistema de Autenticación

### **Hook useAuth**
El proyecto utiliza un hook personalizado `useAuth` que maneja:

- **Estado de autenticación**: Verificación automática del token
- **Gestión de sesión**: Login/logout automático
- **Headers de autorización**: Inclusión automática del token en peticiones
- **Persistencia**: Almacenamiento en localStorage

### **Flujo de Autenticación**
1. Usuario ingresa credenciales
2. Backend valida y retorna JWT token
3. Token se almacena en localStorage
4. Todas las peticiones posteriores incluyen el token automáticamente
5. Logout elimina el token y redirige al login

### **Protección de Rutas**
```typescript
const { user, isLoading, isAuthenticated } = useAuth();

useEffect(() => {
  if (!isLoading && !isAuthenticated()) {
    router.push('/');
  }
}, [isLoading, isAuthenticated, router]);
```

## 🌐 Configuración CORS

### **Frontend (Next.js)**
El proyecto incluye configuración automática de CORS en `next.config.js`:

```javascript
async headers() {
  return [
    {
      source: '/api/:path*',
      headers: [
        { key: 'Access-Control-Allow-Credentials', value: 'true' },
        { key: 'Access-Control-Allow-Origin', value: '*' },
        { key: 'Access-Control-Allow-Methods', value: 'GET,DELETE,PATCH,POST,PUT' },
        { key: 'Access-Control-Allow-Headers', value: 'Authorization, Content-Type' },
      ],
    },
  ];
}
```

### **Backend (Flask)**
Asegúrate de que tu backend Flask tenga CORS configurado:

```python
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": ["http://localhost:3000"]}})
```

## 🎯 Funcionalidades Principales

### 1. **Sistema de Autenticación**
- Login con JWT
- Protección de rutas automática
- Manejo de sesiones persistente
- Logout seguro

### 2. **Dashboard Principal**
- Estadísticas de marcas
- Acciones rápidas
- Navegación intuitiva
- Información del usuario

### 3. **Registro de Marcas (Stepper)**
- **Paso 1**: Nombre de la marca
- **Paso 2**: Información del titular
- **Paso 3**: Resumen y confirmación

### 4. **Gestión de Marcas**
- Lista de marcas del usuario
- Acciones: Ver, Editar, Eliminar
- Estados: Activa/Inactiva
- Información completa

### 5. **Gestión de Usuarios**
- Acciones CRUD completas
- Estados de usuario
- Información detallada

## 🎨 Componentes Principales

### **useAuth Hook**
Hook personalizado para gestión de autenticación:
- `user`: Datos del usuario autenticado
- `token`: Token JWT actual
- `login()`: Función de login
- `logout()`: Función de logout
- `isAuthenticated()`: Verificar estado de autenticación
- `getAuthHeaders()`: Headers para peticiones autenticadas

### **Stepper**
Componente de navegación por pasos con indicadores visuales.

### **Sidebar**
Navegación lateral con menú principal y logout.

### **LoginForm**
Formulario de autenticación con validaciones.

### **MainLayout**
Layout principal que incluye sidebar y contenido.

## 🔌 Integración con Backend

El frontend se comunica con el backend a través de:

- **Base URL**: `http://localhost:5000/api`
- **Autenticación**: JWT Bearer Token (automático)
- **Endpoints**: REST API estándar
- **Formato**: JSON
- **CORS**: Configurado automáticamente

### **Headers Automáticos**
Todas las peticiones autenticadas incluyen automáticamente:
```typescript
{
  'Content-Type': 'application/json',
  'Authorization': `Bearer ${token}`
}
```

## 📱 Responsive Design

- **Mobile First**: Diseño optimizado para móviles
- **Breakpoints**: sm, md, lg, xl
- **Sidebar**: Colapsable en móviles
- **Grids**: Adaptativos según pantalla

## 🚀 Despliegue

### **Vercel (Recomendado)**
```bash
npm run build
# Conectar repositorio a Vercel
```

### **Docker**
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npm", "start"]
```

## 🔒 Seguridad

- **JWT Tokens**: Autenticación stateless
- **Protección de Rutas**: Middleware de autenticación automático
- **Validación de Inputs**: Validación en frontend y backend
- **HTTPS**: Recomendado en producción
- **CORS**: Configurado para desarrollo y producción

## 🧪 Testing

```bash
# Ejecutar tests
npm test

# Tests en modo watch
npm run test:watch

# Coverage
npm run test:coverage
```

## 📊 Performance

- **Lazy Loading**: Componentes cargados bajo demanda
- **Image Optimization**: Next.js Image component
- **Code Splitting**: Automático por rutas
- **Bundle Analysis**: `npm run analyze`

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

## 🎉 Agradecimientos

- Next.js Team por el framework
- Tailwind CSS por el sistema de estilos
- Heroicons por los iconos
- Comunidad de desarrolladores

---

**Desarrollado con ❤️ por el equipo Signa**
