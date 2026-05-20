# 🪨 Piedra · ✋ Papel · ✂️ Tijera — Edición Mortal

Una versión épica e interactiva del clásico juego de Piedra, Papel o Tijera, inspirada en la estética de los juegos de combate arcade (estilo Mortal Kombat). Desarrollado con HTML, CSS y JavaScript puro (Vanilla JS).

---

## 🎮 Modos de Juego

Al iniciar la aplicación serás recibido por la pantalla de selección de destino:

- **⚡ 1 Jugador (VS Máquina):** Enfréntate a la Inteligencia Artificial. Tú eliges tu runa, y la PC responderá de forma aleatoria con una pausa dramática antes de revelar su elección.
- **🩸 2 Jugadores (Local):** Modo "Hot-Seat". El Jugador 1 elige su arma en secreto, la pantalla se oculta, pasas el dispositivo al Jugador 2, y luego se resuelve el combate.

---

## 🔄 Controles y Botones

| Botón | Función |
|---|---|
| ⚡ 1 Jugador (VS Máquina) | Inicia partida contra la PC |
| 🩸 2 Jugadores (Local) | Inicia partida entre dos jugadores |
| Runa Piedra / Papel / Tijera | Elige tu arma en cada ronda |
| ⚔ Jugador 2 — LISTO | Confirmar turno en modo PvP (pantalla de espera) |
| 🔄 Reiniciar Partida | Reinicia la partida actual sin salir al menú |
| ↩ Volver al Menú (en partida) | Vuelve a la pantalla de inicio desde el juego |
| ⚔ REVANCHA | Reinicia la partida con el mismo modo |
| ↩ Volver al Menú (Game Over) | Regresa al menú principal desde la pantalla de Game Over |

---

## ⚙️ Sistema de Juego

- **Vida:** Cada jugador empieza con **4 puntos de vida**. Cada ronda perdida descuenta 1 punto.
- **Empates:** No se descuenta vida. La ronda se repite.
- **Victoria:** Gana quien deje a su rival sin vida primero.
- **Pips:** Los indicadores circulares bajo el contador de rondas muestran el historial de victorias de cada ronda.
- **IA del PC:** La máquina tiene una lógica balanceada: 35% de las veces elige el movimiento perdedor a propósito, y el resto elige al azar. El jugador tiene ~57% de chances de ganar cada ronda.

---

## 🗂️ Estructura del Proyecto

Mantené esta estructura para que todo funcione correctamente:

```text
/tu-proyecto
 ├── index.html            # Estructura del juego y UI principal
 ├── piedra-papel-tij.css  # Estilos de pantalla de inicio y botones de menú
 ├── p-p-t.js              # Lógica del motor, turnos, IA y resolución de daño
 └── readme.md             # Documentación del proyecto
```

---

## 🚀 Cómo usar

1. Descargá los 4 archivos y ponelos todos en la misma carpeta.
2. Abrí `index.html` en tu navegador.
3. Elegí tu modo de juego y ¡que comience el combate!

> No requiere instalación ni servidor. Funciona directamente en el navegador.

---

## 👥 Equipo & Metodología Scrum

**Modalidad de trabajo:** 8 integrantes · Live Server · Comunicación por Discord

| Rol | Integrante |
|---|---|
| 🏆 Scrum Master / Developer | Lautaro Martinez |
| 👨‍💻 Developer | Gabriel Maculus |
| 👨‍💻 Developer | Leandro Orozco |
| 👨‍💻 Developer | Kevin Castilla |
| 👨‍💻 Developer | Mariano Rasguido |
| 👨‍💻 Developer | Ezequiel Diaz |
| 👩‍💻 Developer | Samira Baz |
| 👨‍💻 Developer | Jose Rodriguez |

---

## 🗒️ Distribución de Tareas (Sprint Único)

### Lautaro Martinez — *Scrum Master / Developer*
- Coordinación general del equipo vía Discord
- Planificación del sprint y asignación de tareas
- Variables CSS globales (`--blood`, `--gold`, `--p1-color`, etc.) y reset base
- Referencias al DOM (`§4` en `p-p-t.js`)
- Sección del escenario (avatares, badge VS) en el HTML

### Gabriel Maculus — *Developer*
- Fondo visual: volcán, lava, gradientes animados (`#scene`) — CSS inline
- Animación de partículas de brasa (`#embers`) — CSS inline + `p-p-t.js §1`
- Sección HTML del fondo (`<div id="scene">`, `<div id="embers">`)

### Leandro Orozco — *Developer*
- Definición de armas y reglas (`CHOICES`, `COMBAT_LINES`) — `p-p-t.js §2`
- Estado global del juego (`state`, `MAX_HP`) — `p-p-t.js §3`

### Kevin Castilla — *Developer*
- Lógica de barras de vida (`updateHPBars`, `updatePips`, flashes de daño) — `p-p-t.js §6`
- Estilos CSS de HUD: barras de vida, colores, animación de pulso

### Mariano Rasguido — *Developer*
- Resolución del combate (`resolveCombat`) — `p-p-t.js §8`
- Sistema de reset y revancha (`resetGameUI`, `volverAlMenu`) — `p-p-t.js §12`
- Log de combate e historial de rondas — HTML + CSS inline

### Ezequiel Diaz — *Developer*
- Flujo del juego: `nextRound`, `showChoicesFor`, `showGameOver` — `p-p-t.js §9`
- Event listeners de los botones runa (§10) — `p-p-t.js`
- Panel de elección y turno en el HTML

### Samira Baz — *Developer*
- Pantalla de inicio y selección de modo (`startGame`) — `p-p-t.js §5`
- HTML y CSS de `#start-screen`, botones `mode-btn` — `piedra-papel-tij.css`
- Pantalla de Game Over — HTML y CSS

### Jose Rodriguez — *Developer*
- IA de la máquina (`getPcChoice`) con lógica balanceada — `p-p-t.js §7`
- Botón confirmar modo PvP (`confirmBtn`) — `p-p-t.js §11`
- Pantalla de espera entre turnos PvP — HTML + CSS inline

---

## 📋 Estructura del Sprint

```
Sprint único (proyecto académico)
│
├── 📌 Planning
│   ├── Definición del producto: Piedra Papel Tijera edición arcade
│   ├── Scrum Master: Lautaro Martinez
│   └── Comunicación: Discord + Live Server compartido
│
├── 🔨 Development (tareas paralelas)
│   ├── HTML base y estructura DOM ............ Lautaro Martinez
│   ├── CSS variables y estilos globales ....... Lautaro Martinez
│   ├── Fondo visual y partículas .............. Gabriel Maculus
│   ├── Definición de armas y estado ........... Leandro Orozco
│   ├── Barras de vida y HUD .................. Kevin Castilla
│   ├── Pantalla de inicio y Game Over ......... Samira Baz
│   ├── Lógica de combate y reset .............. Mariano Rasguido
│   ├── Flujo del juego y listeners ............ Ezequiel Diaz
│   └── IA, botón confirmar PvP ............... Jose Rodriguez
│
└── ✅ Review & Demo
    └── Revisión conjunta vía Live Server + Discord
```
