import config
from juego.entidad import Entidad

class DummyLab:
    def es_solido(self, x, y):
        # Pared a la derecha (x=2), sin piso (y=2 no es sólido salvo que x=2)
        if x == 2: return True
        return False

ent = Entidad("Test", "escapista", 50, 50, 100, 14, (0,0,0))

def nuevo_mover_eje(self, dx, dy, laberinto, tile_px):
    if not dx and not dy:
        return
    eps = 0.001
    if dx != 0:
        self.x += dx
        leading_x = self.x + self.radio if dx > 0 else self.x - self.radio
        tx = int(leading_x // tile_px)
        ty_min = int((self.y - self.radio + eps) // tile_px)
        ty_max = int((self.y + self.radio - eps) // tile_px)
        hit = False
        for ty in range(ty_min, ty_max + 1):
            if laberinto.es_solido(tx, ty):
                hit = True
                break
        if hit:
            if dx > 0:
                self.x = tx * tile_px - self.radio
            elif dx < 0:
                self.x = (tx + 1) * tile_px + self.radio

    if dy != 0:
        self.y += dy
        leading_y = self.y + self.radio if dy > 0 else self.y - self.radio
        ty = int(leading_y // tile_px)
        tx_min = int((self.x - self.radio + eps) // tile_px)
        tx_max = int((self.x + self.radio - eps) // tile_px)
        hit = False
        for tx in range(tx_min, tx_max + 1):
            if laberinto.es_solido(tx, ty):
                hit = True
                break
        if hit:
            if dy > 0:
                self.y = ty * tile_px - self.radio
            elif dy < 0:
                self.y = (ty + 1) * tile_px + self.radio

Entidad._mover_eje = nuevo_mover_eje

lab = DummyLab()
tile_px = 32

print(f"Inicio: x={ent.x}, y={ent.y}")

ent._mover_eje(10, 0, lab, tile_px)
print(f"Tras mover der: x={ent.x}, y={ent.y} (Esperado: x=50, y=50)")

ent._mover_eje(0, 5, lab, tile_px)
print(f"Tras mover aba: x={ent.x}, y={ent.y} (Esperado: x=50, y=55)")

ent._mover_eje(-5, 0, lab, tile_px)
print(f"Tras mover izq: x={ent.x}, y={ent.y} (Esperado: x=45, y=55)")

ent._mover_eje(0, -10, lab, tile_px)
print(f"Tras mover arr: x={ent.x}, y={ent.y} (Esperado: x=45, y=45)")
