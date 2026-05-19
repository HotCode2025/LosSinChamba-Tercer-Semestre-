/*
  script.js — N Reinas

  Básicamente lo que hace este archivo es resolver el problema
  usando backtracking. La idea es ir columna por columna
  intentando poner una reina en alguna fila. Si en algún punto
  no hay ninguna fila disponible, se deshace el último movimiento
  y se prueba otra opción. Así hasta encontrar una solución o
  confirmar que no existe.

  Además de resolver, todo se va mostrando en el tablero paso
  a paso con una pequeña pausa entre movimientos para que se
  pueda ver el proceso.

  ─── Autoría ───────────────────────────────────────────────
  Estructura base e integración general : Lautaro Martinez
  Algoritmo de backtracking (solveWithAnimation, isSafe) : Gabriel Maculus
  Renderizado del tablero (renderEmptyBoard) : Leandro Orozco
  Control de animación (sleep, animationDelay, stopRequested) : Kevin Castilla
  Eventos de controles / botones (solveBtn, resetBtn) : Ezequiel Diaz
  Sección de resultados (showResult, hideResult) : Jose Rodriguez
  Mensajes de estado y errores (setStatus, showError) : Jose Rodriguez
  ────────────────────────────────────────────────────────────
*/

// ── Lautaro Martinez: referencias al DOM ──
const nInput     = document.getElementById('nInput');
const solveBtn   = document.getElementById('solveBtn');
const resetBtn   = document.getElementById('resetBtn');
const errorMsg   = document.getElementById('errorMsg');
const statusMsg  = document.getElementById('statusMsg');
const boardEl    = document.getElementById('board');
const resultArea = document.getElementById('resultArea');
const resultArr  = document.getElementById('resultArray');

// ── Kevin Castilla: variables de control de animación ──
// animationDelay es cuánto espera entre cada paso (en ms),
// y stopRequested sirve para cortar la animación si el usuario
// presiona Resolver otra vez antes de que termine.
let animationDelay = 80;
let stopRequested  = false;

// ── Ezequiel Diaz: evento del botón Resolver ──
solveBtn.addEventListener('click', async () => {
  const n = parseInt(nInput.value, 10);

  // Si meten un número menor a 8 o algo que no es número, corto acá
  if (isNaN(n) || n < 8) {
    showError(true);
    return;
  }
  showError(false);

  // Si ya hay una animación corriendo, la freno antes de arrancar otra
  stopRequested = true;
  await sleep(animationDelay * 2);
  stopRequested = false;

  // Para tableros chicos lo hago más lento para que se vea mejor,
  // y para los grandes lo acelero porque sino tarda una eternidad
  animationDelay = n <= 10 ? 30 : n <= 14 ? 15 : 5;

  solveBtn.disabled = true;
  hideResult();
  setStatus('searching', '⏳ Buscando solución...');
  renderEmptyBoard(n);

  // Espero un tick para que el navegador termine de dibujar el tablero
  // antes de empezar a modificarlo
  await sleep(50);

  // queens[col] guarda en qué fila está la reina de esa columna.
  // Arranco todo en -1 (sin reina)
  const queens = new Array(n).fill(-1);
  const found  = await solveWithAnimation(queens, 0, n);

  if (found) {
    setStatus('found', '✅ ¡Solución encontrada!');
    showResult(queens);
  } else {
    setStatus('not-found', '❌ No existe solución para este valor.');
  }

  solveBtn.disabled = false;
  resetBtn.classList.remove('hidden');
});

// ── Ezequiel Diaz: evento del botón Reiniciar ──
resetBtn.addEventListener('click', () => {
  // Corta cualquier animación que esté corriendo
  stopRequested = true;

  // Limpia el tablero, el estado y el resultado
  boardEl.innerHTML = '';
  hideResult();
  statusMsg.classList.add('hidden');
  showError(false);

  // Vuelve el input a 8
  nInput.value = 8;

  // Reactiva el botón de resolver y oculta el de reiniciar
  solveBtn.disabled = false;
  resetBtn.classList.add('hidden');
});

// ── Gabriel Maculus: algoritmo principal de backtracking ──
// Recibe el estado actual del tablero (queens), la columna
// en la que está parado (col), y el tamaño N.
// Va probando cada fila de la columna actual. Si la posición
// está libre, pone la reina y llama a la función de nuevo
// para la siguiente columna. Si ninguna fila sirve, retorna
// false y el llamador deshace su movimiento.
async function solveWithAnimation(queens, col, n) {
  // Si ya llegué a la columna N significa que puse todas las reinas
  if (col === n) return true;

  for (let row = 0; row < n; row++) {
    // Si el usuario pidió parar, salgo
    if (stopRequested) return false;

    // Pinto la celda para mostrar que la estoy evaluando
    highlightRow(col, row, n);

    if (isSafe(queens, col, row)) {
      // La posición es válida, pongo la reina
      queens[col] = row;
      placeQueen(col, row, n, false);

      // Solo hago el await acá (una sola vez por paso válido)
      await sleep(animationDelay);

      // Sigo con la siguiente columna
      const result = await solveWithAnimation(queens, col + 1, n);
      if (result) return true;

      // Si llegué acá es porque esa rama no funcionó,
      // así que saco la reina y pruebo la siguiente fila
      queens[col] = -1;
      removeQueen(col, row, n);
    } else {
      // Solo freno en celdas inválidas con un delay más corto
      await sleep(Math.floor(animationDelay / 3));
    }

    clearHighlightRow(col, row, n);
  }

  // Probé todas las filas y ninguna funcionó
  return false;
}

// ── Gabriel Maculus: verificación de posición segura (isSafe) ──
// Las columnas nunca se repiten porque pongo exactamente una
// reina por columna, así que solo tengo que revisar:
//   - que no haya otra reina en la misma fila
//   - que no haya otra reina en ninguna de las dos diagonales
// La diagonal se detecta comparando la diferencia de filas
// con la diferencia de columnas.
function isSafe(queens, col, row) {
  for (let c = 0; c < col; c++) {
    const r = queens[c];
    if (r === -1) continue;

    const mismaFila   = r === row;
    const diagonalSup = r - c === row - col;  // diagonal hacia arriba
    const diagonalInf = r + c === row + col;  // diagonal hacia abajo

    if (mismaFila || diagonalSup || diagonalInf) return false;
  }
  return true;
}

// ── Leandro Orozco: generación del tablero (renderEmptyBoard) ──
// El tamaño de cada celda se calcula para que entre en pantalla
// sin importar qué tan grande sea N. El mínimo es 28px y el
// máximo 64px. Cada celda tiene un id único para poder
// encontrarla rápido después.
function renderEmptyBoard(n) {
  boardEl.innerHTML = '';

  const cellSize = Math.max(28, Math.min(64, Math.floor(560 / n)));

  boardEl.style.gridTemplateColumns = `repeat(${n}, ${cellSize}px)`;
  boardEl.style.gridTemplateRows    = `repeat(${n}, ${cellSize}px)`;

  for (let row = 0; row < n; row++) {
    for (let col = 0; col < n; col++) {
      const cell = document.createElement('div');
      cell.classList.add('cell');
      // El color del ajedrez depende de si la suma fila+col es par o impar
      cell.classList.add((row + col) % 2 === 0 ? 'light' : 'dark');
      cell.id = `cell-${col}-${row}`;
      cell.style.width  = `${cellSize}px`;
      cell.style.height = `${cellSize}px`;
      cell.style.fontSize = `${cellSize * 0.55}px`;
      boardEl.appendChild(cell);
    }
  }
}

// ── Leandro Orozco: manejo visual de las reinas en el tablero ──
function placeQueen(col, row, n, conflict = false) {
  const cell = getCell(col, row);
  if (!cell) return;
  cell.classList.remove('conflict');
  cell.classList.add(conflict ? 'conflict' : 'queen');
}

// Borra la reina de esa celda
function removeQueen(col, row, n) {
  const cell = getCell(col, row);
  if (!cell) return;
  cell.classList.remove('queen', 'conflict');
}

// Pinta la celda de amarillo para indicar que la estamos evaluando
function highlightRow(col, row, n) {
  const cell = getCell(col, row);
  if (cell) cell.classList.add('active');
}

/**
 * Quita el resaltado de una celda.
 */
// Quita el resaltado amarillo una vez que terminamos de evaluar esa celda
function clearHighlightRow(col, row, n) {
  const cell = getCell(col, row);
  if (cell) cell.classList.remove('active');
}

// Busca la celda por su id. Si por alguna razón no existe devuelve null
// y las funciones que la llaman ya se encargan de no explotar.
function getCell(col, row) {
  return document.getElementById(`cell-${col}-${row}`);
}

// ── Jose Rodriguez: mostrar arreglo de posiciones (showResult) ──
function showResult(queens) {
  resultArr.innerHTML = '';

  queens.forEach((row, col) => {
    const badge = document.createElement('span');
    badge.classList.add('idx-badge');
    badge.textContent = row;
    badge.title = `Columna ${col} → Fila ${row}`;
    resultArr.appendChild(badge);
  });

  const fullLine = document.createElement('p');
  fullLine.classList.add('full-array');
  fullLine.textContent = `[ ${queens.join(', ')} ]`;
  resultArr.appendChild(fullLine);

  resultArea.classList.remove('hidden');
}

// ── Jose Rodriguez: limpiar resultado (hideResult) ──
function hideResult() {
  resultArea.classList.add('hidden');
  resultArr.innerHTML = '';
}

// ── Jose Rodriguez: mensaje de estado (setStatus) ──
function setStatus(type, msg) {
  statusMsg.textContent = msg;
  statusMsg.className   = `status ${type}`;
  statusMsg.classList.remove('hidden');
}

// ── Ezequiel Diaz: mostrar/ocultar error de validación ──
function showError(show) {
  errorMsg.classList.toggle('hidden', !show);
}

// ── Kevin Castilla: helper de pausa para animación (sleep) ──
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}
