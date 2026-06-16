"""Dibujo de todo lo visible: laberinto, entidades, minimapa/radar, HUD y
las pantallas de menú y fin de partida.

Solo se dibujan los tiles dentro del viewport: en mapas grandes, recorrer
el grid completo en cada frame mata los FPS.
"""
import math

import pygame

import config
from juego.laberinto import MURO, SALIDA

# ---------------------------------------------------------------------- #
# Mundo
# ---------------------------------------------------------------------- #


def crear_fondo(laberinto):
    """Pre-dibuja el laberinto COMPLETO una sola vez por partida.

    Antes se dibujaban los ~900 tiles visibles con draw.rect en cada frame
    (unas 1.800 llamadas): eso costaba más que todo el resto del juego junto
    y tiraba los FPS abajo de 60. Ahora por frame se hace UN solo blit del
    recorte visible de esta superficie."""
    tile = config.TILE
    fondo = pygame.Surface((laberinto.ancho * tile, laberinto.alto * tile))
    fondo.fill(config.COLOR_FONDO)
    for ty in range(laberinto.alto):
        fila = laberinto.grid[ty]
        for tx in range(laberinto.ancho):
            rect = pygame.Rect(tx * tile, ty * tile, tile, tile)
            if fila[tx] == MURO:
                pygame.draw.rect(fondo, config.COLOR_MURO, rect)
                pygame.draw.rect(fondo, config.COLOR_MURO_BORDE, rect, 2)
            elif fila[tx] == SALIDA:
                pygame.draw.rect(fondo, config.COLOR_SALIDA, rect)
                pygame.draw.rect(fondo, config.COLOR_SALIDA_BORDE, rect, 3)
            else:
                pygame.draw.rect(fondo, config.COLOR_PASILLO, rect)
    return fondo


def dibujar_laberinto(pantalla, fondo, camara):
    """Un solo blit del recorte del mundo que entra en la ventana."""
    pantalla.blit(fondo, (0, 0),
                  pygame.Rect(int(camara.x), int(camara.y),
                              camara.ancho_ventana, camara.alto_ventana))


def dibujar_entidades(pantalla, partida, camara):
    for e in partida.entidades:
        if e.escapado:          # ya no está en el laberinto
            continue
        px, py = camara.a_pantalla(e.x, e.y)
        if (px < -50 or px > config.ANCHO_VENTANA + 50
                or py < -50 or py > config.ALTO_VENTANA + 50):
            continue
        px, py = int(px), int(py)
        if e.atrapado:
            pygame.draw.circle(pantalla, config.COLOR_ATRAPADO, (px, py), e.radio)
            pygame.draw.line(pantalla, config.COLOR_CAZADOR,
                             (px - 6, py - 6), (px + 6, py + 6), 3)
            pygame.draw.line(pantalla, config.COLOR_CAZADOR,
                             (px - 6, py + 6), (px + 6, py - 6), 3)
            continue
        pygame.draw.circle(pantalla, e.color, (px, py), e.radio)
        pygame.draw.circle(pantalla, config.COLOR_FONDO, (px, py), e.radio, 2)
        if e.es_humano:         # anillo blanco: este sos vos
            pygame.draw.circle(pantalla, config.COLOR_HUD, (px, py), e.radio + 4, 2)


# ---------------------------------------------------------------------- #
# Minimapa / radar
# ---------------------------------------------------------------------- #


def crear_minimapa(laberinto):
    """Pre-dibuja los muros y salidas una sola vez por partida; por frame
    solo se le superponen los puntos móviles."""
    esc = config.MINIMAPA_PX_POR_TILE
    base = pygame.Surface((laberinto.ancho * esc, laberinto.alto * esc),
                          pygame.SRCALPHA)
    base.fill((8, 8, 12, 215))
    for ty in range(laberinto.alto):
        fila = laberinto.grid[ty]
        for tx in range(laberinto.ancho):
            if fila[tx] == MURO:
                base.fill((70, 78, 102, 235), (tx * esc, ty * esc, esc, esc))
    for sx, sy in laberinto.salidas:
        base.fill(config.COLOR_SALIDA, (sx * esc - esc, sy * esc - esc,
                                        esc * 3, esc * 3))
    return base


def dibujar_minimapa(pantalla, base, partida):
    jugador = partida.jugador
    if jugador is None:
        return
    esc = config.MINIMAPA_PX_POR_TILE
    x0 = config.ANCHO_VENTANA - base.get_width() - 14
    y0 = 14
    pantalla.blit(base, (x0, y0))

    radar_px = config.RADIO_RADAR_TILES * config.TILE
    alerta = False
    for e in partida.entidades:
        if e.escapado:
            continue
        aliado = e.rol == jugador.rol
        if not aliado:
            # A los enemigos solo los "escuchás" si están cerca: ese es el radar.
            if not e.activo or e.distancia(jugador) > radar_px:
                continue
            if e.distancia(jugador) < config.RADIO_ALERTA_TILES * config.TILE:
                alerta = True
        bx = x0 + int(e.x * esc / config.TILE)
        by = y0 + int(e.y * esc / config.TILE)
        if e is jugador:
            color, radio = config.COLOR_HUD, 4
        elif e.atrapado:
            color, radio = config.COLOR_ATRAPADO, 3
        else:
            color, radio = e.color, 3
        pygame.draw.circle(pantalla, color, (bx, by), radio)

    if alerta:  # borde rojo pulsante: hay un enemigo encima tuyo
        pulso = (math.sin(partida.tiempo * 10) + 1) / 2
        color_borde = (int(110 + 145 * pulso), 50, 50)
    else:
        color_borde = (90, 95, 115)
    pygame.draw.rect(pantalla, color_borde,
                     (x0 - 2, y0 - 2, base.get_width() + 4, base.get_height() + 4), 2)


# ---------------------------------------------------------------------- #
# HUD y pantallas
# ---------------------------------------------------------------------- #


def _texto_con_sombra(pantalla, fuente, texto, x, y, centrado=False, color=None):
    sombra = fuente.render(texto, True, config.COLOR_HUD_SOMBRA)
    frente = fuente.render(texto, True, color or config.COLOR_HUD)
    if centrado:
        x -= frente.get_width() // 2
    pantalla.blit(sombra, (x + 2, y + 2))
    pantalla.blit(frente, (x, y))


def formato_tiempo(segundos):
    return f"{int(segundos // 60):02d}:{segundos % 60:04.1f}"


def dibujar_hud_partida(pantalla, fuentes, partida, fps):
    _texto_con_sombra(pantalla, fuentes["media"],
                      f"{formato_tiempo(partida.tiempo)} / {formato_tiempo(config.TIEMPO_LIMITE)}",
                      config.ANCHO_VENTANA // 2, 12, centrado=True)
    _texto_con_sombra(pantalla, fuentes["chica"], f"seed: {partida.seed}", 12, 12)
    _texto_con_sombra(pantalla, fuentes["chica"], f"{fps:.0f} fps", 12, 38)
    _texto_con_sombra(pantalla, fuentes["chica"],
                      f"Escaparon {partida.n_escapados}/{config.NUM_ESCAPISTAS}"
                      f" · Atrapados {partida.n_atrapados}/{config.NUM_ESCAPISTAS}",
                      12, 64)
    if getattr(partida, "online", False):
        _texto_con_sombra(pantalla, fuentes["chica"], f"online · sala #{partida.id}",
                          12, 90, color=config.COLOR_SALIDA)
    if partida.jugador is not None and partida.jugador.rol == "escapista":
        objetivo = "Llegá a una salida verde antes de que te atrapen"
    else:
        objetivo = "Atrapá a los escapistas antes de que lleguen a una salida"
    _texto_con_sombra(pantalla, fuentes["chica"],
                      f"{objetivo}   |   ESC: abandonar",
                      12, config.ALTO_VENTANA - 34)


def dibujar_menu(pantalla, fuentes, seleccion, nombre, db_ok):
    pantalla.fill(config.COLOR_FONDO)
    cx = config.ANCHO_VENTANA // 2
    _texto_con_sombra(pantalla, fuentes["grande"], "EL GRAN ESCAPE", cx, 100, centrado=True)
    _texto_con_sombra(pantalla, fuentes["chica"],
                      "3 escapistas vs 2 cazadores en un laberinto procedural",
                      cx, 175, centrado=True)
    _texto_con_sombra(pantalla, fuentes["chica"],
                      f"Jugás como: {nombre}      N  cambiar nombre"
                      f"      T  ranking      J  multijugador online",
                      cx, 205, centrado=True)
    if db_ok:
        estado_db, color_db = "base de datos: conectada", config.COLOR_SALIDA
    else:
        estado_db, color_db = "base de datos: sin conexión (no se guardan tiempos)", config.COLOR_CAZADOR
    _texto_con_sombra(pantalla, fuentes["chica"], estado_db,
                      cx, config.ALTO_VENTANA - 34, centrado=True, color=color_db)

    tarjetas = [
        ("ESCAPISTA", config.COLOR_ESCAPISTA,
         ["Llegá a una salida verde", "antes de que te atrapen.",
          "Ventaja: el radar del minimapa."]),
        ("CAZADOR", config.COLOR_CAZADOR,
         ["Atrapá a los 3 escapistas", "antes de que escapen.",
          "Ventaja: sos más rápido."]),
    ]
    ancho_t, alto_t, sep = 380, 230, 60
    x0 = cx - ancho_t - sep // 2
    y0 = 250
    for i, (titulo, color, lineas) in enumerate(tarjetas):
        rect = pygame.Rect(x0 + i * (ancho_t + sep), y0, ancho_t, alto_t)
        pygame.draw.rect(pantalla, config.COLOR_TARJETA, rect, border_radius=12)
        pygame.draw.rect(pantalla, color if i == seleccion else config.COLOR_MURO,
                         rect, 4 if i == seleccion else 2, border_radius=12)
        pygame.draw.circle(pantalla, color, (rect.centerx, rect.y + 45), 15)
        _texto_con_sombra(pantalla, fuentes["media"], titulo,
                          rect.centerx, rect.y + 72, centrado=True, color=color)
        for j, linea in enumerate(lineas):
            _texto_con_sombra(pantalla, fuentes["chica"], linea,
                              rect.centerx, rect.y + 125 + j * 26, centrado=True)
    _texto_con_sombra(pantalla, fuentes["chica"],
                      "←  →  elegir rol      ENTER  jugar      ESC  salir",
                      cx, y0 + alto_t + 50, centrado=True)


def dibujar_ingreso_nombre(pantalla, fuentes, buffer):
    """Pantalla para escribir el nombre de jugador (queda en usuario.json
    y es el nombre con el que entrás al ranking)."""
    pantalla.fill(config.COLOR_FONDO)
    cx = config.ANCHO_VENTANA // 2
    cy = config.ALTO_VENTANA // 2
    _texto_con_sombra(pantalla, fuentes["media"], "¿Cómo te llamás?",
                      cx, cy - 120, centrado=True)
    _texto_con_sombra(pantalla, fuentes["chica"],
                      "Con este nombre entrás al ranking",
                      cx, cy - 75, centrado=True)
    caja = pygame.Rect(cx - 220, cy - 25, 440, 56)
    pygame.draw.rect(pantalla, config.COLOR_TARJETA, caja, border_radius=8)
    pygame.draw.rect(pantalla, config.COLOR_ESCAPISTA, caja, 2, border_radius=8)
    cursor = "|" if (pygame.time.get_ticks() // 400) % 2 == 0 else " "
    _texto_con_sombra(pantalla, fuentes["media"], buffer + cursor,
                      cx, cy - 12, centrado=True)
    _texto_con_sombra(pantalla, fuentes["chica"], "ENTER  confirmar",
                      cx, cy + 60, centrado=True)


def dibujar_ranking(pantalla, fuentes, escapistas, cazadores, error):
    """Tabla de récords leída de PostgreSQL: mejores tiempos de escape y
    cazadores con más capturas."""
    pantalla.fill(config.COLOR_FONDO)
    cx = config.ANCHO_VENTANA // 2
    _texto_con_sombra(pantalla, fuentes["grande"], "RANKING", cx, 60, centrado=True)
    if error:
        _texto_con_sombra(pantalla, fuentes["media"],
                          "Sin conexión a la base de datos",
                          cx, 280, centrado=True, color=config.COLOR_CAZADOR)
        _texto_con_sombra(pantalla, fuentes["chica"],
                          "Arrancá PostgreSQL y volvé a entrar",
                          cx, 330, centrado=True)
    else:
        col_izq, col_der, y0 = cx - 310, cx + 310, 170
        _texto_con_sombra(pantalla, fuentes["media"], "Escapistas más rápidos",
                          col_izq, y0, centrado=True, color=config.COLOR_ESCAPISTA)
        if not escapistas:
            _texto_con_sombra(pantalla, fuentes["chica"], "Todavía no escapó nadie...",
                              col_izq, y0 + 60, centrado=True)
        for i, (nombre, mejor, escapes) in enumerate(escapistas):
            veces = f"  ({escapes} escapes)" if escapes > 1 else ""
            _texto_con_sombra(pantalla, fuentes["chica"],
                              f"{i + 1:>2}. {nombre}  -  {formato_tiempo(mejor)}{veces}",
                              col_izq, y0 + 55 + i * 32, centrado=True)
        _texto_con_sombra(pantalla, fuentes["media"], "Cazadores más efectivos",
                          col_der, y0, centrado=True, color=config.COLOR_CAZADOR)
        if not cazadores:
            _texto_con_sombra(pantalla, fuentes["chica"], "Todavía no cazó nadie...",
                              col_der, y0 + 60, centrado=True)
        for i, (nombre, capturas) in enumerate(cazadores):
            _texto_con_sombra(pantalla, fuentes["chica"],
                              f"{i + 1:>2}. {nombre}  -  {capturas} capturas",
                              col_der, y0 + 55 + i * 32, centrado=True)
    _texto_con_sombra(pantalla, fuentes["chica"], "ESC  volver al menú",
                      cx, config.ALTO_VENTANA - 50, centrado=True)


def dibujar_fin(pantalla, fuentes, partida, mensaje_guardado=None):
    velo = pygame.Surface((config.ANCHO_VENTANA, config.ALTO_VENTANA), pygame.SRCALPHA)
    velo.fill((0, 0, 0, 175))
    pantalla.blit(velo, (0, 0))
    cx = config.ANCHO_VENTANA // 2
    y = config.ALTO_VENTANA // 2 - 175

    jugador = partida.jugador
    if jugador is not None and jugador.rol == "escapista":
        if jugador.escapado:
            titulo = "¡ESCAPASTE!"
            subtitulo = f"Tu tiempo: {formato_tiempo(jugador.tiempo_escape)}"
        elif jugador.atrapado:
            titulo = "TE ATRAPARON"
            subtitulo = (f"{jugador.capturado_por.nombre} te alcanzó"
                         f" a los {formato_tiempo(partida.tiempo)}")
        else:
            titulo = "SE ACABÓ EL TIEMPO"
            subtitulo = "No llegaste a ninguna salida"
    else:
        if partida.n_atrapados == config.NUM_ESCAPISTAS:
            titulo = "¡CACERÍA PERFECTA!"
        else:
            titulo = "FIN DE LA CACERÍA"
        capturas = f" (vos atrapaste {jugador.capturas})" if jugador is not None else ""
        subtitulo = (f"Atrapados {partida.n_atrapados}/{config.NUM_ESCAPISTAS}"
                     f" · escaparon {partida.n_escapados}{capturas}")

    _texto_con_sombra(pantalla, fuentes["grande"], titulo, cx, y, centrado=True)
    _texto_con_sombra(pantalla, fuentes["media"], subtitulo, cx, y + 75, centrado=True)

    y_filas = y + 150
    for i, e in enumerate(partida.escapistas):
        if e.escapado:
            txt = f"{e.nombre}: escapó en {formato_tiempo(e.tiempo_escape)}"
        elif e.atrapado:
            txt = f"{e.nombre}: atrapado por {e.capturado_por.nombre}"
        else:
            txt = f"{e.nombre}: no escapó"
        _texto_con_sombra(pantalla, fuentes["chica"], txt,
                          cx, y_filas + i * 28, centrado=True)

    if mensaje_guardado:
        guardado_ok = "guardado" in mensaje_guardado.lower()
        _texto_con_sombra(pantalla, fuentes["chica"], mensaje_guardado,
                          cx, y_filas + config.NUM_ESCAPISTAS * 28 + 24, centrado=True,
                          color=config.COLOR_SALIDA if guardado_ok else config.COLOR_CAZADOR)
    pie = ("R  volver al lobby      M  menú      ESC  salir"
           if getattr(partida, "online", False)
           else "R  revancha      M  menú      ESC  salir")
    _texto_con_sombra(pantalla, fuentes["chica"], pie,
                      cx, y_filas + config.NUM_ESCAPISTAS * 28 + 60, centrado=True)


def dibujar_lobby(pantalla, fuentes, partidas, seleccion, rol, error):
    """Lista de salas esperando jugadores, leída de la base."""
    pantalla.fill(config.COLOR_FONDO)
    cx = config.ANCHO_VENTANA // 2
    _texto_con_sombra(pantalla, fuentes["grande"], "PARTIDAS ONLINE", cx, 60, centrado=True)
    color_rol = (config.COLOR_ESCAPISTA if rol == "escapista"
                 else config.COLOR_CAZADOR)
    _texto_con_sombra(pantalla, fuentes["media"],
                      f"Vas a entrar como: {rol.upper()}   (← → cambia)",
                      cx, 150, centrado=True, color=color_rol)
    if error:
        _texto_con_sombra(pantalla, fuentes["chica"], error,
                          cx, 205, centrado=True, color=config.COLOR_CAZADOR)

    y0 = 250
    if not partidas:
        _texto_con_sombra(pantalla, fuentes["chica"],
                          "No hay salas esperando — creá una con C",
                          cx, y0 + 40, centrado=True)
    for i, (pid, host, n_esc, n_caz) in enumerate(partidas):
        marca = "»  " if i == seleccion else "    "
        texto = (f"{marca}Sala #{pid}  de {host}   ·   escapistas "
                 f"{n_esc}/{config.NUM_ESCAPISTAS} · cazadores "
                 f"{n_caz}/{config.NUM_CAZADORES}")
        color = config.COLOR_HUD if i == seleccion else (150, 153, 168)
        _texto_con_sombra(pantalla, fuentes["chica"], texto,
                          cx, y0 + i * 34, centrado=True, color=color)

    _texto_con_sombra(pantalla, fuentes["chica"],
                      "↑ ↓  elegir      ENTER  unirse      C  crear sala      ESC  volver",
                      cx, config.ALTO_VENTANA - 50, centrado=True)


def dibujar_espera(pantalla, fuentes, partida_id, jugadores, soy_host):
    """Sala de espera: quiénes están y quién falta."""
    pantalla.fill(config.COLOR_FONDO)
    cx = config.ANCHO_VENTANA // 2
    _texto_con_sombra(pantalla, fuentes["grande"], f"SALA #{partida_id}",
                      cx, 60, centrado=True)
    n_esc = sum(1 for j in jugadores if j[2] == "escapista")
    n_caz = sum(1 for j in jugadores if j[2] == "cazador")
    _texto_con_sombra(pantalla, fuentes["media"],
                      f"Escapistas {n_esc}/{config.NUM_ESCAPISTAS}   ·   "
                      f"Cazadores {n_caz}/{config.NUM_CAZADORES}",
                      cx, 150, centrado=True)
    y0 = 230
    for i, (_jid, nombre, rol, _slot, es_bot) in enumerate(jugadores):
        color = (config.COLOR_ESCAPISTA if rol == "escapista"
                 else config.COLOR_CAZADOR)
        _texto_con_sombra(pantalla, fuentes["chica"],
                          f"{nombre}   —   {rol}", cx, y0 + i * 32,
                          centrado=True, color=color)
    if soy_host:
        pie = ("ENTER  empezar ya (los puestos vacíos los juegan bots)"
               "      ESC  cerrar la sala")
    else:
        pie = "Esperando a que el host empiece...      ESC  salir de la sala"
    _texto_con_sombra(pantalla, fuentes["chica"], pie,
                      cx, config.ALTO_VENTANA - 50, centrado=True)
