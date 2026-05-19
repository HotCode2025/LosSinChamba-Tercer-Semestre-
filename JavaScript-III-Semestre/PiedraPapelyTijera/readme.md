# 🪨 Piedra · ✋ Papel · ✂️ Tijera — Edición Mortal KombAT

Una versión épica e interactiva del clásico juego de Piedra, Papel o Tijera, inspirada en la estética de los juegos de combate arcade (estilo Mortal Kombat). Desarrollado con HTML, CSS y JavaScript puro.
---

# Modos de Juego

Al iniciar la aplicación serás recibido por la pantalla de selección de destino:

⚡ 1 Jugador (VS Máquina): Enfréntate a la IA. Vos eliges tu arma , y la PC responderá de forma aleatoria con una pausa antes de revelar su elección.
🩸 2 Jugadores (Local): El Jugador 1 elige su arma en secreto, la pantalla se oculta, pasas el dispositivo al Jugador 2, y luego se resuelve el combate.

---

# Controles y Botones

| Botón | Función |

⚡ 1 Jugador (VS Máquina) | Inicia partida contra la PC 
2 Jugadores (Local) | Inicia partida entre dos jugadores 
ARMA: Piedra / Papel / Tijera | Elige tu arma en cada ronda 
⚔ Jugador 2 — LISTO | Confirmar turno en modo PvP (pantalla de espera) 
↩ Volver al Menú (en partida) | Vuelve a la pantalla de inicio desde el juego 
⚔ REVANCHA | Reinicia la partida con el mismo modo |
↩ Volver al Menú (Game Over) | Regresa al menú principal desde la pantalla de Game Over 

---

## ⚙️ Sistema de Juego

- Vida:Cada jugador empieza con 4 puntos de vida. Cada ronda perdida descuenta 1 punto.
- Empates: No se descuenta vida. La ronda se repite.
- Victoria: Gana quien deje a su rival sin vida primero.
- Pips: Los indicadores circulares bajo el contador de rondas muestran el historial de victorias de cada ronda.
- IA del PC:La máquina elige de forma aleatoria entre Piedra, Papel y Tijera.

---

# Estructura del Proyecto

/Piedra-Papel y Tijera Ed.Mortal
 ├── index.html            # Estructura del juego  principal
 ├── piedra-papel-tij.css  # Estilos de pantalla de inicio y botones de menú
 ├── p-p-t.js              # Lógica del motor, turnos, IA y resolución de daño
 └── readme.md             # Documentación del proyecto


