/**
 * Algoritmo recursivo para resolver las Torres de Hanoi.
 * * @param {number} n - Cantidad de discos a mover.
 * @param {string} origen - Nombre de la varilla inicial (ej. 'A').
 * @param {string} destino - Nombre de la varilla final (ej. 'C').
 * @param {string} auxiliar - Nombre de la varilla de apoyo (ej. 'B').
 */
function resolverTorresDeHanoi(n, origen, destino, auxiliar) {
    // CASO BASE: Es la condición de corte de nuestra recursividad.
    // Si solo queda un disco por mover, simplemente lo pasamos del origen al destino.
    if (n === 1) {
        console.log(`Mover disco 1 de la varilla ${origen} a la varilla ${destino}`);
        return;
    }

    // PASO 1: Mover los n-1 discos que están arriba del disco más grande
    // desde la varilla de 'origen' hacia la varilla 'auxiliar'.
    // Usamos la varilla de 'destino' temporalmente como apoyo.
    resolverTorresDeHanoi(n - 1, origen, auxiliar, destino);

    // PASO 2: Ahora que el disco más grande (n) está libre, 
    // lo movemos directamente a su varilla de destino final.
    console.log(`Mover disco ${n} de la varilla ${origen} a la varilla ${destino}`);

    // PASO 3: Finalmente, movemos esos n-1 discos que dejamos esperando en la 
    // varilla 'auxiliar' hacia la varilla de 'destino'.
    // Esta vez usamos la varilla de 'origen' como apoyo.
    resolverTorresDeHanoi(n - 1, auxiliar, destino, origen);
}

//PRUEBA DE EJECUCIÓN
const cantidadDeDiscos = 3; // Podés cambiar este número para probar, igual que en los GIFs
console.log(`--- Iniciando Torres de Hanoi con ${cantidadDeDiscos} discos ---`);

// Llamamos a la función: 
// origen = A, destino = C, auxiliar = B
resolverTorresDeHanoi(cantidadDeDiscos, 'A', 'C', 'B');