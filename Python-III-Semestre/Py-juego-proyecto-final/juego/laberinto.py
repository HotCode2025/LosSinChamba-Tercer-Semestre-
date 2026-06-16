"""Generación procedural del laberinto.

El laberinto se genera con Recursive Backtracking en versión iterativa (con
pila explícita: la versión recursiva revienta el límite de recursión de Python
en mapas grandes). Después se aplica "braiding": se abre un porcentaje de los
callejones sin salida para crear rutas alternativas, que es lo que hace que
las persecuciones tengan gracia.

Todo el azar sale de random.Random(seed): con la misma seed, todos los
clientes generan exactamente el mismo laberinto. Por eso en la base de datos
solo se guarda la seed de la partida (un número), nunca el mapa entero.

Representación: grid de tiles de (2*celdas + 1) de lado. Las celdas lógicas
caen en coordenadas impares; entre medio quedan los muros que el generador
va abriendo.
"""
import random
from collections import deque

PASILLO = 0
MURO = 1
SALIDA = 2


class Laberinto:
    def __init__(self, celdas_ancho, celdas_alto, seed,
                 porcentaje_atajos=0.0, num_salidas=3, distancia_min_salidas=20):
        self.seed = seed
        self.celdas_ancho = celdas_ancho
        self.celdas_alto = celdas_alto
        self.ancho = celdas_ancho * 2 + 1   # en tiles
        self.alto = celdas_alto * 2 + 1
        rng = random.Random(seed)
        self.grid = [[MURO] * self.ancho for _ in range(self.alto)]
        self._excavar(rng)
        self._abrir_atajos(rng, porcentaje_atajos)
        self.salidas = self._crear_salidas(rng, num_salidas, distancia_min_salidas)

    # ------------------------------------------------------------------ #
    # Generación
    # ------------------------------------------------------------------ #

    def _excavar(self, rng):
        """Recursive backtracking iterativo sobre las celdas lógicas."""
        inicio = (rng.randrange(self.celdas_ancho), rng.randrange(self.celdas_alto))
        visitadas = {inicio}
        pila = [inicio]
        self.grid[inicio[1] * 2 + 1][inicio[0] * 2 + 1] = PASILLO
        while pila:
            cx, cy = pila[-1]
            vecinas = [(cx + dx, cy + dy)
                       for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))
                       if 0 <= cx + dx < self.celdas_ancho
                       and 0 <= cy + dy < self.celdas_alto
                       and (cx + dx, cy + dy) not in visitadas]
            if not vecinas:
                pila.pop()
                continue
            nx, ny = rng.choice(vecinas)
            # Abrir la celda destino y el muro intermedio entre ambas celdas.
            self.grid[ny * 2 + 1][nx * 2 + 1] = PASILLO
            self.grid[cy + ny + 1][cx + nx + 1] = PASILLO
            visitadas.add((nx, ny))
            pila.append((nx, ny))

    def _abrir_atajos(self, rng, porcentaje):
        """Braiding: abre una pared en un % de los callejones sin salida."""
        if porcentaje <= 0:
            return
        sin_salida = []
        for cy in range(self.celdas_alto):
            for cx in range(self.celdas_ancho):
                tx, ty = cx * 2 + 1, cy * 2 + 1
                muros = [(tx + dx, ty + dy)
                         for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))
                         if self.grid[ty + dy][tx + dx] == MURO]
                if len(muros) == 3:     # celda con una sola abertura = callejón
                    sin_salida.append((muros,))
        rng.shuffle(sin_salida)
        for (muros,) in sin_salida[:int(len(sin_salida) * porcentaje)]:
            # Abrir un muro al azar, nunca el del borde exterior del mapa.
            candidatos = [(mx, my) for mx, my in muros
                          if 0 < mx < self.ancho - 1 and 0 < my < self.alto - 1]
            if candidatos:
                mx, my = rng.choice(candidatos)
                self.grid[my][mx] = PASILLO

    def _crear_salidas(self, rng, cantidad, distancia_min):
        """Abre `cantidad` salidas en el borde, pegadas a un pasillo y separadas entre sí."""
        candidatos = []
        for tx in range(1, self.ancho - 1):
            if self.grid[1][tx] == PASILLO:
                candidatos.append((tx, 0))
            if self.grid[self.alto - 2][tx] == PASILLO:
                candidatos.append((tx, self.alto - 1))
        for ty in range(1, self.alto - 1):
            if self.grid[ty][1] == PASILLO:
                candidatos.append((0, ty))
            if self.grid[ty][self.ancho - 2] == PASILLO:
                candidatos.append((self.ancho - 1, ty))
        rng.shuffle(candidatos)

        salidas = []
        # Si no se consigue la separación pedida, se relaja el margen.
        for margen in (distancia_min, distancia_min // 2, 0):
            for tx, ty in candidatos:
                if len(salidas) == cantidad:
                    break
                if (tx, ty) not in salidas and all(
                        abs(tx - sx) + abs(ty - sy) >= margen for sx, sy in salidas):
                    salidas.append((tx, ty))
            if len(salidas) == cantidad:
                break
        for tx, ty in salidas:
            self.grid[ty][tx] = SALIDA
        return salidas

    # ------------------------------------------------------------------ #
    # Consultas
    # ------------------------------------------------------------------ #

    def es_solido(self, tx, ty):
        """True si el tile bloquea el paso (muro, o directamente fuera del mapa)."""
        if 0 <= tx < self.ancho and 0 <= ty < self.alto:
            return self.grid[ty][tx] == MURO
        return True

    def tile(self, tx, ty):
        return self.grid[ty][tx]

    def centro_mapa_px(self, tile_px):
        """Centro de la celda lógica central, en píxeles (spawn de la fase 1)."""
        tx = (self.celdas_ancho // 2) * 2 + 1
        ty = (self.celdas_alto // 2) * 2 + 1
        return (tx + 0.5) * tile_px, (ty + 0.5) * tile_px

    def camino(self, origen, destinos, evitar=None):
        """Camino más corto (BFS) desde `origen` hasta el más cercano de los
        `destinos` (un set de tiles). Devuelve la lista de tiles a recorrer,
        sin incluir el origen, o None si no hay camino.

        `evitar` es un predicado opcional tile -> bool para esquivar zonas
        peligrosas (los destinos se permiten igual: mejor escapar rozando el
        peligro que quedarse encerrado). Lo usa la IA de los bots.
        """
        if origen in destinos:
            return []
        padres = {origen: None}
        cola = deque([origen])
        while cola:
            actual = cola.popleft()
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                vecino = (actual[0] + dx, actual[1] + dy)
                if vecino in padres or self.es_solido(*vecino):
                    continue
                if evitar is not None and vecino not in destinos and evitar(vecino):
                    continue
                padres[vecino] = actual
                if vecino in destinos:
                    pasos = []
                    while vecino != origen:
                        pasos.append(vecino)
                        vecino = padres[vecino]
                    pasos.reverse()
                    return pasos
                cola.append(vecino)
        return None

    def salidas_alcanzables_desde_centro(self):
        """BFS de verificación: cuántas salidas se alcanzan desde el centro del mapa."""
        inicio = ((self.celdas_ancho // 2) * 2 + 1, (self.celdas_alto // 2) * 2 + 1)
        visitados = {inicio}
        cola = deque([inicio])
        alcanzadas = 0
        while cola:
            x, y = cola.popleft()
            if self.grid[y][x] == SALIDA:
                alcanzadas += 1
                continue
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx, ny = x + dx, y + dy
                if (0 <= nx < self.ancho and 0 <= ny < self.alto
                        and (nx, ny) not in visitados
                        and self.grid[ny][nx] != MURO):
                    visitados.add((nx, ny))
                    cola.append((nx, ny))
        return alcanzadas


if __name__ == "__main__":
    # Demo rápida sin Pygame: imprime un laberinto chico y verifica conectividad.
    # Ejecutar desde la raíz del proyecto:  python -m juego.laberinto
    lab = Laberinto(15, 10, seed=42, porcentaje_atajos=0.2, num_salidas=3)
    dibujo = {PASILLO: "  ", MURO: "██", SALIDA: "()"}
    for fila in lab.grid:
        print("".join(dibujo[t] for t in fila))
    print(f"seed=42 | salidas en {lab.salidas} | "
          f"alcanzables desde el centro: {lab.salidas_alcanzables_desde_centro()}/3")
