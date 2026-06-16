# El Gran Escape

Juego multijugador asimétrico de persecución en un laberinto procedural:
**3 escapistas vs 2 cazadores**. Los escapistas ganan llegando a una de las 3
salidas; los cazadores, atrapándolos antes. Los mejores tiempos de escape se
registran en PostgreSQL y alimentan un ranking global.

Hecho con **Python + Pygame + PostgreSQL** como proyecto final.

## Cómo ejecutarlo

```
pip install -r requirements.txt
python main.py                   # abre el menú para elegir rol
python main.py --seed 1234       # misma seed = misma partida
python main.py --rol cazador     # entra directo a jugar, sin menú
```

| Tecla | Acción |
|---|---|
| ← → (en el menú) | elegir rol: escapista o cazador |
| ENTER | jugar single-player |
| J (en el menú) | multijugador online: lobby de salas |
| T / N (en el menú) | ver ranking / cambiar nombre |
| ↑ ↓ + ENTER (lobby) | unirse a una sala · C crea una sala (sos host) |
| ENTER (sala, host) | empezar: los puestos vacíos los juegan bots |
| WASD / flechas | moverse |
| ESC (jugando) | abandonar al menú |
| R (al terminar) | revancha / volver al lobby · M vuelve al menú |

Para jugar en LAN: todos apuntan a la misma base con `PGHOST` (la PC que
tiene PostgreSQL debe aceptar conexiones externas en `pg_hba.conf`).

La primera vez te pide tu nombre de jugador (queda en `usuario.json`).

**Base de datos**: el juego espera un PostgreSQL en `localhost:5432` (usuario
`postgres`, contraseña `postgres` — se puede cambiar con las variables de
entorno `PGHOST`, `PGPORT`, `PGUSER`, `PGPASSWORD`, `PGDATABASE`). La base
`gran_escape` y sus tablas **se crean solas** la primera vez que el juego
logra conectarse. Sin PostgreSQL el juego anda igual, pero no guarda tiempos.

Pruebas sin abrir ventana:
- `python tests_fase2.py` — 5 partidas completas entre bots (no necesita DB)
- `python tests_fase3.py` — guardado y rankings contra PostgreSQL real
- `python tests_fase4.py` — lobby, sincronización entre dos clientes de red
  y arbitraje atómico de capturas/escapes contra PostgreSQL real

## Estado del proyecto (plan por fases)

- [x] **Fase 1 — núcleo jugable**: laberinto procedural, jugador con colisiones,
  cámara/viewport, cronómetro y salidas.
- [x] **Fase 2 — el juego completo offline**: jugás de escapista o de cazador;
  el resto son bots con IA. Capturas, radar/minimapa, tiempo límite, menú y
  pantalla de resultados.
- [x] **Fase 3 — PostgreSQL**: nombre de jugador, cada partida terminada se
  guarda (participantes, tiempos, quién capturó a quién) y pantalla de
  ranking con los mejores tiempos de escape y los cazadores más efectivos.
- [x] **Fase 4 — multijugador online**: lobby de salas, hasta 3 escapistas y
  2 cazadores humanos; los puestos vacíos los juegan bots simulados por el
  host. Toda la sincronización pasa por PostgreSQL (ver abajo).

## Decisiones técnicas

**Laberinto procedural con seed.** Se genera con *recursive backtracking*
(iterativo) a partir de `random.Random(seed)`. La misma seed produce siempre
el mismo mapa, así que en la fase multijugador la partida solo guarda la seed
en la base: cada cliente regenera el laberinto localmente y nadie transmite
250.000 celdas.

**Braiding.** Un laberinto "perfecto" tiene exactamente una ruta entre cada
par de puntos: un cazador parado en un pasillo bloquea matemáticamente el
paso. Por eso, después de generar, se abre un porcentaje de los callejones
sin salida (`PORCENTAJE_ATAJOS` en [config.py](config.py)) para crear rutas
alternativas y que las persecuciones tengan escapatoria.

**Cámara/viewport.** El mapa (101×101 tiles de 32 px) no entra en pantalla:
se dibuja solo la ventana visible alrededor del jugador, lo que además
mantiene los FPS estables sin importar el tamaño del mapa.

**IA de los bots.** Los cazadores patrullan (a veces montan guardia cerca de
una salida) y persiguen al escapista que ven —distancia más línea de visión
libre—, recalculando el camino por BFS hacia su última posición conocida.
Los bots escapistas **no conocen el camino a la salida de memoria**: exploran
con preferencia por los bordes y recién cuando una salida entra en el alcance
de su radar la memorizan y van directo, esquivando la zona alrededor de los
cazadores que "escuchan" cerca. Sin esa limitación, el BFS perfecto los hacía
escapar en menos de 30 segundos y jugar de cazador no tenía gracia. Todos los
bots usan la misma física de movimiento que el humano: no atraviesan paredes
ni tienen ventajas imposibles.

**Radar y asimetría.** Los cazadores son un 9 % más rápidos; los escapistas
compensan con información: el minimapa muestra el laberinto y las salidas
siempre, pero a los enemigos solo cuando están a menos de 14 tiles — y el
borde del radar pulsa en rojo cuando alguno está encima tuyo. La lógica de
partida (`juego/partida.py`) no depende de Pygame, así que `tests_fase2.py`
simula partidas completas entre bots sin abrir ventana para verificar que
las reglas cierren.

**Persistencia tolerante a fallos.** Toda operación de base pasa por
`db/repositorio.py` y puede lanzar `DBNoDisponible`: el juego la atrapa,
avisa en pantalla ("sin conexión: el resultado no se guardó") y sigue — la
base nunca puede colgar ni romper una partida. La base y el esquema se crean
solos en el primer contacto (bootstrap idempotente en `db/conexion.py`).

**Los bots también van a la base.** Cada partida se guarda completa (los 5
participantes, con los bots marcados `es_bot = TRUE` y quién capturó a
quién), igual que será en la fase 4 con 5 humanos. Las vistas de ranking
excluyen a los bots, y el ranking de escapistas muestra la **mejor marca de
cada jugador** (`MIN(tiempo_escape) GROUP BY`), así un solo jugador no puede
llenar el top 10 a fuerza de repetir.

**Sincronización multijugador vía PostgreSQL (fase 4).** Toda la comunicación
entre jugadores pasa por la base de datos, sin servidor de juego propio:

- Un **hilo de red** por cliente ([db/red.py](db/red.py)) habla con la base
  cada 0,1 s: publica la posición propia con un upsert sobre la tabla
  **UNLOGGED** `posiciones` (sin WAL: updates baratos; los datos son efímeros
  y pueden perderse) y lee posiciones ajenas, flags y reloj de partida. El
  loop de Pygame nunca espera un round-trip.
- Las posiciones remotas llegan a 10 Hz y se dibujan con **suavizado
  exponencial**, así el movimiento se ve continuo.
- Las **capturas y escapes no los decide ningún cliente**: se *reclaman* y la
  base los arbitra con UPDATEs condicionales atómicos — si dos eventos
  compiten ("te atrapé" vs "llegué a la salida"), Postgres serializa y gana
  exactamente uno. El reclamo además **valida contra las posiciones que la
  base conoce** (cazador y presa a menos de `DIST_VALIDA_CAPTURA`), y el
  tiempo de escape lo cronometra el **reloj de la base** (`now() -
  iniciada_en`), no el de los clientes. Detalle en
  [db/esquema.sql](db/esquema.sql) y [db/repositorio.py](db/repositorio.py).
- El **lobby** también vive en la base: salas en estado `esperando`, slots por
  rol con índice único (dos clientes no pueden quedarse el mismo puesto), y
  el host **rellena los cupos vacíos con bots** que simula su propio cliente
  — para el resto, un bot es un jugador remoto más. El laberinto y los spawns
  salen de la seed: nadie transmite el mapa.
- El fin de partida lo puede declarar cualquier cliente: el UPDATE de cierre
  tiene un WHERE que solo es verdadero una vez y cuando corresponde.

Limitaciones asumidas (conscientes, documentadas para la defensa): funciona
bien en LAN o localhost (latencias de pocos ms); por internet las posiciones
se verían con retraso. El escape confía en la posición que reporta el propio
cliente (anti-cheat fuera de alcance). Si el host se desconecta en pleno
juego, sus bots se congelan y la partida termina por tiempo límite.

## Estructura

```
main.py            # loop y estados: nombre/menú/lobby/espera/partida/fin/ranking
config.py          # todas las constantes ajustables (+ conexión a la base)
tests_fase2.py     # simula partidas completas entre bots, sin ventana
tests_fase3.py     # guardado y rankings contra PostgreSQL real
tests_fase4.py     # lobby, sincronización y arbitraje multijugador
juego/
  laberinto.py     # generación procedural + braiding + salidas + BFS (+ demo ASCII)
  partida.py       # reglas single-player (independiente de Pygame)
  partida_multi.py # partida online: física local + remotos suavizados + bots del host
  entidad.py       # física común de movimiento y colisiones (humano y bots)
  bots.py          # IA: cazadores que patrullan/persiguen, escapistas que exploran
  camara.py        # viewport que sigue al jugador
  render.py        # tiles visibles, entidades, minimapa/radar, HUD y pantallas
db/
  esquema.sql      # tablas, vistas de ranking y arbitraje de capturas
  conexion.py      # conexión + bootstrap automático de base y esquema
  repositorio.py   # lobby, sincronización, arbitraje, partidas y rankings
  red.py           # hilo de red: sincroniza con la base cada 0,1 s
```

Demo del generador sin abrir el juego: `python -m juego.laberinto`
