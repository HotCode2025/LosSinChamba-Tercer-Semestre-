"""El Gran Escape — Fase 4: multijugador online a través de PostgreSQL.

Single-player: igual que siempre (ENTER en el menú, bots de la fase 2).
Multijugador (J en el menú): el lobby lista las salas en espera; podés crear
una (sos host) o unirte con el rol que elijas. Cuando el host arranca, los
puestos vacíos los juegan bots simulados por su cliente. La sincronización
de posiciones, capturas, escapes y reloj de partida pasa entera por la base
de datos — no hay servidor de juego.

Ejecutar:   python main.py [--seed 1234] [--rol escapista|cazador]
"""
import argparse
import json
import random
from pathlib import Path

import pygame

import config
from db import repositorio
from db.conexion import DBNoDisponible, hay_conexion
from db.red import RedPartida
from juego import render
from juego.camara import Camara
from juego.partida import Partida
from juego.partida_multi import PartidaMulti

NOMBRE, MENU, JUGANDO, FIN, RANKING = "nombre", "menu", "jugando", "fin", "ranking"
LOBBY, ESPERA = "lobby", "espera"
ROLES = ("escapista", "cazador")
RUTA_USUARIO = Path(__file__).parent / config.ARCHIVO_USUARIO
LARGO_MAX_NOMBRE = 20


def direccion_desde_teclas(teclas):
    dx = ((teclas[pygame.K_d] or teclas[pygame.K_RIGHT])
          - (teclas[pygame.K_a] or teclas[pygame.K_LEFT]))
    dy = ((teclas[pygame.K_s] or teclas[pygame.K_DOWN])
          - (teclas[pygame.K_w] or teclas[pygame.K_UP]))
    return dx, dy


def preparar_partida(seed, rol):
    partida = Partida(seed, rol)
    return partida, *_recursos_render(partida)


def construir_partida_online(partida_id, mi_jugador_id, soy_host):
    """Arma el mundo local de una partida que la base marca como 'jugando'."""
    estado, seed, _host = repositorio.estado_de(partida_id)
    jugadores = repositorio.jugadores_de(partida_id)
    partida = PartidaMulti(partida_id, seed, mi_jugador_id, soy_host, jugadores)
    red = RedPartida(partida_id, mi_jugador_id)
    return (partida, *_recursos_render(partida), red)


def _recursos_render(partida):
    """Cámara + superficies que se pre-dibujan una vez por partida."""
    lab = partida.laberinto
    camara = Camara(config.ANCHO_VENTANA, config.ALTO_VENTANA,
                    lab.ancho * config.TILE, lab.alto * config.TILE)
    return camara, render.crear_minimapa(lab), render.crear_fondo(lab)


def cargar_nombre():
    try:
        return json.loads(RUTA_USUARIO.read_text(encoding="utf-8"))["nombre"]
    except (OSError, KeyError, ValueError):
        return None


def guardar_nombre(nombre):
    RUTA_USUARIO.write_text(json.dumps({"nombre": nombre}, ensure_ascii=False),
                            encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="El Gran Escape")
    parser.add_argument("--seed", type=int, default=None,
                        help="seed de la partida (misma seed = mismo laberinto)")
    parser.add_argument("--rol", choices=ROLES, default=None,
                        help="entra directo a jugar single-player, sin menú")
    parser.add_argument("--frames", type=int, default=0, help=argparse.SUPPRESS)
    parser.add_argument("--multi-solo", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args()

    pygame.init()
    pantalla = pygame.display.set_mode((config.ANCHO_VENTANA, config.ALTO_VENTANA))
    pygame.display.set_caption("El Gran Escape")
    reloj = pygame.time.Clock()
    fuentes = {
        "chica": pygame.font.Font(None, 26),
        "media": pygame.font.Font(None, 44),
        "grande": pygame.font.Font(None, 80),
    }

    db_ok = hay_conexion()
    seed_pendiente = args.seed

    def proxima_seed():
        nonlocal seed_pendiente
        if seed_pendiente is not None:
            s, seed_pendiente = seed_pendiente, None
            return s
        return random.randrange(2**31)

    nombre = cargar_nombre()
    buffer_nombre = ""
    seleccion = 0
    partida = camara = minimapa = fondo = red = None
    mensaje_guardado = None
    ranking = ([], [], None)
    # Estado del lobby / sala de espera:
    lobby_partidas, lobby_sel, lobby_error = [], 0, None
    espera_pid = mi_jid = None
    espera_soy_host = False
    espera_jugadores = []
    timer_poll = 99.0           # alto: el primer frame refresca ya

    if args.rol is not None:
        nombre = nombre or "Jugador"
        seleccion = ROLES.index(args.rol)
        partida, camara, minimapa, fondo = preparar_partida(proxima_seed(), args.rol)
        estado = JUGANDO
    elif args.multi_solo:
        # Modo de verificación: crea una sala online y la arranca ya,
        # con bots en todos los puestos vacíos.
        nombre = nombre or "Jugador"
        espera_pid, mi_jid = repositorio.crear_partida_multi(
            nombre, ROLES[seleccion], proxima_seed())
        repositorio.arrancar_partida(espera_pid, mi_jid)
        partida, camara, minimapa, fondo, red = construir_partida_online(
            espera_pid, mi_jid, soy_host=True)
        estado = JUGANDO
    elif nombre is None:
        estado = NOMBRE
    else:
        estado = MENU

    def guardar_resultado():
        nonlocal db_ok
        if partida.online:
            if partida.conexion_perdida:
                return "Se perdió la conexión con la base de datos"
            return "Partida online: el resultado ya quedó guardado en el ranking"
        try:
            repositorio.guardar_partida(partida, nombre)
            db_ok = True
            return "Resultado guardado en el ranking"
        except DBNoDisponible:
            db_ok = False
            return "Sin conexión a la base: el resultado no se guardó"

    def cargar_ranking():
        nonlocal db_ok
        try:
            datos = (repositorio.ranking_escapistas(),
                     repositorio.ranking_cazadores(), None)
            db_ok = True
            return datos
        except DBNoDisponible as e:
            db_ok = False
            return [], [], str(e)

    def cortar_red():
        nonlocal red
        if red is not None:
            red.detener()
            red = None

    def ir_al_lobby():
        nonlocal estado, lobby_error, timer_poll, lobby_sel
        lobby_error, lobby_sel, timer_poll = None, 0, 99.0
        estado = LOBBY

    frames = 0
    corriendo = True
    while corriendo:
        dt = min(reloj.tick(config.FPS) / 1000.0, 0.05)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False
            elif evento.type != pygame.KEYDOWN:
                continue
            elif estado == NOMBRE:
                if evento.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    if buffer_nombre.strip():
                        nombre = buffer_nombre.strip()[:LARGO_MAX_NOMBRE]
                        guardar_nombre(nombre)
                        estado = MENU
                elif evento.key == pygame.K_BACKSPACE:
                    buffer_nombre = buffer_nombre[:-1]
                elif evento.key == pygame.K_ESCAPE:
                    if nombre:
                        estado = MENU
                    else:
                        corriendo = False
                elif (evento.unicode and evento.unicode.isprintable()
                        and len(buffer_nombre) < LARGO_MAX_NOMBRE):
                    buffer_nombre += evento.unicode
            elif estado == MENU:
                if evento.key in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_a, pygame.K_d):
                    seleccion = 1 - seleccion
                elif evento.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    partida, camara, minimapa, fondo = preparar_partida(
                        proxima_seed(), ROLES[seleccion])
                    mensaje_guardado = None
                    estado = JUGANDO
                elif evento.key == pygame.K_j:
                    ir_al_lobby()
                elif evento.key == pygame.K_n:
                    buffer_nombre = nombre
                    estado = NOMBRE
                elif evento.key == pygame.K_t:
                    ranking = cargar_ranking()
                    estado = RANKING
                elif evento.key == pygame.K_ESCAPE:
                    corriendo = False
            elif estado == LOBBY:
                if evento.key in (pygame.K_LEFT, pygame.K_RIGHT):
                    seleccion = 1 - seleccion
                elif evento.key == pygame.K_UP:
                    lobby_sel = max(0, lobby_sel - 1)
                elif evento.key == pygame.K_DOWN:
                    lobby_sel = min(max(0, len(lobby_partidas) - 1), lobby_sel + 1)
                elif evento.key == pygame.K_c:
                    try:
                        espera_pid, mi_jid = repositorio.crear_partida_multi(
                            nombre, ROLES[seleccion], proxima_seed())
                        espera_soy_host, espera_jugadores = True, []
                        timer_poll = 99.0
                        estado = ESPERA
                    except DBNoDisponible:
                        lobby_error = "Sin conexión a la base de datos"
                elif evento.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    if lobby_partidas:
                        pid = lobby_partidas[lobby_sel][0]
                        try:
                            mi_jid, slot = repositorio.unirse_a_partida(
                                pid, nombre, ROLES[seleccion])
                            if slot is None:
                                lobby_error = (f"No hay cupo de {ROLES[seleccion]}"
                                               " en esa sala (o ya arrancó)")
                            else:
                                espera_pid, espera_soy_host = pid, False
                                espera_jugadores, timer_poll = [], 99.0
                                estado = ESPERA
                        except DBNoDisponible:
                            lobby_error = "Sin conexión a la base de datos"
                elif evento.key == pygame.K_ESCAPE:
                    estado = MENU
            elif estado == ESPERA:
                if evento.key == pygame.K_ESCAPE:
                    repositorio.abandonar_partida(espera_pid, mi_jid)
                    ir_al_lobby()
                elif (evento.key in (pygame.K_RETURN, pygame.K_KP_ENTER)
                        and espera_soy_host):
                    repositorio.arrancar_partida(espera_pid, mi_jid)
                    timer_poll = 99.0   # el poll inmediato detecta 'jugando'
            elif estado == JUGANDO:
                if evento.key == pygame.K_ESCAPE:
                    cortar_red()
                    estado = MENU
            elif estado == FIN:
                if evento.key == pygame.K_r:
                    if partida.online:
                        ir_al_lobby()
                    else:
                        partida, camara, minimapa, fondo = preparar_partida(
                            proxima_seed(), ROLES[seleccion])
                        mensaje_guardado = None
                        estado = JUGANDO
                elif evento.key == pygame.K_m:
                    estado = MENU
                elif evento.key == pygame.K_ESCAPE:
                    corriendo = False
            elif estado == RANKING:
                if evento.key in (pygame.K_ESCAPE, pygame.K_m):
                    estado = MENU

        if estado == NOMBRE:
            render.dibujar_ingreso_nombre(pantalla, fuentes, buffer_nombre)
        elif estado == MENU:
            render.dibujar_menu(pantalla, fuentes, seleccion, nombre, db_ok)
        elif estado == RANKING:
            render.dibujar_ranking(pantalla, fuentes, *ranking)
        elif estado == LOBBY:
            timer_poll += dt
            if timer_poll >= config.REFRESCO_LOBBY:
                timer_poll = 0.0
                try:
                    lobby_partidas = repositorio.partidas_esperando()
                    lobby_sel = min(lobby_sel, max(0, len(lobby_partidas) - 1))
                    db_ok = True
                except DBNoDisponible:
                    lobby_partidas, lobby_error = [], "Sin conexión a la base de datos"
            render.dibujar_lobby(pantalla, fuentes, lobby_partidas, lobby_sel,
                                 ROLES[seleccion], lobby_error)
        elif estado == ESPERA:
            timer_poll += dt
            if timer_poll >= config.REFRESCO_LOBBY:
                timer_poll = 0.0
                try:
                    info = repositorio.estado_de(espera_pid)
                    if info is None:            # el host cerró la sala
                        ir_al_lobby()
                        lobby_error = "El host cerró la sala"
                    elif info[0] == "jugando":
                        partida, camara, minimapa, fondo, red = construir_partida_online(
                            espera_pid, mi_jid, espera_soy_host)
                        mensaje_guardado = None
                        estado = JUGANDO
                    else:
                        espera_jugadores = repositorio.jugadores_de(espera_pid)
                except DBNoDisponible:
                    ir_al_lobby()
                    lobby_error = "Sin conexión a la base de datos"
            if estado == ESPERA:
                render.dibujar_espera(pantalla, fuentes, espera_pid,
                                      espera_jugadores, espera_soy_host)
        if estado in (JUGANDO, FIN):
            if estado == JUGANDO:
                entrada = direccion_desde_teclas(pygame.key.get_pressed())
                if partida.online:
                    partida.actualizar(dt, entrada, red)
                else:
                    partida.actualizar(dt, entrada)
                if partida.terminada:
                    mensaje_guardado = guardar_resultado()
                    cortar_red()
                    estado = FIN
            camara.seguir(partida.jugador.x, partida.jugador.y)
            render.dibujar_laberinto(pantalla, fondo, camara)
            render.dibujar_entidades(pantalla, partida, camara)
            render.dibujar_minimapa(pantalla, minimapa, partida)
            render.dibujar_hud_partida(pantalla, fuentes, partida, reloj.get_fps())
            if estado == FIN:
                render.dibujar_fin(pantalla, fuentes, partida, mensaje_guardado)
        pygame.display.flip()

        frames += 1
        if args.frames and frames >= args.frames:
            corriendo = False

    cortar_red()
    pygame.quit()


if __name__ == "__main__":
    main()
