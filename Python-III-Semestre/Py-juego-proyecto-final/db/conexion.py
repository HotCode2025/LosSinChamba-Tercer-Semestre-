"""Conexión a PostgreSQL.

La primera vez que se logra conectar, se hace el "bootstrap" completo:
si la base del juego no existe se crea (conectando a la base administrativa
'postgres'), y se aplica db/esquema.sql, que es idempotente.

Si no hay servidor disponible, todas las operaciones lanzan DBNoDisponible:
el juego la atrapa y sigue funcionando sin ranking, nunca se cuelga por la
base. Los parámetros salen de config.DB (con variables de entorno PG* como
override opcional).
"""
from pathlib import Path

import psycopg

import config


class DBNoDisponible(Exception):
    """No se pudo hablar con PostgreSQL (apagado, mal configurado, etc.)."""


_bootstrap_hecho = False


def _params(dbname):
    return dict(host=config.DB["host"], port=config.DB["port"], dbname=dbname,
                user=config.DB["user"], password=config.DB["password"],
                connect_timeout=config.DB["timeout"])


def conectar(autocommit=False):
    """Devuelve una conexión a la base del juego, creando base y esquema si
    es la primera vez. Usar con `with conectar() as con:` (hace commit solo).
    El hilo de red usa autocommit=True: cada statement confirma al instante,
    que es justo lo que el arbitraje por UPDATEs atómicos necesita."""
    global _bootstrap_hecho
    try:
        if not _bootstrap_hecho:
            _bootstrap()
            _bootstrap_hecho = True
        return psycopg.connect(**_params(config.DB["dbname"]), autocommit=autocommit)
    except psycopg.OperationalError as e:
        raise DBNoDisponible(str(e)) from e


def hay_conexion():
    """True si la base está disponible (y de paso deja el esquema aplicado)."""
    try:
        with conectar():
            return True
    except DBNoDisponible:
        return False


def _bootstrap():
    # 1) Crear la base del juego si no existe. CREATE DATABASE no puede ir
    #    dentro de una transacción, por eso autocommit.
    with psycopg.connect(**_params("postgres"), autocommit=True) as con:
        existe = con.execute("SELECT 1 FROM pg_database WHERE datname = %s",
                             (config.DB["dbname"],)).fetchone()
        if not existe:
            con.execute(f'CREATE DATABASE "{config.DB["dbname"]}"')
    # 2) Aplicar el esquema (todo IF NOT EXISTS / DROP+CREATE: idempotente).
    sql = (Path(__file__).with_name("esquema.sql")).read_text(encoding="utf-8")
    with psycopg.connect(**_params(config.DB["dbname"])) as con:
        con.execute(sql)
