"""Configuración global del juego. Todos los valores ajustables viven acá."""
import os

# --- Base de datos (fase 3) ---
# Cada parámetro puede pisarse con una variable de entorno sin tocar código.
DB = {
    "host": os.environ.get("PGHOST", "localhost"),
    "port": int(os.environ.get("PGPORT", "5432")),
    "dbname": os.environ.get("PGDATABASE", "gran_escape"),
    "user": os.environ.get("PGUSER", "postgres"),
    "password": os.environ.get("PGPASSWORD", "postgres"),
    "timeout": 3,   # seg: si no responde, el juego sigue sin ranking
}
ARCHIVO_USUARIO = "usuario.json"   # acá se recuerda tu nombre de jugador

# --- Laberinto ---
# Tamaño en celdas lógicas. El grid final de tiles es (2*celdas + 1) por lado:
# 50x50 celdas -> 101x101 tiles. Subí esto con cuidado: el tiempo de partida
# crece mucho más rápido que el tamaño.
CELDAS_ANCHO = 50
CELDAS_ALTO = 50

# Braiding: porcentaje de callejones sin salida que se abren para crear rutas
# alternativas. 0.0 = laberinto "perfecto" (una sola ruta entre cada par de
# puntos: malo para persecuciones, un cazador bloquea un pasillo y no hay
# escapatoria posible). 0.15 a 0.30 es un buen rango.
PORCENTAJE_ATAJOS = 0.20

NUM_SALIDAS = 3
DISTANCIA_MIN_SALIDAS = 40  # en tiles, separación mínima entre salidas

# --- Partida ---
NUM_ESCAPISTAS = 3
NUM_CAZADORES = 2
TIEMPO_LIMITE = 240.0       # seg; si se agota, los que no salieron no escapan
RADIO_CAPTURA_EXTRA = 2.0   # margen en px sobre la suma de radios al capturar

# --- IA de los bots ---
VISION_CAZADOR_TILES = 8     # a esta distancia (y con línea de visión) persigue
PELIGRO_ESCAPISTA_TILES = 7  # a esta distancia el escapista "escucha" al cazador
EVITAR_TILES = 4             # radio alrededor del cazador que se esquiva al planear

# --- Multijugador (fase 4) ---
TICK_RED = 0.1              # seg entre sincronizaciones con la base (10 Hz)
SUAVIZADO_REMOTOS = 12.0    # interpolación de jugadores remotos (converge ~150 ms)
DIST_VALIDA_CAPTURA = 110.0  # px: separación máxima entre posiciones EN LA BASE
                             # para que un reclamo de captura sea válido
REFRESCO_LOBBY = 1.2        # seg entre consultas del lobby / sala de espera

# --- Radar / minimapa ---
MINIMAPA_PX_POR_TILE = 2
RADIO_RADAR_TILES = 14       # enemigos visibles en el minimapa hasta esta distancia
RADIO_ALERTA_TILES = 6       # enemigo más cerca que esto = radar en alerta

# --- Ventana y render ---
TILE = 32                # lado de cada tile en píxeles
ANCHO_VENTANA = 1280
ALTO_VENTANA = 720
FPS = 0                  # tope de cuadros por segundo; 0 = SIN límite (el juego
                         # corre a todo lo que dé la máquina). El movimiento usa
                         # dt, así que la velocidad del juego no cambia con los fps.

# --- Jugadores ---
VEL_ESCAPISTA = 280.0    # píxeles por segundo
VEL_CAZADOR = 300.0      # algo más rápidos; los escapistas compensan con el radar
RADIO_JUGADOR = 11       # radio del círculo; menor a TILE/2 para no rozar las paredes
AYUDA_CARRIL = 0.6       # qué tan fuerte te centra en el pasillo al avanzar
                         # (0 = sin ayuda; 0.5-0.8 dobla esquinas sin engancharse)

# --- Colores (R, G, B) ---
COLOR_FONDO = (12, 12, 16)
COLOR_MURO = (52, 58, 78)
COLOR_MURO_BORDE = (34, 38, 52)
COLOR_PASILLO = (18, 19, 26)
COLOR_SALIDA = (60, 220, 120)
COLOR_SALIDA_BORDE = (140, 255, 190)
COLOR_ESCAPISTA = (90, 170, 255)      # el humano
COLOR_ESCAPISTA_BOT = (70, 125, 205)
COLOR_CAZADOR = (235, 80, 80)
COLOR_ATRAPADO = (120, 120, 120)
COLOR_HUD = (235, 235, 235)
COLOR_HUD_SOMBRA = (0, 0, 0)
COLOR_TARJETA = (26, 28, 40)
