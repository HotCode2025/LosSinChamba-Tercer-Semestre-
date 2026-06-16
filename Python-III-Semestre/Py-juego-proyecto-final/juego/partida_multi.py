"""Partida online: misma interfaz que juego.partida.Partida (así todo el
render y el HUD funcionan igual), pero el estado de verdad vive en PostgreSQL.

Cómo se reparte el trabajo:

  * Mi entidad usa la física local de siempre (responsiva, sin lag) y publica
    su posición por el hilo de red.
  * Las entidades remotas reciben su posición de la base (~10 Hz) y se
    dibujan con suavizado exponencial para que el movimiento se vea continuo.
  * Los cupos vacíos se llenan con bots que SIMULA EL HOST con los mismos
    cerebros de la fase 2, publicando sus posiciones: para el resto de los
    clientes un bot es un jugador remoto más.
  * Capturas y escapes no se deciden acá: se RECLAMAN (red.encolar_*) y la
    base los arbitra con UPDATEs atómicos. La confirmación vuelve en el
    siguiente snapshot por los flags. Por eso no hay race conditions aunque
    cinco clientes vean mundos ligeramente distintos.

El laberinto y los spawns salen de la seed (misma derivación exacta que en
single-player), así los cinco clientes generan el mismo mundo sin
transmitirlo.
"""
import random

import config
from juego.bots import CerebroCazador, CerebroEscapista
from juego.entidad import Entidad
from juego.laberinto import Laberinto, SALIDA


class PartidaMulti:
    online = True

    def __init__(self, partida_id, seed, mi_jugador_id, soy_host, jugadores):
        """jugadores: [(jugador_id, nombre, rol, slot, es_bot)] — la lista
        viene de la base y es idéntica en todos los clientes."""
        self.id = partida_id
        self.seed = seed
        self.mi_jugador_id = mi_jugador_id
        self.soy_host = soy_host
        self.laberinto = Laberinto(config.CELDAS_ANCHO, config.CELDAS_ALTO, seed,
                                   config.PORCENTAJE_ATAJOS, config.NUM_SALIDAS,
                                   config.DISTANCIA_MIN_SALIDAS)
        self.tiempo = 0.0
        self.terminada = False
        self.conexion_perdida = False

        # Misma derivación de azar que en single-player: spawns idénticos
        # en los cinco clientes sin comunicarse.
        rng = random.Random(seed ^ 0xC0FFEE)
        spawns_esc = self._spawns_escapistas()
        spawns_caz = self._spawns_cazadores(rng)

        self.entidades = []
        self.por_id = {}
        self.jugador = None
        tile = config.TILE
        for jugador_id, nombre, rol, slot, es_bot in jugadores:
            es_mio = jugador_id == mi_jugador_id
            if rol == "escapista":
                tx, ty = spawns_esc[slot]
                vel = config.VEL_ESCAPISTA
                color = config.COLOR_ESCAPISTA if es_mio else config.COLOR_ESCAPISTA_BOT
            else:
                tx, ty = spawns_caz[slot]
                vel = config.VEL_CAZADOR
                color = config.COLOR_CAZADOR
            e = Entidad(nombre, rol, (tx + 0.5) * tile, (ty + 0.5) * tile,
                        vel, config.RADIO_JUGADOR, color)
            e.jugador_id = jugador_id
            e.es_humano = es_mio
            if es_bot and soy_host:
                e.cerebro = (CerebroCazador if rol == "cazador"
                             else CerebroEscapista)(e, self, rng)
            self.entidades.append(e)
            self.por_id[jugador_id] = e
            if es_mio:
                self.jugador = e

    # Las mismas fórmulas que Partida: el slot indexa el spawn.

    def _spawns_escapistas(self):
        cx = (self.laberinto.celdas_ancho // 2) * 2 + 1
        cy = (self.laberinto.celdas_alto // 2) * 2 + 1
        return [(cx, cy), (cx - 2, cy), (cx + 2, cy),
                (cx, cy - 2), (cx, cy + 2)][:config.NUM_ESCAPISTAS]

    def _spawns_cazadores(self, rng):
        cw, ch = self.laberinto.celdas_ancho, self.laberinto.celdas_alto
        spawns = []
        for qx, qy in rng.sample([(-1, -1), (1, -1), (-1, 1), (1, 1)],
                                 k=config.NUM_CAZADORES):
            celda_x = cw // 2 + qx * rng.randrange(cw // 4, cw // 2)
            celda_y = ch // 2 + qy * rng.randrange(ch // 4, ch // 2)
            celda_x = min(max(celda_x, 0), cw - 1)
            celda_y = min(max(celda_y, 0), ch - 1)
            spawns.append((celda_x * 2 + 1, celda_y * 2 + 1))
        return spawns

    # Interfaz común con Partida (la usa todo el render):

    @property
    def escapistas(self):
        return [e for e in self.entidades if e.rol == "escapista"]

    @property
    def cazadores(self):
        return [e for e in self.entidades if e.rol == "cazador"]

    @property
    def n_escapados(self):
        return sum(1 for e in self.escapistas if e.escapado)

    @property
    def n_atrapados(self):
        return sum(1 for e in self.escapistas if e.atrapado)

    # ------------------------------------------------------------------ #
    # Un tick de juego online
    # ------------------------------------------------------------------ #

    def actualizar(self, dt, direccion, red):
        if self.terminada:
            return
        posiciones, flags, estado, t_red, caida = red.snapshot()
        if caida:
            self.conexion_perdida = True
            self.terminada = True
            return
        # El reloj de la partida es el de la BASE: igual para todos.
        self.tiempo = float(t_red) if t_red else self.tiempo + dt

        # Flags arbitrados por la base (¿quién está atrapado/escapado?).
        for jugador_id, (atrapado, escapado, t_esc, capturador) in flags.items():
            e = self.por_id.get(jugador_id)
            if e is None:
                continue
            e.atrapado, e.escapado = atrapado, escapado
            e.tiempo_escape = float(t_esc) if t_esc is not None else None
            e.capturado_por = self.por_id.get(capturador)

        # Mi entidad: física local + publicar.
        yo = self.jugador
        if yo.activo:
            yo.mover(dt, *direccion, self.laberinto, config.TILE)
            red.publicar(yo.jugador_id, yo.x, yo.y)

        # Bots del host: misma IA de la fase 2, publicados como uno más.
        if self.soy_host:
            for e in self.entidades:
                if e.cerebro is not None and e.activo:
                    dx, dy = e.cerebro.direccion(dt)
                    e.mover(dt, dx, dy, self.laberinto, config.TILE)
                    red.publicar(e.jugador_id, e.x, e.y)

        # Remotos: mover suavemente hacia la última posición publicada.
        k = min(1.0, dt * config.SUAVIZADO_REMOTOS)
        for e in self.entidades:
            if e.es_humano or e.cerebro is not None or not e.activo:
                continue
            if e.jugador_id in posiciones:
                ox, oy = posiciones[e.jugador_id]
                e.x += (ox - e.x) * k
                e.y += (oy - e.y) * k

        # Reclamos: la base decide, nosotros solo pedimos.
        self._reclamar_eventos(red)

        if estado == "terminada":
            self.terminada = True

    def _reclamar_eventos(self, red):
        tile = config.TILE
        mios = [self.jugador] + ([e for e in self.entidades if e.cerebro]
                                 if self.soy_host else [])
        for e in mios:
            if not e.activo:
                continue
            if e.rol == "escapista":
                if self.laberinto.tile(*e.tile_actual(tile)) == SALIDA:
                    red.encolar_escape(e.jugador_id)
            else:
                for presa in self.escapistas:
                    if not presa.activo:
                        continue
                    alcance = e.radio + presa.radio + config.RADIO_CAPTURA_EXTRA
                    if e.distancia(presa) <= alcance:
                        red.encolar_captura(presa.jugador_id, e.jugador_id)
