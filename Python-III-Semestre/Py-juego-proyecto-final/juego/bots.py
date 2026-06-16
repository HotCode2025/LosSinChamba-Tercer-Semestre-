"""IA de los bots ("cerebros").

Cada cerebro decide solo una dirección (dx, dy) por frame; el movimiento
real lo hace la física común de Entidad, así un bot nunca atraviesa paredes.

CAZADOR — máquina de estados implícita:
  * Patrulla: elige un destino (a veces cerca de una salida, para "montar
    guardia") y lo sigue por BFS.
  * Persecución: si ve a un escapista (dentro de su radio de visión Y con
    línea de visión libre), persigue su última posición vista, recalculando
    el camino. Si lo pierde, revisa esa última posición y vuelve a patrullar.

ESCAPISTA — siempre quiere la salida más cercana (BFS multi-destino), pero
"escucha" a los cazadores próximos: si hay uno cerca replanifica el camino
evitando la zona que lo rodea, y si queda acorralado huye al tile vecino
que más lo aleje.
"""
from math import hypot

import config

REPATH_CAZA = 0.35       # seg entre recálculos de camino al perseguir
REPATH_ESCAPE = 0.5      # seg entre replanificaciones del escapista
DIST_WAYPOINT = 6.0      # px para dar por alcanzado un waypoint
PROB_VIGILAR_SALIDA = 0.4


def hay_vision(laberinto, x0, y0, x1, y1, tile_px):
    """True si el segmento entre dos puntos no cruza ningún muro.
    Muestrea el segmento cada medio tile: simple y suficiente."""
    pasos = max(1, int(hypot(x1 - x0, y1 - y0) / (tile_px / 2)))
    for i in range(1, pasos + 1):
        t = i / pasos
        tx = int((x0 + (x1 - x0) * t) // tile_px)
        ty = int((y0 + (y1 - y0) * t) // tile_px)
        if laberinto.es_solido(tx, ty):
            return False
    return True


class _CerebroBase:
    def __init__(self, entidad, partida, rng):
        self.ent = entidad
        self.partida = partida
        self.rng = rng
        self.camino = []        # lista de tiles a recorrer
        # Arranque desfasado: si todos los cerebros recalculan camino en el
        # mismo frame, los BFS simultáneos producen un tironcito periódico.
        self.t_repath = rng.random() * 0.3

    def _seguir_camino(self):
        """Dirección hacia el próximo waypoint del camino actual."""
        ent, tile = self.ent, config.TILE
        while self.camino:
            tx, ty = self.camino[0]
            cx, cy = (tx + 0.5) * tile, (ty + 0.5) * tile
            d = hypot(cx - ent.x, cy - ent.y)
            if d < DIST_WAYPOINT:
                self.camino.pop(0)
                continue
            return (cx - ent.x) / d, (cy - ent.y) / d
        return 0.0, 0.0


class CerebroCazador(_CerebroBase):
    def __init__(self, entidad, partida, rng):
        super().__init__(entidad, partida, rng)
        self.ultima_vista = None    # último tile donde vio a una presa

    def direccion(self, dt):
        self.t_repath -= dt
        ent, lab, tile = self.ent, self.partida.laberinto, config.TILE
        vision_px = config.VISION_CAZADOR_TILES * tile

        # ¿Veo a algún escapista? (el más cercano, con línea de visión libre)
        presa, dist_presa = None, None
        for e in self.partida.escapistas:
            if not e.activo:
                continue
            d = ent.distancia(e)
            if d <= vision_px and (dist_presa is None or d < dist_presa) \
                    and hay_vision(lab, ent.x, ent.y, e.x, e.y, tile):
                presa, dist_presa = e, d

        if presa is not None:
            objetivo = presa.tile_actual(tile)
            if objetivo != self.ultima_vista or self.t_repath <= 0 or not self.camino:
                self.camino = lab.camino(ent.tile_actual(tile), {objetivo}) or []
                self.t_repath = REPATH_CAZA
            self.ultima_vista = objetivo
        elif self.ultima_vista is not None and not self.camino:
            # Llegué a donde la vi por última vez y no hay nadie: a patrullar.
            self.ultima_vista = None

        if not self.camino and self.ultima_vista is None:
            self.camino = self._nueva_patrulla()
        return self._seguir_camino()

    def _nueva_patrulla(self):
        """Destino de patrulla: a veces vigilar una salida, a veces vagar."""
        lab = self.partida.laberinto
        if lab.salidas and self.rng.random() < PROB_VIGILAR_SALIDA:
            sx, sy = self.rng.choice(lab.salidas)
            # El tile interior pegado a la salida (la salida está en el borde).
            if sx == 0:
                destino = (1, sy)
            elif sx == lab.ancho - 1:
                destino = (lab.ancho - 2, sy)
            elif sy == 0:
                destino = (sx, 1)
            else:
                destino = (sx, lab.alto - 2)
        else:
            destino = (self.rng.randrange(lab.celdas_ancho) * 2 + 1,
                       self.rng.randrange(lab.celdas_alto) * 2 + 1)
        return lab.camino(self.ent.tile_actual(config.TILE), {destino}) or []


class CerebroEscapista(_CerebroBase):
    """El bot no conoce el camino a la salida de memoria: explora el
    laberinto (con preferencia por los bordes, que es donde están las
    salidas) y recién cuando una salida entra en el alcance de su radar la
    recuerda y va directo. Sin esto, el pathfinding perfecto hacía que los
    bots escaparan en menos de 30 segundos y jugar de cazador no tuviera
    ninguna gracia."""

    def __init__(self, entidad, partida, rng):
        super().__init__(entidad, partida, rng)
        self.salidas_vistas = set()

    def direccion(self, dt):
        self.t_repath -= dt
        self._mirar_radar()
        if self.t_repath <= 0 or not self.camino:
            self.t_repath = REPATH_ESCAPE
            self._planificar()
        return self._seguir_camino()

    def _mirar_radar(self):
        """Memoriza las salidas que entran en el alcance del radar."""
        ent, lab, tile = self.ent, self.partida.laberinto, config.TILE
        alcance = config.RADIO_RADAR_TILES * tile
        for s in lab.salidas:
            if s not in self.salidas_vistas and hypot(
                    (s[0] + 0.5) * tile - ent.x,
                    (s[1] + 0.5) * tile - ent.y) <= alcance:
                self.salidas_vistas.add(s)
                self.camino = []    # apareció una salida: replanificar ya
                self.t_repath = 0.0

    def _planificar(self):
        ent, lab, tile = self.ent, self.partida.laberinto, config.TILE
        peligro_px = config.PELIGRO_ESCAPISTA_TILES * tile
        cercanos = [c for c in self.partida.cazadores if ent.distancia(c) < peligro_px]
        mi_tile = ent.tile_actual(tile)

        if self.salidas_vistas:
            if cercanos:
                # Ir a una salida conocida esquivando la zona de los cazadores.
                tiles_caz = [c.tile_actual(tile) for c in cercanos]
                radio = config.EVITAR_TILES

                def peligroso(t):
                    return any(abs(t[0] - cx) <= radio and abs(t[1] - cy) <= radio
                               for cx, cy in tiles_caz)

                camino = lab.camino(mi_tile, self.salidas_vistas, evitar=peligroso)
                self.camino = (camino if camino is not None
                               else self._huida_greedy(cercanos))
            else:
                self.camino = lab.camino(mi_tile, self.salidas_vistas) or []
        elif cercanos:
            self.camino = self._huida_greedy(cercanos)
        elif not self.camino:
            # Explorar: seguir vagando hacia un destino nuevo.
            self.camino = lab.camino(mi_tile, {self._destino_exploracion()}) or []

    def _destino_exploracion(self):
        """La mayoría de las veces, una celda pegada a un borde al azar (ahí
        están las salidas); el resto, una celda cualquiera."""
        lab, rng = self.partida.laberinto, self.rng
        cw, ch = lab.celdas_ancho, lab.celdas_alto
        if rng.random() < 0.7:
            lado = rng.randrange(4)
            if lado == 0:
                celda = (rng.randrange(cw), 0)
            elif lado == 1:
                celda = (rng.randrange(cw), ch - 1)
            elif lado == 2:
                celda = (0, rng.randrange(ch))
            else:
                celda = (cw - 1, rng.randrange(ch))
        else:
            celda = (rng.randrange(cw), rng.randrange(ch))
        return celda[0] * 2 + 1, celda[1] * 2 + 1

    def _huida_greedy(self, cercanos):
        """Acorralado: ir al tile vecino que más lo aleje del cazador próximo."""
        ent, lab, tile = self.ent, self.partida.laberinto, config.TILE
        tx, ty = ent.tile_actual(tile)
        mejor, mejor_d = None, -1.0
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            vecino = (tx + dx, ty + dy)
            if lab.es_solido(*vecino):
                continue
            d = min(hypot((vecino[0] + 0.5) * tile - c.x,
                          (vecino[1] + 0.5) * tile - c.y) for c in cercanos)
            if d > mejor_d:
                mejor, mejor_d = vecino, d
        return [mejor] if mejor else []
