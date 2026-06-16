"""Operaciones del juego sobre la base de datos.

Todo lo que el juego le pide a PostgreSQL pasa por acá: registrar jugadores,
guardar partidas terminadas y leer los rankings. Cualquier función puede
lanzar DBNoDisponible si el servidor no está; el que llama decide qué hacer
(el juego muestra "sin conexión" y sigue).

Los bots también se registran (con es_bot = TRUE y nombre prefijado "[bot]"),
así la partida queda completa en la base — igual que será en la fase 4 con
5 humanos — pero las vistas de ranking los excluyen.
"""
import psycopg

import config
from db.conexion import conectar, DBNoDisponible  # noqa: F401  (re-export)

CUPOS = {"escapista": config.NUM_ESCAPISTAS, "cazador": config.NUM_CAZADORES}


def obtener_o_crear_jugador(con, nombre, es_bot=False):
    """Devuelve el id del jugador, creándolo si no existe.
    El ON CONFLICT ... DO UPDATE es para que RETURNING devuelva la fila
    también cuando el jugador ya existía."""
    fila = con.execute(
        """INSERT INTO jugadores (nombre, es_bot) VALUES (%s, %s)
           ON CONFLICT (nombre) DO UPDATE SET es_bot = EXCLUDED.es_bot
           RETURNING id""",
        (nombre, es_bot)).fetchone()
    return fila[0]


def guardar_partida(partida, nombre_humano):
    """Registra una partida terminada completa: la fila en `partidas` y una
    en `jugadores_partida` por participante. Devuelve el id de partida."""
    with conectar() as con:
        ids = {}
        for e in partida.entidades:
            nombre = nombre_humano if e.es_humano else f"[bot] {e.nombre}"
            ids[id(e)] = obtener_o_crear_jugador(con, nombre, es_bot=not e.es_humano)

        partida_id = con.execute(
            """INSERT INTO partidas (seed, estado, iniciada_en, terminada_en)
               VALUES (%s, 'terminada', now() - make_interval(secs => %s), now())
               RETURNING id""",
            (partida.seed, partida.tiempo)).fetchone()[0]

        slots = {"escapista": 0, "cazador": 0}
        for e in partida.entidades:
            capturador = ids[id(e.capturado_por)] if e.capturado_por else None
            con.execute(
                """INSERT INTO jugadores_partida
                       (partida_id, jugador_id, rol, slot, atrapado, escapado,
                        capturado_por, tiempo_escape)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                (partida_id, ids[id(e)], e.rol, slots[e.rol], e.atrapado, e.escapado,
                 capturador, e.tiempo_escape))
            slots[e.rol] += 1
        return partida_id


# ------------------------------------------------------------------ #
# Fase 4 — lobby
# ------------------------------------------------------------------ #


def crear_partida_multi(nombre_host, rol_host, seed):
    """Crea una sala en estado 'esperando' con el host ya adentro (slot 0).
    Devuelve (partida_id, host_id)."""
    with conectar() as con:
        host_id = obtener_o_crear_jugador(con, nombre_host)
        partida_id = con.execute(
            "INSERT INTO partidas (seed, estado, host_id)"
            " VALUES (%s, 'esperando', %s) RETURNING id",
            (seed, host_id)).fetchone()[0]
        con.execute(
            "INSERT INTO jugadores_partida (partida_id, jugador_id, rol, slot)"
            " VALUES (%s, %s, %s, 0)", (partida_id, host_id, rol_host))
        return partida_id, host_id


def partidas_esperando():
    """[(id, nombre_host, n_escapistas, n_cazadores)] — salas abiertas."""
    with conectar() as con:
        return con.execute(
            """SELECT p.id, j.nombre,
                      COUNT(*) FILTER (WHERE jp.rol = 'escapista'),
                      COUNT(*) FILTER (WHERE jp.rol = 'cazador')
                 FROM partidas p
                 JOIN jugadores j ON j.id = p.host_id
            LEFT JOIN jugadores_partida jp ON jp.partida_id = p.id
                WHERE p.estado = 'esperando'
                GROUP BY p.id, j.nombre
                ORDER BY p.id DESC
                LIMIT 9""").fetchall()


def unirse_a_partida(partida_id, nombre, rol):
    """Intenta ocupar un puesto. Devuelve (jugador_id, slot) o (jugador_id,
    None) si no había cupo / la sala ya arrancó. El slot se calcula y se
    inserta en un solo statement; si dos clientes compiten por el mismo,
    el índice único hace fallar a uno y se devuelve None (puede reintentar)."""
    with conectar() as con:
        jugador_id = obtener_o_crear_jugador(con, nombre)
        try:
            fila = con.execute(
                """INSERT INTO jugadores_partida (partida_id, jugador_id, rol, slot)
                   SELECT %(p)s, %(j)s, %(rol)s::varchar, COALESCE(MAX(slot) + 1, 0)
                     FROM jugadores_partida
                    WHERE partida_id = %(p)s AND rol = %(rol)s
                   HAVING COUNT(*) < %(cupo)s
                      AND EXISTS (SELECT 1 FROM partidas
                                  WHERE id = %(p)s AND estado = 'esperando')
                   ON CONFLICT (partida_id, jugador_id) DO NOTHING
                   RETURNING slot""",
                dict(p=partida_id, j=jugador_id, rol=rol,
                     cupo=CUPOS[rol])).fetchone()
        except psycopg.errors.UniqueViolation:
            return jugador_id, None
        return jugador_id, (fila[0] if fila else None)


def jugadores_de(partida_id):
    """[(jugador_id, nombre, rol, slot, es_bot)] de una partida."""
    with conectar() as con:
        return con.execute(
            """SELECT jp.jugador_id, j.nombre, jp.rol, jp.slot, j.es_bot
                 FROM jugadores_partida jp
                 JOIN jugadores j ON j.id = jp.jugador_id
                WHERE jp.partida_id = %s
                ORDER BY jp.rol, jp.slot""", (partida_id,)).fetchall()


def estado_de(partida_id):
    """(estado, seed, host_id) o None si la sala ya no existe (host se fue)."""
    with conectar() as con:
        return con.execute(
            "SELECT estado, seed, host_id FROM partidas WHERE id = %s",
            (partida_id,)).fetchone()


def arrancar_partida(partida_id, host_id):
    """Solo el host: rellena los cupos vacíos con bots (que él va a simular)
    y pasa la sala a 'jugando'. Los demás clientes lo detectan por polling."""
    with conectar() as con:
        es_host = con.execute(
            "SELECT 1 FROM partidas WHERE id = %s AND host_id = %s"
            " AND estado = 'esperando'", (partida_id, host_id)).fetchone()
        if not es_host:
            return False
        for rol, cupo in CUPOS.items():
            ocupados = {s for (s,) in con.execute(
                "SELECT slot FROM jugadores_partida WHERE partida_id = %s"
                " AND rol = %s", (partida_id, rol)).fetchall()}
            for slot in range(cupo):
                if slot not in ocupados:
                    bot_id = obtener_o_crear_jugador(
                        con, f"[bot] {rol.capitalize()} {slot + 1}", es_bot=True)
                    con.execute(
                        "INSERT INTO jugadores_partida"
                        " (partida_id, jugador_id, rol, slot)"
                        " VALUES (%s, %s, %s, %s)",
                        (partida_id, bot_id, rol, slot))
        con.execute(
            "UPDATE partidas SET estado = 'jugando', iniciada_en = now()"
            " WHERE id = %s", (partida_id,))
        return True


def abandonar_partida(partida_id, jugador_id):
    """Salir de una sala en espera. Si se va el host, la sala se borra."""
    with conectar() as con:
        fila = con.execute(
            "SELECT host_id, estado FROM partidas WHERE id = %s",
            (partida_id,)).fetchone()
        if fila is None or fila[1] != "esperando":
            return      # en juego no se borra nada: quedás como "no escapó"
        if jugador_id == fila[0]:
            con.execute("DELETE FROM posiciones WHERE partida_id = %s", (partida_id,))
            con.execute("DELETE FROM jugadores_partida WHERE partida_id = %s",
                        (partida_id,))
            con.execute("DELETE FROM partidas WHERE id = %s", (partida_id,))
        else:
            con.execute(
                "DELETE FROM jugadores_partida WHERE partida_id = %s"
                " AND jugador_id = %s", (partida_id, jugador_id))


# ------------------------------------------------------------------ #
# Fase 4 — sincronización en vivo (las llama el hilo de red con SU conexión)
# ------------------------------------------------------------------ #


def upsert_posiciones(con, partida_id, posiciones):
    """Publica las posiciones {jugador_id: (x, y)} de este cliente."""
    con.cursor().executemany(
        """INSERT INTO posiciones (partida_id, jugador_id, x, y)
           VALUES (%s, %s, %s, %s)
           ON CONFLICT (partida_id, jugador_id)
           DO UPDATE SET x = EXCLUDED.x, y = EXCLUDED.y, actualizado_en = now()""",
        [(partida_id, j, x, y) for j, (x, y) in posiciones.items()])


def intentar_captura(con, partida_id, presa_id, cazador_id):
    """El UPDATE condicional atómico que arbitra el juego: solo captura si la
    presa sigue libre Y las posiciones registradas en la base están a menos
    de DIST_VALIDA_CAPTURA px. Si dos eventos compiten, Postgres serializa
    y gana exactamente uno. Devuelve True si la captura fue de este cazador."""
    d2 = config.DIST_VALIDA_CAPTURA ** 2
    cur = con.execute(
        """UPDATE jugadores_partida
              SET atrapado = TRUE, capturado_por = %(caz)s
            WHERE partida_id = %(p)s AND jugador_id = %(presa)s
              AND atrapado = FALSE AND escapado = FALSE
              AND EXISTS (SELECT 1
                            FROM posiciones a, posiciones b
                           WHERE a.partida_id = %(p)s AND a.jugador_id = %(caz)s
                             AND b.partida_id = %(p)s AND b.jugador_id = %(presa)s
                             AND (a.x - b.x) * (a.x - b.x)
                               + (a.y - b.y) * (a.y - b.y) <= %(d2)s)""",
        dict(p=partida_id, presa=presa_id, caz=cazador_id, d2=d2))
    return cur.rowcount == 1


def intentar_escape(con, partida_id, jugador_id):
    """Reclama el escape; el tiempo lo pone el reloj de la BASE (now() -
    iniciada_en), así no depende del reloj de ningún cliente. Si te
    atraparon un instante antes (fila ya atrapada), rowcount = 0."""
    cur = con.execute(
        """UPDATE jugadores_partida jp
              SET escapado = TRUE,
                  tiempo_escape = EXTRACT(EPOCH FROM (now() - pa.iniciada_en))
             FROM partidas pa
            WHERE pa.id = jp.partida_id
              AND jp.partida_id = %s AND jp.jugador_id = %s
              AND jp.atrapado = FALSE AND jp.escapado = FALSE
              AND pa.estado = 'jugando'""", (partida_id, jugador_id))
    return cur.rowcount == 1


def leer_sincronizacion(con, partida_id):
    """Todo lo que un cliente necesita por tick: posiciones ajenas, flags de
    cada jugador y estado/reloj de la partida (según la base)."""
    posiciones = con.execute(
        "SELECT jugador_id, x, y FROM posiciones WHERE partida_id = %s",
        (partida_id,)).fetchall()
    flags = con.execute(
        """SELECT jugador_id, atrapado, escapado, tiempo_escape, capturado_por
             FROM jugadores_partida WHERE partida_id = %s""",
        (partida_id,)).fetchall()
    estado = con.execute(
        """SELECT estado, COALESCE(EXTRACT(EPOCH FROM (now() - iniciada_en)), 0)
             FROM partidas WHERE id = %s""", (partida_id,)).fetchone()
    return posiciones, flags, estado


def marcar_terminada_si_corresponde(con, partida_id):
    """Cualquier cliente puede cerrar la partida; el WHERE garantiza que el
    cierre ocurra una sola vez y solo cuando corresponde (todos los
    escapistas resueltos, o tiempo límite vencido)."""
    con.execute(
        """UPDATE partidas
              SET estado = 'terminada', terminada_en = now()
            WHERE id = %(p)s AND estado = 'jugando'
              AND (NOT EXISTS (SELECT 1 FROM jugadores_partida
                                WHERE partida_id = %(p)s AND rol = 'escapista'
                                  AND atrapado = FALSE AND escapado = FALSE)
                   OR now() > iniciada_en + make_interval(secs => %(lim)s))""",
        dict(p=partida_id, lim=config.TIEMPO_LIMITE))


def ranking_escapistas():
    """[(nombre, mejor_tiempo, escapes_totales)] — top 10, sin bots."""
    with conectar() as con:
        return con.execute("SELECT * FROM ranking_escapistas").fetchall()


def ranking_cazadores():
    """[(nombre, capturas_totales)] — top 5, sin bots."""
    with conectar() as con:
        return con.execute("SELECT * FROM ranking_cazadores").fetchall()
