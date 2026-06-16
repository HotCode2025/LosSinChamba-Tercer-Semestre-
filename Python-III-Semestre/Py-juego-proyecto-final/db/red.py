"""Sincronización en vivo del multijugador — todo a través de PostgreSQL.

Un hilo aparte habla con la base cada TICK_RED segundos, así el loop de
Pygame nunca espera un round-trip y los FPS no dependen de la red. Por tick:

  1. publica las posiciones que este cliente controla (la propia, y las de
     los bots si es el host) con un solo upsert,
  2. ejecuta los eventos encolados (reclamos de captura/escape) como
     UPDATEs atómicos — la base es el árbitro,
  3. lee el snapshot: posiciones ajenas, flags de todos y estado/reloj de
     la partida,
  4. cada ~2 s intenta cerrar la partida si ya corresponde.

Los eventos son "fire and forget": el juego los encola y sigue; la
confirmación vuelve sola en el próximo snapshot (si el UPDATE perdió la
carrera contra otro evento, el flag simplemente no aparece y no pasó nada).

El hilo y el juego comparten datos solo bajo lock. Si la base se cae, el
hilo reintenta reconectar; tras varios fallos seguidos marca `caida = True`
y el juego corta la partida avisando, en vez de colgarse.
"""
import threading
import time

import config
from db import repositorio
from db.conexion import DBNoDisponible, conectar

FALLOS_PARA_CAER = 8
CADA_CUANTO_CIERRE = 2.0    # seg entre intentos de marcar la partida terminada
REINTENTO_EVENTO = 0.7      # seg antes de poder reintentar el mismo reclamo


class RedPartida:
    def __init__(self, partida_id, mi_jugador_id):
        self.partida_id = partida_id
        self.mi_jugador_id = mi_jugador_id
        self._lock = threading.Lock()
        self._salientes = {}        # jugador_id -> (x, y) a publicar
        self._eventos = []          # ("captura", presa, cazador) | ("escape", jid)
        self._ultimo_reclamo = {}   # clave evento -> momento (para no spamear)
        # Snapshot que lee el juego:
        self.posiciones = {}        # jugador_id -> (x, y)
        self.flags = {}             # jugador_id -> (atrapado, escapado, t, capturador)
        self.estado = "jugando"
        self.t_partida = 0.0
        self.caida = False
        self._fallos = 0
        self._t_cierre = 0.0
        self._activa = True
        self._con = None
        self._hilo = threading.Thread(target=self._loop, daemon=True)
        self._hilo.start()

    # -------------------------------------------------- lado del juego --- #

    def publicar(self, jugador_id, x, y):
        with self._lock:
            self._salientes[jugador_id] = (x, y)

    def encolar_captura(self, presa_id, cazador_id):
        self._encolar(("captura", presa_id, cazador_id))

    def encolar_escape(self, jugador_id):
        self._encolar(("escape", jugador_id))

    def _encolar(self, evento):
        ahora = time.perf_counter()
        with self._lock:
            if ahora - self._ultimo_reclamo.get(evento, -99) < REINTENTO_EVENTO:
                return
            self._ultimo_reclamo[evento] = ahora
            self._eventos.append(evento)

    def snapshot(self):
        with self._lock:
            return (dict(self.posiciones), dict(self.flags),
                    self.estado, self.t_partida, self.caida)

    def detener(self):
        self._activa = False

    # -------------------------------------------------- lado del hilo --- #

    def _loop(self):
        while self._activa:
            inicio = time.perf_counter()
            try:
                if self._con is None:
                    self._con = conectar(autocommit=True)
                self._tick()
                self._fallos = 0
            except (DBNoDisponible, Exception):
                self._fallos += 1
                self._con = None        # forzar reconexión en el próximo tick
                if self._fallos >= FALLOS_PARA_CAER:
                    with self._lock:
                        self.caida = True
                    return
            resto = config.TICK_RED - (time.perf_counter() - inicio)
            time.sleep(max(0.01, resto))
        if self._con is not None:
            self._con.close()

    def _tick(self):
        con = self._con
        with self._lock:
            salientes = dict(self._salientes)
            eventos, self._eventos = self._eventos, []

        if salientes:
            repositorio.upsert_posiciones(con, self.partida_id, salientes)
        for evento in eventos:
            if evento[0] == "captura":
                repositorio.intentar_captura(con, self.partida_id,
                                             evento[1], evento[2])
            else:
                repositorio.intentar_escape(con, self.partida_id, evento[1])

        posiciones, flags, estado = repositorio.leer_sincronizacion(
            con, self.partida_id)

        ahora = time.perf_counter()
        if ahora - self._t_cierre > CADA_CUANTO_CIERRE:
            self._t_cierre = ahora
            repositorio.marcar_terminada_si_corresponde(con, self.partida_id)

        with self._lock:
            self.posiciones = {j: (x, y) for j, x, y in posiciones}
            self.flags = {j: (atr, esc, t, cap)
                          for j, atr, esc, t, cap in flags}
            if estado is not None:
                self.estado = estado[0]
                self.t_partida = float(estado[1])
