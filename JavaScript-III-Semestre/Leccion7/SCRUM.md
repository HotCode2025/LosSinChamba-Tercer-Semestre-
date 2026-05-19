# 📋 Estructura Scrum — Lección 7: Problema de las N Reinas

## Información del Proyecto

| Campo              | Detalle                                      |
|--------------------|----------------------------------------------|
| **Proyecto**       | Problema de las N Reinas con Backtracking    |
| **Tecnologías**    | HTML, CSS (Glassmorphism), JavaScript        |
| **Herramientas**   | VS Code + Live Server, Discord               |
| **Equipo**         | 8 integrantes                                |
| **Sprint**         | 1 (entrega única)                            |

---

## 👥 Equipo

| Rol              | Integrante             |
|------------------|------------------------|
| **Scrum Master** | Lautaro Martinez       |
| **Desarrollador**| Gabriel Maculus        |
| **Desarrollador**| Leandro Orozco         |
| **Desarrollador**| Kevin Castilla         |
| **Desarrollador**| Mariano Rasguido       |
| **Desarrollador**| Ezequiel Diaz          |
| **Desarrollador**| Samira Baz             |
| **Desarrollador**| Jose Rodriguez         |

---

## 🗂️ Product Backlog

| ID  | Historia de Usuario                                                                 | Prioridad |
|-----|-------------------------------------------------------------------------------------|-----------|
| US1 | Como usuario quiero ingresar un valor N para definir el tamaño del tablero          | Alta      |
| US2 | Como usuario quiero ver el tablero generado dinámicamente en pantalla               | Alta      |
| US3 | Como usuario quiero que el algoritmo de backtracking resuelva el problema           | Alta      |
| US4 | Como usuario quiero ver la animación paso a paso del proceso de resolución          | Media     |
| US5 | Como usuario quiero ver el arreglo final con las posiciones de las reinas           | Media     |
| US6 | Como usuario quiero una interfaz moderna y agradable visualmente                    | Media     |
| US7 | Como usuario quiero recibir mensajes de estado (buscando, encontrado, sin solución) | Baja      |
| US8 | Como usuario quiero poder reiniciar el tablero sin recargar la página               | Baja      |

---

## 🏃 Sprint 1 — Planning

**Objetivo del Sprint:** Desarrollar una aplicación web funcional que resuelva el Problema de las N Reinas con visualización animada del backtracking.

**Duración:** 1 sesión de trabajo colaborativo  
**Comunicación:** Discord (canal de voz + texto)  
**Entorno:** VS Code con Live Server (previsualización en tiempo real compartida)

---

## ✅ Sprint Backlog — Tareas por Integrante

### 🟣 Lautaro Martinez — *Scrum Master + Desarrollador*
- Coordinó el equipo y organizó las tareas mediante Discord
- Facilitó la Daily Scrum y resolvió bloqueos entre integrantes
- Armó la estructura base del proyecto (`index.html`, `script.js`, `style.css`)
- Definió las variables CSS globales y el sistema de diseño (paleta, tipografía, tokens)
- Integró y revisó los aportes de cada integrante antes del merge final

---

### 🔵 Gabriel Maculus — *Desarrollador*
- Desarrolló el algoritmo principal de **backtracking** en `script.js`
- Implementó la función `isSafe()` para verificar conflictos entre reinas (filas, columnas y diagonales)
- Implementó la función recursiva `solveWithAnimation()` con `async/await`

---

### 🔵 Leandro Orozco — *Desarrollador*
- Construyó la función `renderEmptyBoard(n)` que genera el tablero dinámicamente desde JavaScript
- Aplicó el patrón de colores claros/oscuros al tablero como un tablero de ajedrez real
- Se encargó del posicionamiento y renderizado de las celdas con `grid`

---

### 🔵 Kevin Castilla — *Desarrollador*
- Desarrolló la lógica de **animación paso a paso** del algoritmo
- Implementó la función `sleep()` y el control del `animationDelay` según el valor de N
- Gestionó la variable `stopRequested` para cortar animaciones en curso al reiniciar

---

### 🔵 Mariano Rasguido — *Desarrollador*
- Diseñó y maquetó el **header** con el chip de categoría, título y subtítulo
- Implementó el efecto de línea luminosa (`header::after`) y el orbe decorativo (`header::before`)
- Trabajó en el sistema de tipografía con fuentes Inter y JetBrains Mono (Google Fonts)

---

### 🔵 Ezequiel Diaz — *Desarrollador*
- Construyó la **sección de controles**: input de N, validación de mínimo (≥ 8), botón Resolver y botón Reiniciar
- Implementó el manejo de errores con el mensaje `errorMsg` y la clase `.hidden`
- Conectó los eventos `click` del DOM con la lógica del algoritmo

---

### 🔵 Samira Baz — *Desarrolladora*
- Diseñó los estilos de las **cards** con efecto glassmorphism (`backdrop-filter`, `rgba`)
- Estilizó los botones con gradiente animado, efectos hover y estados deshabilitados
- Trabajó en el diseño responsivo y los efectos visuales de la sección de resultado (`resultArea`)

---

### 🔵 Jose Rodriguez — *Desarrollador*
- Desarrolló la **sección de resultados**: función `showResult(queens)` que genera el arreglo visual de posiciones
- Implementó las funciones `setStatus()`, `hideResult()` y `showResult()` para los mensajes de estado
- Estilizó los badges de posición del arreglo final con colores y fuente monoespaciada

---

## 📊 Sprint Review

| Historia | Estado       | Responsable(s)                    |
|----------|--------------|-----------------------------------|
| US1      | ✅ Completada | Ezequiel Diaz                     |
| US2      | ✅ Completada | Leandro Orozco                    |
| US3      | ✅ Completada | Gabriel Maculus                   |
| US4      | ✅ Completada | Kevin Castilla                    |
| US5      | ✅ Completada | Jose Rodriguez                    |
| US6      | ✅ Completada | Mariano Rasguido, Samira Baz      |
| US7      | ✅ Completada | Jose Rodriguez, Ezequiel Diaz     |
| US8      | ✅ Completada | Ezequiel Diaz, Kevin Castilla     |

**Resultado:** Todas las historias del sprint fueron completadas exitosamente. ✅

---

## 🔄 Sprint Retrospectiva

### ¿Qué salió bien?
- La comunicación por Discord (canal de voz) permitió coordinar en tiempo real sin fricciones
- Live Server facilitó ver los cambios de todos instantáneamente sin necesidad de builds
- La división de tareas fue clara desde el inicio gracias a la organización del Scrum Master

### ¿Qué se puede mejorar?
- Establecer una convención de nombres de variables y ramas desde el principio
- Documentar el código a medida que se escribe, no al final

### Compromisos para el próximo sprint
- Usar comentarios en el código durante el desarrollo, no después
- Definir el diseño visual (mockup) antes de arrancar con el CSS

---

## 🛠️ Herramientas utilizadas

| Herramienta     | Uso                                                   |
|-----------------|-------------------------------------------------------|
| **VS Code**     | Editor de código principal                            |
| **Live Server** | Previsualización en tiempo real del resultado         |
| **Discord**     | Comunicación por voz y texto entre los integrantes    |
| **Google Fonts**| Tipografías Inter y JetBrains Mono                   |
