# 📋 SCRUM — Piedra · Papel · Tijera (Edición Mortal)

> **Metodología:** Scrum adaptado a proyecto académico  
> **Modalidad:** 8 integrantes · Live Server compartido · Comunicación por Discord  
> **Sprint:** Único (desarrollo completo del proyecto)

---

## 👥 Equipo Scrum

| Rol | Integrante |
|---|---|
| 🏆 **Scrum Master / Developer** | Lautaro Martinez |
| 👨‍💻 **Developer** | Gabriel Maculus |
| 👨‍💻 **Developer** | Leandro Orozco |
| 👨‍💻 **Developer** | Kevin Castilla |
| 👨‍💻 **Developer** | Mariano Rasguido |
| 👨‍💻 **Developer** | Ezequiel Diaz |
| 👩‍💻 **Developer** | Samira Baz |
| 👨‍💻 **Developer** | Jose Rodriguez |

---

## 🔄 Flujo del Sprint

```
┌─────────────────────────────────────────────────────────────────┐
│                        SPRINT ÚNICO                             │
│                                                                 │
│  1. SPRINT PLANNING  →  2. DESARROLLO  →  3. DAILY (Discord)   │
│         ↓                                        ↓             │
│  Definir tareas y           Live Server     Sincronización      │
│  asignar roles              compartido      diaria del equipo   │
│                                  ↓                             │
│                        4. SPRINT REVIEW & DEMO                 │
│                        Revisión conjunta del resultado final    │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📌 Sprint Planning

### Objetivo del Sprint
Desarrollar un juego completo de **Piedra, Papel o Tijera** con estética arcade (inspiración Mortal Kombat), incluyendo:
- Modo 1 Jugador (vs IA) y Modo 2 Jugadores (local)
- Sistema de vida con 4 HP por jugador
- Efectos visuales: partículas, animaciones, shake de pantalla
- Pantalla de inicio, Game Over y revancha
- Diseño responsivo

### Herramientas acordadas
| Herramienta | Uso |
|---|---|
| **Live Server** (VS Code) | Visualización en tiempo real compartida |
| **Discord** | Comunicación, revisiones y daily standups |
| **HTML + CSS + JS Vanilla** | Stack tecnológico del proyecto |

---

## 🗒️ Product Backlog → Sprint Backlog

| ID | Historia de Usuario | Responsable | Estado |
|---|---|---|---|
| US-01 | Como jugador quiero ver una pantalla de inicio con selección de modo | Samira Baz | ✅ Done |
| US-02 | Como jugador quiero un fondo animado tipo volcán | Gabriel Maculus | ✅ Done |
| US-03 | Como jugador quiero partículas de brasa cayendo | Gabriel Maculus | ✅ Done |
| US-04 | Como jugador quiero poder elegir Piedra, Papel o Tijera | Ezequiel Diaz | ✅ Done |
| US-05 | Como jugador quiero ver mis puntos de vida actualizarse | Kevin Castilla | ✅ Done |
| US-06 | Como jugador quiero enfrentarme a la IA en modo 1 jugador | Jose Rodriguez | ✅ Done |
| US-07 | Como jugador quiero jugar vs otro jugador en el mismo dispositivo | Ezequiel Diaz | ✅ Done |
| US-08 | Como jugador quiero ver quién ganó la ronda y el combate | Mariano Rasguido | ✅ Done |
| US-09 | Como jugador quiero un historial de rondas | Mariano Rasguido | ✅ Done |
| US-10 | Como jugador quiero poder regresar al menú o revanchar | Mariano Rasguido | ✅ Done |
| US-11 | Como jugador quiero efectos de shake y flash al recibir daño | Kevin Castilla | ✅ Done |
| US-12 | Como jugador quiero ver la pantalla de Game Over con el ganador | Samira Baz | ✅ Done |

---

## 🤝 Cómo Trabajamos

El equipo trabajó de forma **totalmente remota y colaborativa**. Cada integrante tenía el proyecto abierto en su propio editor con **Live Server** activo, lo que permitía ver los cambios reflejados en el navegador en tiempo real sin necesidad de recargar manualmente.

La comunicación se centralizó en **Discord**, donde el equipo tenía canales para:
- Compartir avances y capturas de pantalla
- Resolver dudas sobre el código
- Coordinar quién trabajaba en cada parte para evitar pisar el trabajo del otro
- Hacer los daily standups informales antes de cada sesión

**Lautaro Martinez**, como Scrum Master, arrancaba cada sesión asignando tareas y al final revisaba que todo encajara sin conflictos entre los archivos.

El desarrollo fue **modular**: cada uno se encargó de una sección específica del HTML, CSS o JS, de modo que el trabajo fuera paralelo y no se generaran conflictos. Al terminar cada parte, se compartía en Discord para que el resto pudiera ver el resultado y dar feedback.

---

## 🔨 Distribución de Tareas por Integrante

---

### 🏆 Lautaro Martinez — *Scrum Master / Developer*

**Cómo trabajó:**  
Como Scrum Master, Lautaro fue el punto de contacto del equipo. Organizaba las sesiones de trabajo por Discord, distribuía las tareas al inicio de cada jornada y verificaba que los archivos no tuvieran conflictos al juntarse. Además, contribuyó directamente al código encargándose de la base estructural del proyecto: las variables CSS globales que todo el equipo usaría como referencia, y la organización centralizada de las referencias al DOM en el JS.

**Responsabilidades Scrum:**
- Coordinación general del equipo
- Facilitación de dailys por Discord
- Eliminación de bloqueos (impedimentos)
- Asignación y seguimiento de tareas del sprint

**Tareas técnicas:**
- Variables CSS globales (`--blood`, `--gold`, `--p1-color`, `--hp-green`, etc.)
- Reset y estilos base del `body`
- Referencias al DOM (sección `§4` en `p-p-t.js`)
- Sección del escenario en HTML: avatares de jugadores, badge `VS`

**Archivos afectados:** `index.html` (CSS `:root`, `body`, `#stage`), `p-p-t.js` (§4)

---

### 👨‍💻 Gabriel Maculus — *Developer*

**Cómo trabajó:**  
Gabriel se encargó de toda la parte visual del fondo del juego. Trabajó de forma independiente en el CSS y en el JS de las partículas, probando distintas configuraciones de colores, velocidades y tamaños de brasas hasta lograr el efecto de atmósfera de volcán. Subió avances por Discord para que el equipo validara que el resultado visual encajara con la estética del juego.

**Tareas técnicas:**
- Fondo visual: volcán, gradientes de lava, columnas de piedra (`#scene`)
- Animaciones `lavaFlicker` y patrón de columnas con `::before` / `::after`
- Sistema de partículas de brasa: generación dinámica de `.ember` en JS
- Animación `emberRise` (movimiento ascendente con drift lateral)

**Archivos afectados:** `index.html` (CSS `#scene`, `.ember`, `@keyframes emberRise`), `p-p-t.js` (§1 `spawnEmbers`)

---

### 👨‍💻 Leandro Orozco — *Developer*

**Cómo trabajó:**  
Leandro definió el corazón lógico del juego: las reglas de qué le gana a qué, y la estructura del estado global. Esto fue lo primero que se implementó, ya que el resto del equipo necesitaba saber cómo estaba organizado el estado (`state`) para construir sus funciones encima. Lo compartó rápido en Discord para que todos pudieran arrancar en paralelo.

**Tareas técnicas:**
- Definición del objeto `CHOICES` con emojis, nombres y reglas de victoria
- Definición de `COMBAT_LINES` con mensajes narrativos por combinación
- Objeto `state` con toda la estructura del estado del juego (`hp`, `round`, `phase`, `history`)
- Constante `MAX_HP`

**Archivos afectados:** `p-p-t.js` (§2 Definición de armas, §3 Estado del juego)

---

### 👨‍💻 Kevin Castilla — *Developer*

**Cómo trabajó:**  
Kevin se encargó de todo lo visual relacionado con la vida de los jugadores. Probó distintas transiciones y colores para las barras de HP hasta que quedaron fluidas y claras. También implementó los efectos de daño (flash y shake), que le daban más impacto al combate. Iba mostrando el progreso en el canal de Discord para recibir feedback del equipo.

**Tareas técnicas:**
- Función `updateHPBars()`: actualización dinámica de barras con clases `full`, `medium`, `low`
- Función `triggerDamageFlash()`: efecto visual al recibir daño
- Función `shakeScreen()`: animación de sacudida de pantalla
- CSS de HUD: `.hp-bar-wrap`, `.hp-bar`, `@keyframes hpPulse`, `@keyframes damageFlash`
- Función `setAvatar()`: mostrar/ocultar elección del jugador con animación `reveal`

**Archivos afectados:** `index.html` (CSS HUD), `p-p-t.js` (§6)

---

### 👨‍💻 Mariano Rasguido — *Developer*

**Cómo trabajó:**  
Mariano tuvo una de las tareas más centrales: la función que resuelve cada ronda del combate. Trabajó sobre el objeto `state` que definió Leandro y coordinó con Ezequiel para que el flujo del juego (siguiente ronda, game over) encajara bien. También se ocupó del historial de rondas y de los botones de reset/revancha.

**Tareas técnicas:**
- Función `resolveCombat()`: lógica central de resolución (empate, victoria P1, victoria P2), descuento de HP, logs
- Función `resetGameUI()`: reinicio completo del estado y la interfaz
- Función `volverAlMenu()`: retorno al menú principal
- Función `addHistoryEntry()`: registro visual de cada ronda con iconos
- Función `showResultFlash()`: destello de resultado (win/draw)
- CSS del log de combate e historial: `#combat-log`, `#history`, `.history-entry`

**Archivos afectados:** `index.html` (CSS historial y log), `p-p-t.js` (§8, §12)

---

### 👨‍💻 Ezequiel Diaz — *Developer*

**Cómo trabajó:**  
Ezequiel implementó el flujo general del juego y los controles del jugador. Trabajó en estrecha coordinación con Mariano (combate) y Jose (modo PvP), ya que sus funciones estaban conectadas. Fue quien armó la lógica de turnos del modo de 2 jugadores, asegurándose de que la elección del Jugador 1 quedara oculta antes de pasarle el dispositivo al Jugador 2.

**Tareas técnicas:**
- Función `nextRound()`: avance de ronda y reseteo de selecciones
- Función `showChoicesFor(player)`: mostrar panel de elección al jugador correcto
- Función `showGameOver()`: determinar y mostrar al ganador final
- Event listeners de los botones `.rune-btn` (piedra/papel/tijera) para P1 y P2
- Lógica de turno PvP: ocultamiento de elección de P1 antes de turno de P2
- CSS del panel de elección y botones runa

**Archivos afectados:** `index.html` (HTML `#choice-panel`, CSS `.rune-btn`), `p-p-t.js` (§9, §10)

---

### 👩‍💻 Samira Baz — *Developer*

**Cómo trabajó:**  
Samira se enfocó en la experiencia de entrada y salida del juego: la pantalla de inicio y la de Game Over. Diseñó los botones de modo con el efecto de brillo animado y la tipografía temática, y también implementó la lógica JS que arranca el juego según el modo elegido. Fue la responsable del CSS externo (`piedra-papel-tij.css`).

**Tareas técnicas:**
- Función `startGame(mode)`: inicialización según modo PvE o PvP
- HTML completo de `#start-screen`: títulos, subtítulo y botones de modo
- CSS de `#start-screen`: overlay, `title-mortal`, `subtitle-kombat`, animación `pulseTitle`
- Estilos de `.mode-btn` con efecto `::before` de brillo y variantes `.pve` / `.pvp`
- HTML y CSS de `#gameover`: nombre del ganador, "FATALIDAD", botones de revancha y menú
- Estilos de `.menu-btn` y `.gameover-buttons`

**Archivos afectados:** `index.html` (HTML `#start-screen`, `#gameover`), `piedra-papel-tij.css`, `p-p-t.js` (§5)

---

### 👨‍💻 Jose Rodriguez — *Developer*

**Cómo trabajó:**  
Jose implementó la IA del modo 1 jugador y el sistema de transición de turnos en el modo PvP. También se ocupó de la función que actualiza el mensaje central del juego (`setAnnounce`), que es la que le da feedback narrativo al jugador en cada momento. Trabajó coordinado con Ezequiel para que el botón de confirmación del Jugador 2 encajara bien con el flujo de turnos.

**Tareas técnicas:**
- Función `getPcChoice()`: IA aleatoria del modo 1 jugador
- Listener del botón `#confirm-btn` (PvP): transición de turno P1 → P2
- Función `setAnnounce()`: actualización del mensaje central con color y glow dinámico
- HTML de la pantalla de espera PvP (`#waiting-screen`, `.waiting-text`, `#confirm-btn`)
- CSS de `#waiting-screen` y animación `waitingPulse`

**Archivos afectados:** `index.html` (HTML `#waiting-screen`, CSS), `p-p-t.js` (§7, §11)

---

## 📅 Daily Standups (simulado por Discord)

Cada jornada de trabajo el equipo respondía en Discord:

```
✅ ¿Qué hice ayer?
🔨 ¿Qué voy a hacer hoy?
🚧 ¿Tengo algún bloqueo?
```

Lautaro Martinez, como Scrum Master, consolidaba las respuestas y coordinaba
si algún integrante necesitaba ayuda o tenía conflictos en el código.

---

## ✅ Sprint Review

**Demo realizada con Live Server** — todos los integrantes pudieron visualizar
el resultado final en tiempo real desde sus equipos.

### Criterios de aceptación cumplidos
- [x] Pantalla de inicio con selección de modo
- [x] Modo 1 Jugador (vs IA) funcional
- [x] Modo 2 Jugadores (local/hot-seat) funcional
- [x] Sistema de 4 HP por jugador con barras animadas
- [x] Efectos visuales: brasa, lava, shake, flash de daño
- [x] Historial de rondas y log de combate
- [x] Pantalla de Game Over con revancha y vuelta al menú
- [x] Diseño responsivo (mobile y desktop)

---

## 🔁 Sprint Retrospective

| ¿Qué salió bien? | ¿Qué mejoraría? |
|---|---|
| Comunicación fluida por Discord | Definir antes la nomenclatura de IDs y clases |
| Live Server permitió ver cambios en tiempo real | Dividir el CSS en archivos separados por módulo |
| División de tareas clara y sin superposición | Usar Git con ramas para evitar conflictos |
| Buen resultado visual final | Documentar mientras se desarrolla, no al final |

---

## 🗂️ Mapa de Responsabilidades por Archivo

### `index.html`
| Sección | Responsable |
|---|---|
| CSS `:root` y `body` | Lautaro Martinez |
| CSS `#scene` (volcán y lava) | Gabriel Maculus |
| CSS `#embers` y `.ember` | Gabriel Maculus |
| CSS `#hud`, `.hp-bar-*` | Kevin Castilla |
| CSS `.rune-btn` y `#choice-panel` | Ezequiel Diaz |
| CSS `#waiting-screen` | Jose Rodriguez |
| CSS `#gameover` | Samira Baz |
| CSS historial y log | Mariano Rasguido |
| HTML `#start-screen` | Samira Baz |
| HTML `#hud` | Kevin Castilla |
| HTML `#stage` (avatares, VS) | Lautaro Martinez |
| HTML `#choice-panel` y `.rune-btn` | Ezequiel Diaz |
| HTML `#waiting-screen` | Jose Rodriguez |
| HTML `#gameover` | Samira Baz |

### `p-p-t.js`
| Sección | Responsable |
|---|---|
| §1 Partículas de brasa | Gabriel Maculus |
| §2 Definición de armas | Leandro Orozco |
| §3 Estado del juego | Leandro Orozco |
| §4 Referencias al DOM | Lautaro Martinez |
| §5 Selección de modo y arranque | Samira Baz |
| §6 Lógica de UI y barras de vida | Kevin Castilla |
| §7 IA de la máquina | Jose Rodriguez |
| §8 Resolver combate | Mariano Rasguido |
| §9 Flujo del juego | Ezequiel Diaz |
| §10 Listeners botones runa | Ezequiel Diaz |
| §11 Botón confirmar (PvP) | Jose Rodriguez |
| §12 Reset / Rematch / Menú | Mariano Rasguido |

### `piedra-papel-tij.css`
| Sección | Responsable |
|---|---|
| Pantalla de inicio y botones de modo | Samira Baz |
| Botón de menú (Game Over) | Samira Baz |
