"""Pruebas de la fase 3 contra PostgreSQL de verdad (requiere el servidor
corriendo; la base y el esquema se crean solos si faltan).

Guarda dos partidas con un jugador de prueba —una como escapista con tiempo
conocido, otra como cazador con dos capturas— y verifica que los rankings
devuelvan exactamente eso y que los bots queden excluidos. Al final borra
los datos de prueba.

Ejecutar:  python tests_fase3.py
"""
import random

from db import repositorio
from db.conexion import conectar
from juego.partida import Partida

NOMBRE_TEST = f"_test_{random.randrange(10**6)}"

# 1) Partida como escapista: simular unos ticks y forzar un resultado conocido
#    (acá se prueba el repositorio, no la IA).
p1 = Partida(101, "escapista")
for _ in range(30):
    p1.actualizar(1 / 30, (1, 0))
p1.jugador.escapado = True
p1.jugador.tiempo_escape = 33.3
pid1 = repositorio.guardar_partida(p1, NOMBRE_TEST)
print(f"partida escapista guardada con id {pid1}")

# 2) Partida como cazador: el humano captura a dos bots.
p2 = Partida(102, "cazador")
for presa in p2.escapistas[:2]:
    presa.atrapado = True
    presa.capturado_por = p2.jugador
    p2.jugador.capturas += 1
pid2 = repositorio.guardar_partida(p2, NOMBRE_TEST)
print(f"partida cazador guardada con id {pid2}")

# 3) Los rankings tienen que reflejarlo (y nunca incluir bots).
escapistas = repositorio.ranking_escapistas()
cazadores = repositorio.ranking_cazadores()
assert any(n == NOMBRE_TEST and abs(t - 33.3) < 0.01
           for n, t, _ in escapistas), escapistas
assert any(n == NOMBRE_TEST and c == 2 for n, c in cazadores), cazadores
assert all(not fila[0].startswith("[bot]") for fila in escapistas + cazadores)
print("rankings correctos (tiempo 33.3s y 2 capturas presentes, sin bots)")

# 4) Limpieza: borrar las partidas y el jugador de prueba.
with conectar() as con:
    con.execute("DELETE FROM jugadores_partida WHERE partida_id = ANY(%s)",
                ([pid1, pid2],))
    con.execute("DELETE FROM partidas WHERE id = ANY(%s)", ([pid1, pid2],))
    con.execute("DELETE FROM jugadores WHERE nombre = %s", (NOMBRE_TEST,))
print("OK - datos de prueba borrados")
