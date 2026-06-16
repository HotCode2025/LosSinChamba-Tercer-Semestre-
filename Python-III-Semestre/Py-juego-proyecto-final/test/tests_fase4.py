"""Pruebas de la fase 4 contra PostgreSQL real: lobby, sincronización entre
dos clientes de red y el arbitraje atómico de capturas/escapes.

Simula a "A" (host, escapista) y "B" (cazador) como dos clientes de verdad:
cada uno con su RedPartida (hilo + conexión propia). Verifica que:
  * el lobby respeta cupos y slots,
  * el host rellena los puestos vacíos con bots al arrancar,
  * una posición publicada por A aparece en el snapshot de B (y viceversa),
  * la captura solo vale si las posiciones EN LA BASE están cerca,
  * nadie puede ser capturado dos veces ni escapar ya atrapado,
  * la partida se cierra sola cuando todos los escapistas están resueltos.

Ejecutar:  python tests_fase4.py
"""
import random
import time

import config
from db import repositorio
from db.conexion import conectar
from db.red import RedPartida

sufijo = random.randrange(10**6)
A, B, C = (f"_test4_{sufijo}_{x}" for x in "ABC")

# --- 1) Lobby: crear, listar, unirse, cupos ----------------------------- #
pid, a_id = repositorio.crear_partida_multi(A, "escapista", seed=4242)
assert any(p[0] == pid for p in repositorio.partidas_esperando()), "la sala no se lista"

b_id, slot_b = repositorio.unirse_a_partida(pid, B, "cazador")
assert slot_b == 0, f"slot de B: {slot_b}"
c_id, slot_c = repositorio.unirse_a_partida(pid, C, "cazador")
assert slot_c == 1, f"slot de C: {slot_c}"
_, slot_lleno = repositorio.unirse_a_partida(pid, f"{C}x", "cazador")
assert slot_lleno is None, "dejó entrar un tercer cazador"
repositorio.abandonar_partida(pid, c_id)        # C se arrepiente y se va
print(f"1) lobby OK (sala #{pid}: host + cazador, cupos respetados)")

# --- 2) El host arranca: bots de relleno + estado 'jugando' -------------- #
assert not repositorio.arrancar_partida(pid, b_id), "arrancó alguien que no es host"
assert repositorio.arrancar_partida(pid, a_id)
jugadores = repositorio.jugadores_de(pid)
assert len(jugadores) == 5 and sum(1 for j in jugadores if j[4]) == 3, jugadores
assert repositorio.estado_de(pid)[0] == "jugando"
print("2) arranque OK (2 humanos + 3 bots de relleno, estado 'jugando')")

# --- 3) Sincronización real entre dos clientes de red -------------------- #
red_a = RedPartida(pid, a_id)
red_b = RedPartida(pid, b_id)
red_a.publicar(a_id, 333.0, 444.0)
red_b.publicar(b_id, 555.0, 666.0)
limite = time.perf_counter() + 3.0
visto = False
while time.perf_counter() < limite and not visto:
    time.sleep(0.05)
    pos_b = red_b.snapshot()[0]
    pos_a = red_a.snapshot()[0]
    visto = pos_b.get(a_id) == (333.0, 444.0) and pos_a.get(b_id) == (555.0, 666.0)
red_a.detener()
red_b.detener()
assert visto, "las posiciones no cruzaron por la base en 3 segundos"
print("3) sincronización OK (A y B se ven mutuamente a través de la base)")

# --- 4) Arbitraje atómico ------------------------------------------------ #
bots_esc = [j[0] for j in jugadores if j[2] == "escapista" and j[4]]
presa1, presa2 = bots_esc[0], bots_esc[1]
with conectar(autocommit=True) as con:
    # B (100, 100) y presa1 (160, 180): dist 100 px <= 110 -> captura válida.
    repositorio.upsert_posiciones(con, pid, {b_id: (100.0, 100.0),
                                             presa1: (160.0, 180.0),
                                             presa2: (3000.0, 3000.0)})
    assert repositorio.intentar_captura(con, pid, presa1, b_id), "captura válida rechazada"
    assert not repositorio.intentar_captura(con, pid, presa1, b_id), \
        "capturó dos veces a la misma presa"
    assert not repositorio.intentar_escape(con, pid, presa1), "escapó estando atrapado"
    assert not repositorio.intentar_captura(con, pid, presa2, b_id), \
        "capturó a 4000 px de distancia (validación de posición rota)"
    assert repositorio.intentar_escape(con, pid, presa2), "escape válido rechazado"
    tiempo = con.execute(
        "SELECT tiempo_escape FROM jugadores_partida WHERE partida_id=%s"
        " AND jugador_id=%s", (pid, presa2)).fetchone()[0]
    assert tiempo is not None and tiempo > 0, f"tiempo de escape: {tiempo}"
    print(f"4) arbitraje OK (captura con distancia validada, sin dobles eventos;"
          f" escape cronometrado por la base: {tiempo:.2f}s)")

    # --- 5) Cierre de partida -------------------------------------------- #
    repositorio.marcar_terminada_si_corresponde(con, pid)
    assert repositorio.estado_de(pid)[0] == "jugando", "cerró con A todavía libre"
    repositorio.upsert_posiciones(con, pid, {a_id: (150.0, 150.0)})
    assert repositorio.intentar_captura(con, pid, a_id, b_id)  # B caza al host
    repositorio.marcar_terminada_si_corresponde(con, pid)
    assert repositorio.estado_de(pid)[0] == "terminada", "no cerró con todos resueltos"
    print("5) cierre OK (la partida se marcó 'terminada' sola, una sola vez)")

    # --- 6) El ranking ve la partida online ------------------------------ #
    assert any(n == B and c == 2 for n, c in repositorio.ranking_cazadores()), \
        "las 2 capturas de B no aparecen en el ranking"
    print("6) ranking OK (las capturas online cuentan)")

    # --- limpieza --------------------------------------------------------- #
    con.execute("DELETE FROM posiciones WHERE partida_id = %s", (pid,))
    con.execute("DELETE FROM jugadores_partida WHERE partida_id = %s", (pid,))
    con.execute("DELETE FROM partidas WHERE id = %s", (pid,))
    con.execute("DELETE FROM jugadores WHERE nombre LIKE %s", (f"_test4_{sufijo}%",))
print("OK - fase 4 verificada y datos de prueba borrados")
