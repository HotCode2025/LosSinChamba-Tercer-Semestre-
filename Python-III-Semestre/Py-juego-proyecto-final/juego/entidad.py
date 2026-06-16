"""Entidad: cualquier cosa que se mueve por el laberinto (humano o bot).

La física es la misma para todos — movimiento continuo en píxeles con
colisión resuelta por ejes (primero X, después Y, el esquema clásico para
mapas de tiles: no se traba en esquinas y permite deslizarse por las
paredes). Que los bots usen exactamente la misma física que el jugador
garantiza que no atraviesen paredes ni tengan ventajas imposibles.

Quién decide la dirección es lo único que cambia: el teclado para el humano,
un "cerebro" de juego.bots para los bots. Acá también viven los datos de
partida de cada uno (rol, atrapado, escapado, tiempo, capturas), que en la
fase 3 son exactamente lo que se persiste en PostgreSQL.
"""
from math import hypot

import config


class Entidad:
    def __init__(self, nombre, rol, x_px, y_px, velocidad, radio, color):
        self.nombre = nombre
        self.rol = rol                  # 'escapista' | 'cazador'
        self.x = x_px
        self.y = y_px
        self.velocidad = velocidad
        self.radio = radio
        self.color = color
        self.es_humano = False
        self.cerebro = None             # los bots reciben el suyo en partida.py
        # Estado dentro de la partida (lo que la fase 3 guarda en la base):
        self.atrapado = False
        self.escapado = False
        self.capturado_por = None       # Entidad cazadora, para el ranking
        self.tiempo_escape = None       # segundos, si escapó
        self.capturas = 0               # solo cazadores

    @property
    def activo(self):
        """Sigue en juego: ni atrapado ni escapado."""
        return not self.atrapado and not self.escapado

    def mover(self, dt, dx, dy, laberinto, tile_px):
        """Avanza en la dirección (dx, dy), normalizada si hace falta para
        que en diagonal no se vaya más rápido."""
        norma = hypot(dx, dy)
        if norma == 0:
            return
        if norma > 1:
            dx, dy = dx / norma, dy / norma
        self._mover_eje(dx * self.velocidad * dt, 0, laberinto, tile_px)
        self._mover_eje(0, dy * self.velocidad * dt, laberinto, tile_px)
        self._ayuda_carril(dt, dx, dy, laberinto, tile_px)

    def _ayuda_carril(self, dt, dx, dy, laberinto, tile_px):
        """Al avanzar por un pasillo (movimiento en un solo eje), empuja
        suavemente hacia el centro del carril. Sin esto, doblar una esquina
        exigía estar alineado al píxel y el control se sentía "enganchado";
        es el mismo truco que usa Pac-Man."""
        paso = config.AYUDA_CARRIL * self.velocidad * dt
        if dx and not dy:
            centro = (int(self.y // tile_px) + 0.5) * tile_px
            self._mover_eje(0, max(-paso, min(paso, centro - self.y)),
                            laberinto, tile_px)
        elif dy and not dx:
            centro = (int(self.x // tile_px) + 0.5) * tile_px
            self._mover_eje(max(-paso, min(paso, centro - self.x)), 0,
                            laberinto, tile_px)

    def _mover_eje(self, dx, dy, laberinto, tile_px):
        if not dx and not dy:
            return
        
        eps = 0.001
        if dx != 0:
            self.x += dx
            leading_x = self.x + self.radio if dx > 0 else self.x - self.radio
            tx = int(leading_x // tile_px)
            ty_min = int((self.y - self.radio + eps) // tile_px)
            ty_max = int((self.y + self.radio - eps) // tile_px)
            
            for ty in range(ty_min, ty_max + 1):
                if laberinto.es_solido(tx, ty):
                    if dx > 0:
                        self.x = tx * tile_px - self.radio
                    elif dx < 0:
                        self.x = (tx + 1) * tile_px + self.radio
                    break

        if dy != 0:
            self.y += dy
            leading_y = self.y + self.radio if dy > 0 else self.y - self.radio
            ty = int(leading_y // tile_px)
            tx_min = int((self.x - self.radio + eps) // tile_px)
            tx_max = int((self.x + self.radio - eps) // tile_px)
            
            for tx in range(tx_min, tx_max + 1):
                if laberinto.es_solido(tx, ty):
                    if dy > 0:
                        self.y = ty * tile_px - self.radio
                    elif dy < 0:
                        self.y = (ty + 1) * tile_px + self.radio
                    break

    def tile_actual(self, tile_px):
        """Tile donde está parado el centro de la entidad."""
        return int(self.x // tile_px), int(self.y // tile_px)

    def distancia(self, otra):
        return hypot(self.x - otra.x, self.y - otra.y)
