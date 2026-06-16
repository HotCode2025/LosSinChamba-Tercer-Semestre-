-- ============================================================================
-- Esquema de "El Gran Escape" (se aplica en la fase 3).
--
-- Diseño clave: la tabla `posiciones` es UNLOGGED — no escribe en el WAL,
-- así que los UPDATE son mucho más baratos. Si Postgres se reinicia, esos
-- datos se pierden... y no importa: son efímeros, solo valen mientras la
-- partida está en curso. Lo persistente (jugadores, resultados, tiempos)
-- va en tablas normales.
-- ============================================================================

CREATE TABLE IF NOT EXISTS jugadores (
    id         SERIAL PRIMARY KEY,
    nombre     VARCHAR(30) UNIQUE NOT NULL,
    -- En single-player los bots también se registran (la partida queda
    -- completa en la base) pero los rankings los excluyen.
    es_bot     BOOLEAN NOT NULL DEFAULT FALSE,
    creado_en  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS partidas (
    id           SERIAL PRIMARY KEY,
    -- Con la seed, cada cliente regenera localmente el MISMO laberinto:
    -- nunca hace falta transmitir el mapa.
    seed         BIGINT NOT NULL,
    estado       VARCHAR(10) NOT NULL DEFAULT 'esperando'
                 CHECK (estado IN ('esperando', 'jugando', 'terminada')),
    host_id      INT REFERENCES jugadores(id),  -- quien creó la sala: arranca
                                                -- la partida y simula los bots
    iniciada_en  TIMESTAMPTZ,
    terminada_en TIMESTAMPTZ
);
-- Para bases creadas antes de la fase 4 (ADD COLUMN es idempotente):
ALTER TABLE partidas ADD COLUMN IF NOT EXISTS host_id INT REFERENCES jugadores(id);

CREATE TABLE IF NOT EXISTS jugadores_partida (
    partida_id    INT NOT NULL REFERENCES partidas(id),
    jugador_id    INT NOT NULL REFERENCES jugadores(id),
    rol           VARCHAR(10) NOT NULL CHECK (rol IN ('escapista', 'cazador')),
    slot          INT NOT NULL DEFAULT 0,         -- puesto dentro del rol: define
                                                  -- el spawn (determinista por seed)
    atrapado      BOOLEAN NOT NULL DEFAULT FALSE,
    escapado      BOOLEAN NOT NULL DEFAULT FALSE,
    capturado_por INT REFERENCES jugadores(id),   -- alimenta el ranking de cazadores
    tiempo_escape REAL,                           -- segundos; NULL si no escapó
    PRIMARY KEY (partida_id, jugador_id)
);
ALTER TABLE jugadores_partida ADD COLUMN IF NOT EXISTS slot INT NOT NULL DEFAULT 0;
-- Dos clientes no pueden quedarse con el mismo puesto: si la carrera ocurre,
-- uno de los dos INSERT viola este índice y el cliente reintenta.
CREATE UNIQUE INDEX IF NOT EXISTS ux_jp_partida_rol_slot
    ON jugadores_partida (partida_id, rol, slot);

-- Posiciones en vivo: cada cliente hace UPDATE de su fila ~10 veces por
-- segundo y un SELECT de las otras. fillfactor bajo deja lugar en la página
-- para que esos UPDATE constantes sean "HOT updates" (sin tocar índices).
CREATE UNLOGGED TABLE IF NOT EXISTS posiciones (
    partida_id     INT NOT NULL,
    jugador_id     INT NOT NULL,
    x              REAL NOT NULL,
    y              REAL NOT NULL,
    actualizado_en TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (partida_id, jugador_id)
) WITH (fillfactor = 50);

-- ----------------------------------------------------------------------------
-- El árbitro de las capturas es la atomicidad de Postgres. Una captura se
-- reclama con un UPDATE condicional; si dos eventos compiten (dos cazadores,
-- o "te atrapo" vs "llegué a la salida"), la base serializa y gana uno solo:
--
--   UPDATE jugadores_partida
--      SET atrapado = TRUE, capturado_por = :cazador_id
--    WHERE partida_id = :partida AND jugador_id = :presa
--      AND atrapado = FALSE AND escapado = FALSE;
--
--   UPDATE jugadores_partida
--      SET escapado = TRUE, tiempo_escape = :segundos
--    WHERE partida_id = :partida AND jugador_id = :yo
--      AND atrapado = FALSE AND escapado = FALSE;
--
-- Si rowcount == 0, el evento "perdió" contra otro ya confirmado.
-- ----------------------------------------------------------------------------

-- Rankings (DROP + CREATE para poder cambiar columnas sin migraciones).
-- Escapistas: la MEJOR marca de cada jugador, no sus 10 corridas — un solo
-- jugador no puede llenar el top.
DROP VIEW IF EXISTS ranking_escapistas;
CREATE VIEW ranking_escapistas AS
SELECT j.nombre,
       MIN(jp.tiempo_escape) AS mejor_tiempo,
       COUNT(*)              AS escapes
  FROM jugadores_partida jp
  JOIN jugadores j ON j.id = jp.jugador_id
 WHERE jp.escapado AND NOT j.es_bot
 GROUP BY j.nombre
 ORDER BY mejor_tiempo ASC
 LIMIT 10;

-- Cazadores: capturas acumuladas (solo capturas hechas por humanos).
DROP VIEW IF EXISTS ranking_cazadores;
CREATE VIEW ranking_cazadores AS
SELECT j.nombre, COUNT(*) AS capturas
  FROM jugadores_partida jp
  JOIN jugadores j ON j.id = jp.capturado_por
 WHERE NOT j.es_bot
 GROUP BY j.nombre
 ORDER BY capturas DESC
 LIMIT 5;
