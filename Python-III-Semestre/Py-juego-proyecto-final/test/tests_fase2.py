"""Pruebas de la fase 2 sin abrir ventana.

Corre partidas completas solo entre bots (rol_jugador=None) y verifica que
las reglas cierren solas: la partida termina, cada escapista queda escapado
o atrapado (o se agotó el tiempo), los tiempos y capturas son coherentes.

Ejecutar:  python tests_fase2.py
"""
import time

import config
from juego.partida import Partida


def correr(seed):
    p = Partida(seed, rol_jugador=None)
    dt = 1 / 30
    pasos_max = int((config.TIEMPO_LIMITE + 10) / dt)
    for _ in range(pasos_max):
        p.actualizar(dt)
        if p.terminada:
            break
    assert p.terminada, f"seed {seed}: la partida no terminó"
    for e in p.escapistas:
        assert e.escapado or e.atrapado or p.motivo_fin == "tiempo", \
            f"seed {seed}: {e.nombre} quedó sin resolver"
        if e.escapado:
            assert e.tiempo_escape is not None and 0 < e.tiempo_escape <= p.tiempo
        if e.atrapado:
            assert e.capturado_por in p.cazadores
    assert sum(c.capturas for c in p.cazadores) == p.n_atrapados
    print(f"seed {seed}: fin a los {p.tiempo:5.1f}s ({p.motivo_fin}) - "
          f"escaparon {p.n_escapados}, atrapados {p.n_atrapados}")


inicio = time.perf_counter()
for seed in (1, 2, 3, 4, 5):
    correr(seed)
print(f"OK — 5 partidas simuladas en {time.perf_counter() - inicio:.1f}s")
