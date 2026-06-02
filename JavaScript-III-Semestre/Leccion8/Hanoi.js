/**
 * Torres de Hanoi — Algoritmo Recursivo
 * LGL Solutions — Tarea grupal
 *
 * Reglas del problema:
 *  - n discos apilados en el poste A (mayor abajo, menor arriba)
 *  - Mover todos los discos al poste C en el mismo orden
 *  - Solo se puede mover un disco a la vez (el que está arriba)
 *  - No se puede poner un disco más grande sobre uno más pequeño
 *
 * Solución: divide y vencerás (recursión)
 *  1. Mover los (n-1) discos superiores de A → B usando C como auxiliar
 *  2. Mover el disco más grande de A → C
 *  3. Mover los (n-1) discos de B → C usando A como auxiliar
 *
 * Cantidad de movimientos: 2^n − 1
 *
 * Método de trabajo: Scrum
 *  - Daily stand-up
 *  - Planificación de sprint
 *  - Revisión y retrospectiva
 *
 * Integrantes:
 *  - Lautaro Martinez
 *  - Gabriel Maculus
 *  - Leandro Orozco
 */

// ─────────────────────────────────────────────
// Algoritmo recursivo
// ─────────────────────────────────────────────

function hanoi(n, desde, hasta, auxiliar) {
  if (n === 1) {
    console.log(`Mover disco 1 de ${desde} → ${hasta}`);
    return;
  }

  // Paso 1: mover n-1 discos del poste origen al auxiliar
  hanoi(n - 1, desde, auxiliar, hasta);

  // Paso 2: mover el disco más grande al destino
  console.log(`Mover disco ${n} de ${desde} → ${hasta}`);

  // Paso 3: mover los n-1 discos del auxiliar al destino
  hanoi(n - 1, auxiliar, hasta, desde);
}


// ─────────────────────────────────────────────
// Versión que retorna los pasos como array
// ─────────────────────────────────────────────

function hanoiPasos(n, desde = 'A', hasta = 'C', auxiliar = 'B', pasos = []) {
  if (n === 1) {
    pasos.push({ disco: 1, desde, hasta });
    return pasos;
  }

  hanoiPasos(n - 1, desde, auxiliar, hasta, pasos);
  pasos.push({ disco: n, desde, hasta });
  hanoiPasos(n - 1, auxiliar, hasta, desde, pasos);

  return pasos;
}


// ─────────────────────────────────────────────
// Ejecución de ejemplo
// ─────────────────────────────────────────────

const N = 3; // cantidad de discos

console.log(`\n=== Torres de Hanoi con ${N} discos ===`);
console.log(`Movimientos mínimos necesarios: 2^${N} - 1 = ${Math.pow(2, N) - 1}\n`);

// Opción A: imprime los pasos directamente
hanoi(N, 'A', 'C', 'B');

// Opción B: obtener los pasos como array para procesar
const pasos = hanoiPasos(N);
console.log(`\nTotal de movimientos: ${pasos.length}`);

/*
  Salida esperada con N=3:
  Mover disco 1 de A → C
  Mover disco 2 de A → B
  Mover disco 1 de C → B
  Mover disco 3 de A → C
  Mover disco 1 de B → A
  Mover disco 2 de B → C
  Mover disco 1 de A → C
  Total de movimientos: 7
*/