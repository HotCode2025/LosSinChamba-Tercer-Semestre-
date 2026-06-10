# UniCampus - Student Portal

## Descripción
UniCampus es un **proyecto de práctica** desarrollado por estudiantes para aplicar conocimientos adquiridos en la carrera, así como aprendizajes autodidactas. El proyecto utiliza metodología Scrum para gestionar el desarrollo de manera colaborativa. 

La aplicación es un portal de estudiantes que permite a los usuarios registrarse, autenticarse de forma segura y acceder a su portal personalizado. A través de este proyecto, el equipo práctica conceptos de desarrollo full stack, seguridad, bases de datos y trabajo en equipo.

**Estado del Proyecto**: ⚠️ En desarrollo activo - El proyecto aún no está finalizado.

## Propósito Educativo

Este proyecto tiene como objetivos:

- 📚 **Aplicar conocimientos de carrera** - Poner en práctica conceptos de desarrollo web, bases de datos, seguridad
- 🎓 **Aprendizaje autodidacta** - Investigar y aprender nuevas tecnologías por propia iniciativa
- 👥 **Trabajo en equipo** - Colaborar bajo metodología Scrum con responsabilidades compartidas
- 🔄 **Iteración continua** - Mejorar el código y las prácticas constantemente
- 🧠 **Crecimiento profesional** - Desarrollar habilidades técnicas y blandas

## Estado del Proyecto

🚧 **En desarrollo activo**

El proyecto aún **no está finalizado**. Se encuentran en progreso:
- [ ] Funcionalidades del dashboard de estudiante
- [ ] Integración de más servicios
- [ ] Pruebas exhaustivas
- [ ] Despliegue en producción


- 🔐 Autenticación segura con JWT (JSON Web Tokens)
- 🔒 Contraseñas encriptadas con bcrypt
- 📝 Sistema de registro e inicio de sesión
- 🗄️ Base de datos PostgreSQL
- 🌐 API REST con Express.js
- 🔄 CORS habilitado para solicitudes cross-origin

## Stack Tecnológico

### Backend
- **Express.js** - Framework web para Node.js
- **Node.js** - Runtime de JavaScript
- **PostgreSQL** - Sistema de gestión de base de datos relacional

### Autenticación y Seguridad
- **JWT** - JSON Web Tokens para autenticación
- **bcrypt** - Encriptación de contraseñas

### Utilidades
- **CORS** - Control de acceso cross-origin
- **dotenv** - Gestión de variables de entorno

## Frontend
- **HTML5** - Estructura
- **CSS3** - Estilos
- **JavaScript Vanilla** - Interactividad

## Instalación

1. Clonar el repositorio:
```bash
git clone <URL-del-repositorio>
cd unicampus
```

2. Instalar dependencias:
```bash
npm install
```

3. Configurar variables de entorno:
Crear un archivo `.env` con las siguientes variables:
```
DATABASE_URL=postgresql://usuario:contraseña@localhost:5432/unicampus
JWT_SECRET=tu_clave_secreta_aqui
PORT=3000
```

4. Inicializar la base de datos:
```bash
# Ejecutar migrations o scripts de setup según corresponda
```

## Uso

Iniciar el servidor:
```bash
npm start
```

El servidor se ejecutará en `http://localhost:3000`

## Estructura del Proyecto

```
unicampus/
├── server.js          # Punto de entrada del servidor
├── app.js             # Configuración de Express
├── database.js        # Configuración de base de datos
├── index.html         # Página principal
├── login.html         # Página de inicio de sesión
├── login.js           # Lógica de inicio de sesión
├── register.html      # Página de registro
├── register.js        # Lógica de registro
├── styles.css         # Estilos globales
├── package.json       # Dependencias del proyecto
└── README.md          # Este archivo
```

## Equipo de Desarrollo

Este proyecto fue desarrollado mediante metodología **Scrum** por:

- **Lautaro Martinez** - Desarrollador Full Stack
- **Leandro Orozco** - Desarrollador Full Stack
- **Gabriel Maculus** - Desarrollador Full Stack

## Metodología

El proyecto utiliza **Scrum** como metodología de desarrollo, permitiendo:
- Desarrollo iterativo e incremental
- Entregas regulares de funcionalidades
- Adaptación flexible a cambios de requisitos
- Colaboración continua entre miembros del equipo

## Seguridad

- Las contraseñas se encriptan usando bcrypt antes de almacenarse
- Los tokens JWT se utilizan para mantener sesiones seguras
- CORS está configurado para controlar el acceso a recursos

## Próximos Pasos / Mejoras Futuras

- [ ] Implementar recuperación de contraseña
- [ ] Agregar validación de email
- [ ] Dashboard de estudiante mejorado
- [ ] Sistema de notificaciones
- [ ] Integración con Google/OAuth

## Licencia

Este proyecto es de código educativo.

---

**Última actualización**: 2026-06-10
