/**
 * Salto del Caballo (Knight's Tour)
 * Los sin chamba — Tarea grupal
 *
 * Problema:
 *   Dado un tablero de N×N, encontrar una secuencia de movimientos de un
 *   caballo de ajedrez que visite cada casilla exactamente una vez,
 *   partiendo desde la posición (0, 0).
 *
 * Técnica: Backtracking (vuelta atrás)
 *   Si un camino no lleva a solución, se retrocede y se prueba otro.
 *
 * Los 8 movimientos posibles del caballo (desplazamientos relativos):
 *   d = {(2,1), (1,2), (-1,2), (-2,1), (-2,-1), (-1,-2), (1,-2), (2,-1)}
 *
 * Condición de éxito: el caballo realizó N²-1 saltos (visitó N² casillas).
 *
 * Método de trabajo: Scrum
 *  - Daily stand-up
 *  - Planificación de sprint
 *  - Revisión de sprint
 *  - Retrospectiva
 *
 * Integrantes:
 *  - Lautaro Martinez
 *  - Gabriel Maculus
 *  - Leandro Orozco
 */

const N = 8;

const MOVIMIENTOS = [
  [2, 1], [1, 2], [-1, 2], [-2, 1],
  [-2, -1], [-1, -2], [1, -2], [2, -1]
];

// ─────────────────────────────────────────────
// Inicializar tablero: -1 = no visitada
// ─────────────────────────────────────────────

function crearTablero() {
  return Array.from({ length: N }, () => Array(N).fill(-1));
}

// ─────────────────────────────────────────────
// Verificar si una posición es válida
// ─────────────────────────────────────────────

function esValido(tablero, x, y) {
  return x >= 0 && y >= 0 && x < N && y < N && tablero[x][y] === -1;
}

// ─────────────────────────────────────────────
// Algoritmo de backtracking (recursivo)
// ─────────────────────────────────────────────

function saltoCaballo(tablero, x, y, saltoActual) {

  // Condición de éxito: se completaron N² casillas
  if (saltoActual === N * N) return true;

  // Probar los 8 movimientos posibles
  for (const [dx, dy] of MOVIMIENTOS) {
    const nx = x + dx;
    const ny = y + dy;

    if (esValido(tablero, nx, ny)) {
      // Anotar el salto
      tablero[nx][ny] = saltoActual;

      // Continuar desde la nueva posición (recursión)
      if (saltoCaballo(tablero, nx, ny, saltoActual + 1)) {
        return true;
      }

      // Vuelta atrás: borrar la anotación
      tablero[nx][ny] = -1;
    }
  }

  // Ningún movimiento llevó a solución desde esta posición
  return false;
}

// ─────────────────────────────────────────────
// Heurística de Warnsdorff (optimización)
// Elegir siempre la casilla con menos salidas posibles.
// Reduce drásticamente el tiempo de búsqueda.
// ─────────────────────────────────────────────

function contarSalidas(tablero, x, y) {
  let count = 0;
  for (const [dx, dy] of MOVIMIENTOS) {
    if (esValido(tablero, x + dx, y + dy)) count++;
  }
  return count;
}

function saltoCaballoWarnsdorff(tablero, x, y, saltoActual) {
  if (saltoActual === N * N) return true;

  // Ordenar los movimientos por cantidad de salidas (menor primero)
  const candidatos = [];
  for (const [dx, dy] of MOVIMIENTOS) {
    const nx = x + dx, ny = y + dy;
    if (esValido(tablero, nx, ny)) {
      candidatos.push({ nx, ny, salidas: contarSalidas(tablero, nx, ny) });
    }
  }
  candidatos.sort((a, b) => a.salidas - b.salidas);

  for (const { nx, ny } of candidatos) {
    tablero[nx][ny] = saltoActual;
    if (saltoCaballoWarnsdorff(tablero, nx, ny, saltoActual + 1)) return true;
    tablero[nx][ny] = -1;
  }

  return false;
}

// ─────────────────────────────────────────────
// Imprimir el tablero con el recorrido
// ─────────────────────────────────────────────

function imprimirTablero(tablero) {
  console.log('\nTablero con el recorrido del caballo:\n');
  const sep = '+' + ('----+').repeat(N);
  for (let fila = 0; fila < N; fila++) {
    console.log(sep);
    let linea = '|';
    for (let col = 0; col < N; col++) {
      linea += String(tablero[fila][col] + 1).padStart(3, ' ') + ' |';
    }
    console.log(linea);
  }
  console.log(sep);
}

// ─────────────────────────────────────────────
// Ejecución principal
// ─────────────────────────────────────────────

console.log(`\n=== Salto del Caballo — Tablero ${N}×${N} ===`);
console.log(`Casillas a visitar: ${N * N}`);
console.log(`Inicio: (0, 0)\n`);

const tablero = crearTablero();
tablero[0][0] = 0;  // La casilla inicial es el salto número 0

console.log('Resolviendo con heurística de Warnsdorff...');
const inicio = Date.now();
const encontrado = saltoCaballoWarnsdorff(tablero, 0, 0, 1);
const tiempo = Date.now() - inicio;

if (encontrado) {
  console.log(`Solución encontrada en ${tiempo}ms`);
  imprimirTablero(tablero);
} else {
  console.log('No se encontró solución desde (0, 0).');
}

/*
  Ejemplo de salida para N=8 (los números indican el orden del recorrido):

  +----+----+----+----+----+----+----+----+
  |  1 | 60 | 39 | 34 | 31 | 18 |  9 | 64 |
  +----+----+----+----+----+----+----+----+
  | 38 | 33 | 32 | 61 | 10 | 63 | 30 | 17 |
  ...  (y así hasta completar las 64 casillas)
*/
