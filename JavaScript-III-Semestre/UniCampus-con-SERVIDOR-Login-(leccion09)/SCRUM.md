# Scrum - Metodología de Desarrollo

## Resumen

Este documento describe la implementación de la metodología **Scrum** utilizada en el desarrollo del proyecto UniCampus. El equipo trabajó de manera colaborativa siguiendo los principios ágiles de Scrum para lograr entregas incrementales y adaptarse a los cambios de manera eficiente.

## Equipo Scrum

### Miembros del Equipo
- **Lautaro Martinez** - Desarrollador Full Stack / Scrum Master
- **Leandro Orozco** - Desarrollador Full Stack
- **Gabriel Maculus** - Desarrollador Full Stack

### Roles y Responsabilidades

El equipo trabaja bajo un modelo **colaborativo e igualitario** donde todos los miembros tienen las mismas responsabilidades y contribuyen por igual en todas las áreas del proyecto.

#### Equipo Colaborativo
- **Desarrollo Full Stack** - Todos implementan funcionalidades del backend y frontend
- **Gestión del Proyecto** - Todos participan en la planificación y priorización
- **Calidad y Testing** - Todos son responsables de la calidad del código
- **Facilitación de Sprints** - Todos rotan responsabilidades de coordinación
- **Documentación** - Todos documentan su trabajo y aprenden juntos

**Principio fundamental**: El equipo aprende mutuamente, comparte conocimiento y se desarrolla en conjunto. No hay jerarquías, sino un equipo de pares comprometido con el éxito del proyecto.

## Duración de los Sprints

- **Duración**: 2 semanas (14 días)
- **Inicio**: Lunes
- **Cierre**: Viernes

## Ceremonias de Scrum

### 1. Sprint Planning
**Frecuencia**: Inicio de cada sprint (Lunes)  
**Duración**: 2 horas  
**Objetivos**:
- Revisar el Product Backlog
- Seleccionar las historias de usuario para el sprint
- Estimar la complejidad de las tareas
- Definir el objetivo del sprint
- Crear las tareas técnicas necesarias

### 2. Daily Standup
**Frecuencia**: Diariamente  
**Duración**: 15 minutos  
**Preguntas clave**:
- ¿Qué hice ayer?
- ¿Qué haré hoy?
- ¿Hay algún impedimento?

### 3. Sprint Review
**Frecuencia**: Final del sprint (Viernes)  
**Duración**: 1.5 horas  
**Actividades**:
- Demostración de las funcionalidades completadas
- Recopilación de feedback
- Actualización del Product Backlog

### 4. Sprint Retrospectiva
**Frecuencia**: Final del sprint (Viernes)  
**Duración**: 1 hora  
**Enfoque**:
- ¿Qué salió bien?
- ¿Qué se puede mejorar?
- Acciones de mejora para el próximo sprint

## Product Backlog

El Product Backlog contiene todas las funcionalidades y requisitos del proyecto, priorizados según el valor para el negocio:

### Historias de Usuario Implementadas

#### Sprint 1: Autenticación y Seguridad
- [ ] Como usuario, quiero registrarme en la plataforma
- [ ] Como usuario, quiero iniciar sesión con mis credenciales
- [ ] Como desarrollador, quiero encriptar las contraseñas de forma segura
- [ ] Como desarrollador, quiero implementar JWT para autenticación

#### Sprint 2: Base de Datos y Backend
- [ ] Como desarrollador, quiero configurar PostgreSQL
- [ ] Como desarrollador, quiero crear las tablas de usuarios
- [ ] Como desarrollador, quiero implementar endpoints REST
- [ ] Como desarrollador, quiero validar datos de entrada

#### Sprint 3: Frontend y Interfaz de Usuario
- [ ] Como usuario, quiero una página de inicio
- [ ] Como usuario, quiero un formulario de registro intuitivo
- [ ] Como usuario, quiero un formulario de login intuitivo
- [ ] Como usuario, quiero ver mi dashboard de estudiante

## Artefactos de Scrum

### Product Backlog
Lista de todas las funcionalidades, mejoras y correcciones necesarias para el proyecto, priorizadas por valor.

### Sprint Backlog
Conjunto de elementos del Product Backlog seleccionados para el sprint actual, más las tareas técnicas necesarias para completarlos.

### Incremento de Producto
El conjunto de funcionalidades completadas y potencialmente entregables al final de cada sprint.

## Métricas de Scrum

### Velocity (Velocidad del Equipo)
Mide la cantidad de trabajo completado por sprint. Ayuda a:
- Planificar sprints futuros
- Identificar tendencias
- Mejorar la estimación

### Burndown Chart
Gráfico que muestra el progreso del sprint:
- Eje vertical: trabajo pendiente (en puntos o horas)
- Eje horizontal: días del sprint
- Línea ideal vs línea real

### Burnup Chart
Alternativa al burndown, mostrando el trabajo completado en lugar del trabajo pendiente.

## Valores de Scrum

1. **Compromiso** - El equipo se compromete con los objetivos del sprint y entre sí
2. **Enfoque** - Concentrarse en el trabajo del sprint juntos
3. **Apertura** - Ser transparente y receptivo a las ideas de todos
4. **Respeto** - Valorar por igual las contribuciones de cada miembro
5. **Coraje** - Enfrentar desafíos juntos y proponer mejoras sin temor
6. **Colaboración** - Trabajar como un equipo unido sin jerarquías
7. **Aprendizaje Mutuo** - Enseñar y aprender de los compañeros continuamente

## Herramientas Utilizadas

- **Control de Versiones**: Git / GitHub
- **Gestión de Tareas**: Tablero Kanban (Trello, Jira, o similar)
- **Comunicación**: Reuniones síncronas y canales de chat
- **Documentación**: README, SCRUM.md, comentarios en código

## Definición de Hecho (Definition of Done)

Una tarea se considera completada cuando:

- ✅ El código ha sido escrito y revisado
- ✅ Se han ejecutado pruebas unitarias
- ✅ Se han ejecutado pruebas de integración
- ✅ El código cumple con los estándares de calidad
- ✅ La documentación ha sido actualizada
- ✅ Se ha realizado code review por al menos un compañero
- ✅ La funcionalidad está lista para producción

## Lecciones Aprendidas

### Beneficios Observados
- ✨ **Comunicación mejorada** - Al trabajar en igualdad, todos se sienten cómodos compartiendo ideas
- ✨ **Aprendizaje mutuo** - Cada miembro aprende de la experiencia y conocimiento de los otros
- ✨ **Entregas incrementales y regulares** - Todos comprometidos con el mismo objetivo
- ✨ **Capacidad de adaptarse a cambios** - Flexibilidad y colaboración del equipo
- ✨ **Mejor calidad del código** - Reviews entre pares con responsabilidad compartida
- ✨ **Mayor satisfacción del equipo** - Ambiente inclusivo y de igualdad
- ✨ **Rotación de tareas** - Todos aprendemos diferentes áreas del proyecto
- ✨ **Resiliencia del equipo** - Cualquiera puede continuar el trabajo de otro

### Áreas de Mejora
- 📈 Mejorar la estimación de tareas complejas
- 📈 Aumentar la cobertura de pruebas
- 📈 Documentar decisiones técnicas de manera más formal
- 📈 Implementar CI/CD para automatizar deploys
- 📈 Sistematizar el proceso de aprendizaje mutuo

## Próximos Pasos

- [ ] Consolidar backlog de próximos sprints
- [ ] Implementar mejoras identificadas en retrospectivas
- [ ] Aumentar cobertura de tests
- [ ] Configurar pipeline de CI/CD
- [ ] Planificar expansión de funcionalidades

---

**Última actualización**: 2026-06-10  
**Metodología**: Scrum con sprints de 2 semanas  
**Estado**: Proyecto en desarrollo activo
