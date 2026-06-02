// Definimos el tamaño del tablero (8x8)
const N = 8;

// Los 8 posibles movimientos del caballo (ejes X e Y)
// Como los ejemplos: d = {(2,1), (1,2), (-1,2), (-2,1), (-2,-1), (-1,-2), (1,-2), (2,-1)}
const movX = [2, 1, -1, -2, -2, -1, 1, 2];
const movY = [1, 2, 2, 1, -1, -2, -2, -1];

// Función para verificar si la casilla destino es válida y no fue sido visitada
function esMovimientoValido(x, y, tablero) {
    return (x >= 0 && x < N && y >= 0 && y < N && tablero[x][y] === -1);
}

// Cuenta cuántos movimientos válidos hay desde una casilla específica
// Esto es parte de la optimización para que no tarde horas en resolverse
function contarMovimientosPosibles(x, y, tablero) {
    let cuenta = 0;
    for (let i = 0; i < 8; i++) {
        if (esMovimientoValido(x + movX[i], y + movY[i], tablero)) {
            cuenta++;
        }
    }
    return cuenta;
}

// Función principal de Backtracking
function resolverSaltoCaballo(x, y, saltoActual, tablero) {
    // Condición de éxito: Si el caballo dio los 64 saltos (del 0 al 63)
    if (saltoActual === N * N) {
        return true;
    }

    // Recopilamos los próximos movimientos posibles
    let proximosMovimientos = [];
    for (let i = 0; i < 8; i++) {
        let siguienteX = x + movX[i];
        let siguienteY = y + movY[i];
        
        if (esMovimientoValido(siguienteX, siguienteY, tablero)) {
            // Guardamos el movimiento y calculamos cuántas salidas tendrá esa futura casilla
            let futurasSalidas = contarMovimientosPosibles(siguienteX, siguienteY, tablero);
            proximosMovimientos.push({ x: siguienteX, y: siguienteY, salidas: futurasSalidas });
        }
    }

    // OPTIMIZACIÓN (Regla de Warnsdorff): 
    // Ordenamos los movimientos para ir primero a las casillas que tienen MENOS salidas futuras.
    // Esto evita que el caballo quede atrapado y hace que el algoritmo sea ultra rápido.
    proximosMovimientos.sort((a, b) => a.salidas - b.salidas);

    // Bucle principal de VUELTA ATRÁS (Backtracking)
    for (let i = 0; i < proximosMovimientos.length; i++) {
        let sigX = proximosMovimientos[i].x;
        let sigY = proximosMovimientos[i].y;

        // Anotamos el salto en el tablero
        tablero[sigX][sigY] = saltoActual;

        // Llamada recursiva: intentamos seguir desde esta nueva posición
        if (resolverSaltoCaballo(sigX, sigY, saltoActual + 1, tablero)) {
            return true; // Si el camino llevó a la solución, terminamos
        }

        // Si la llamada recursiva devolvió false, significa que este camino no sirvió.
        // VUELTA ATRÁS (Backtracking): Borramos la anotación y probamos el siguiente movimiento.
        tablero[sigX][sigY] = -1;
    }

    // Si probamos todos los movimientos y ninguno sirve, retornamos false
    return false;
}

// Función para inicializar todo e imprimir el resultado
function iniciarJuego() {
    // Creamos una matriz 8x8 llena de -1 (indicando casillas vacías)
    let tablero = Array.from({ length: N }, () => Array(N).fill(-1));

    // El caballo inicia en la posición (0,0) según la consigna
    tablero[0][0] = 0; // El primer paso es el paso 0

    console.log("Calculando el salto del caballo...");

    // Iniciamos la recursividad desde (0,0) buscando el salto 1
    if (resolverSaltoCaballo(0, 0, 1, tablero)) {
        console.log("¡Solución encontrada!");
        // Imprimimos el tablero formateado
        for (let i = 0; i < N; i++) {
            // Formateamos los números para que la cuadrícula se vea prolija en consola
            console.log(tablero[i].map(num => num.toString().padStart(2, '0')).join(' | '));
        }
    } else {
        console.log("No existe solución para este tablero.");
    }
}

// Ejecutamos el programa
iniciarJuego();