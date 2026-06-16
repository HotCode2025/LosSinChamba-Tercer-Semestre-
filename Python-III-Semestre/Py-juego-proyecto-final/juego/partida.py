"""Una partida completa: laberinto, entidades, reglas y resultado.

Acá viven las reglas del juego — capturas por contacto, escapes al pisar una
salida, condiciones de fin — independientes de Pygame y del teclado. Eso
permite simular partidas enteras entre bots sin abrir ventana (ver
tests_fase2.py) y es la misma lógica que en la fase 4 se valida contra la
base de datos.

rol_jugador: 'escapista' o 'cazador' (el humano ocupa el primer lugar de ese
equipo) o None para partidas 100%% entre bots.
"""
import random

import config
from juego.bots import CerebroCazador, CerebroEscapista
from juego.entidad import Entidad
from juego.laberinto import Laberinto, SALIDA


class Partida:
    online = False      # la variante online es juego.partida_multi.PartidaMulti

    def __init__(self, seed, rol_jugador="escapista"):
        self.seed = seed
        self.rol_jugador = rol_jugador
        self.laberinto = Laberinto(config.CELDAS_ANCHO, config.CELDAS_ALTO, seed,
                                   config.PORCENTAJE_ATAJOS, config.NUM_SALIDAS,
                                   config.DISTANCIA_MIN_SALIDAS)
        self.tiempo = 0.0
        self.terminada = False
        self.motivo_fin = None   # 'todos_resueltos' | 'jugador_resuelto' | 'tiempo'
        # Azar de spawns e IA, separado del azar del laberinto pero también
        # derivado de la seed: la partida entera es reproducible.
        rng = random.Random(seed ^ 0xC0FFEE)

        self.entidades = []
        self.jugador = None
        tile = config.TILE
        for i, (tx, ty) in enumerate(self._spawns_escapistas()):
            humano = rol_jugador == "escapista" and i == 0
            e = Entidad("Vos" if humano else f"Escapista {i + 1}", "escapista",
                        (tx + 0.5) * tile, (ty + 0.5) * tile,
                        config.VEL_ESCAPISTA, config.RADIO_JUGADOR,
                        config.COLOR_ESCAPISTA if humano else config.COLOR_ESCAPISTA_BOT)
            e.es_humano = humano
            self.entidades.append(e)
        for i, (tx, ty) in enumerate(self._spawns_cazadores(rng)):
            humano = rol_jugador == "cazador" and i == 0
            e = Entidad("Vos" if humano else f"Cazador {i + 1}", "cazador",
                        (tx + 0.5) * tile, (ty + 0.5) * tile,
                        config.VEL_CAZADOR, config.RADIO_JUGADOR, config.COLOR_CAZADOR)
            e.es_humano = humano
            self.entidades.append(e)
        for e in self.entidades:
            if e.es_humano:
                self.jugador = e
            else:
                e.cerebro = (CerebroCazador if e.rol == "cazador"
                             else CerebroEscapista)(e, self, rng)

    # ------------------------------------------------------------------ #
    # Armado
    # ------------------------------------------------------------------ #

    def _spawns_escapistas(self):
        """Los escapistas arrancan juntos, en celdas alrededor del centro."""
        cx = (self.laberinto.celdas_ancho // 2) * 2 + 1
        cy = (self.laberinto.celdas_alto // 2) * 2 + 1
        return [(cx, cy), (cx - 2, cy), (cx + 2, cy),
                (cx, cy - 2), (cx, cy + 2)][:config.NUM_ESCAPISTAS]

    def _spawns_cazadores(self, rng):
        """Los cazadores arrancan lejos, cada uno en un cuadrante distinto."""
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

    # ------------------------------------------------------------------ #
    # Consultas
    # ------------------------------------------------------------------ #

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
    # Reglas (un tick de juego)
    # ------------------------------------------------------------------ #

    def actualizar(self, dt, direccion_jugador=(0, 0)):
        if self.terminada:
            return
        self.tiempo += dt
        for e in self.entidades:
            if not e.activo:
                continue
            dx, dy = direccion_jugador if e.es_humano else e.cerebro.direccion(dt)
            e.mover(dt, dx, dy, self.laberinto, config.TILE)
        self._chequear_capturas()
        self._chequear_escapes()
        self._chequear_fin()

    def _chequear_capturas(self):
        for cazador in self.cazadores:
            for presa in self.escapistas:
                if not presa.activo:
                    continue
                alcance = cazador.radio + presa.radio + config.RADIO_CAPTURA_EXTRA
                if cazador.distancia(presa) <= alcance:
                    presa.atrapado = True
                    presa.capturado_por = cazador
                    cazador.capturas += 1

    def _chequear_escapes(self):
        for e in self.escapistas:
            if e.activo and self.laberinto.tile(*e.tile_actual(config.TILE)) == SALIDA:
                e.escapado = True
                e.tiempo_escape = self.tiempo

    def _chequear_fin(self):
        if all(not e.activo for e in self.escapistas):
            self.terminada, self.motivo_fin = True, "todos_resueltos"
        elif (self.jugador is not None and self.jugador.rol == "escapista"
                and not self.jugador.activo):
            # Tu suerte ya está echada: la partida termina para vos.
            self.terminada, self.motivo_fin = True, "jugador_resuelto"
        elif self.tiempo >= config.TIEMPO_LIMITE:
            self.terminada, self.motivo_fin = True, "tiempo"
