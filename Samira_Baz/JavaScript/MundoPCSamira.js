// ==========================================================================
// PROYECTO: SISTEMA DE VENTAS DE COMPUTADORAS (UML a Código)
// ==========================================================================

// ==========================================================================
// PASO 1: LA CLASE PADRE
// Conceptos: Clases, Constructor, Encapsulamiento (Getters/Setters)
// ==========================================================================
class DispositivoEntrada {
    constructor(tipoEntrada, marca) {
        // En JavaScript, por convención, a los atributos que van a tener
        // Getters y Setters se les pone un guion bajo adelante (_). 
        // Esto indica que son "privados" y evita un bucle infinito con el Setter.
        this._tipoEntrada = tipoEntrada;
        this._marca = marca;
    }

    // GETTER: El "portero" que te deja leer el dato.
    get tipoEntrada() {
        return this._tipoEntrada;
    }

    // SETTER: El "guardia" que te deja modificar el dato.
    set tipoEntrada(tipoEntrada) {
        this._tipoEntrada = tipoEntrada;
    }

    get marca() {
        return this._marca;
    }

    set marca(marca) {
        this._marca = marca;
    }
}

// --- PRUEBA PASO 1 ---
console.log("--- Prueba Paso 1: DispositivoEntrada ---");
let inputBase = new DispositivoEntrada("USB", "Genérica");
console.log("Marca original:", inputBase.marca); // Usa el Getter
inputBase.marca = "Logitech"; // Usa el Setter
console.log("Marca modificada:", inputBase.marca);


// ==========================================================================
// PASO 2: LAS CLASES HIJAS (Periféricos)
// Conceptos: Herencia (extends), 'super', Atributos Estáticos (Contadores)
// ==========================================================================
class Raton extends DispositivoEntrada {
    // ATRIBUTO ESTÁTICO: Le pertenece a la CLASE Raton, no a un ratón individual.
    static contadorRatones = 0;

    constructor(tipoEntrada, marca) {
        // 'super' llama al constructor de la clase padre (DispositivoEntrada).
        // Así nos ahorramos volver a escribir la lógica de _tipoEntrada y _marca.
        super(tipoEntrada, marca);
        
        // Cada vez que se crea un objeto Raton, el contador de la clase suma 1,
        // y ese número se le asigna como ID único al objeto actual.
        this._idRaton = ++Raton.contadorRatones;
    }

    get idRaton() {
        return this._idRaton;
    }
    // OJO: No hacemos un "set idRaton" porque el ID se genera automático y no
    // debería poder cambiarse a mano. (Cumplimos con el diseño de no alterar IDs).

    toString() {
        // toString resume el estado del objeto. Usamos 'this.marca' para llamar al Getter del padre.
        return `Raton [ID: ${this._idRaton}, Tipo: ${this.tipoEntrada}, Marca: ${this.marca}]`;
    }
}

class Teclado extends DispositivoEntrada {
    static contadorTeclados = 0;

    constructor(tipoEntrada, marca) {
        super(tipoEntrada, marca);
        this._idTeclado = ++Teclado.contadorTeclados;
    }

    get idTeclado() { return this._idTeclado; }

    toString() {
        return `Teclado [ID: ${this._idTeclado}, Tipo: ${this.tipoEntrada}, Marca: ${this.marca}]`;
    }
}

// --- PRUEBA PASO 2 ---
console.log("\n--- Prueba Paso 2: Herencia y Contadores ---");
let raton1 = new Raton("Bluetooth", "HP");
let raton2 = new Raton("USB", "Razer");
let teclado1 = new Teclado("USB", "Redragon");
console.log(raton1.toString()); // Va a tener ID 1
console.log(raton2.toString()); // Va a tener ID 2 (¡El contador estático funciona!)
console.log(teclado1.toString());


// ==========================================================================
// PASO 3: CLASE INDEPENDIENTE (Monitor)
// ==========================================================================
class Monitor {
    static contadorMonitores = 0;

    constructor(marca, tamanio) {
        this._idMonitor = ++Monitor.contadorMonitores;
        this._marca = marca;
        this._tamanio = tamanio;
    }

    // El diagrama pedía explícitamente: "agregar el método get solo idMonitor"
    get idMonitor() {
        return this._idMonitor;
    }
    
    get marca() { return this._marca; }
    set marca(marca) { this._marca = marca; }
    get tamanio() { return this._tamanio; }
    set tamanio(tamanio) { this._tamanio = tamanio; }

    toString() {
        return `Monitor [ID: ${this._idMonitor}, Marca: ${this._marca}, Tamaño: ${this._tamanio}]`;
    }
}


// ==========================================================================
// PASO 4: AGREGACIÓN / COMPOSICIÓN (Computadora)
// Conceptos: Unir objetos dentro de otro objeto
// ==========================================================================
class Computadora {
    static contadorComputadoras = 0;

    // Fíjate en los parámetros: recibe OBJETOS (unMonitor, unTeclado, unRaton),
    // no simples textos o números.
    constructor(nombre, monitor, teclado, raton) {
        this._idComputadora = ++Computadora.contadorComputadoras;
        this._nombre = nombre;
        this._monitor = monitor; // Agregación del objeto Monitor
        this._teclado = teclado; // Agregación del objeto Teclado
        this._raton = raton;     // Agregación del objeto Raton
    }

    toString() {
        // Al imprimir esto, automáticamente llama al toString() de cada objeto interno.
        return `Computadora ${this._idComputadora}: ${this._nombre} \n  ${this._monitor} \n  ${this._teclado} \n  ${this._raton}`;
    }
}

// --- PRUEBA PASO 3 Y 4 ---
console.log("\n--- Prueba Paso 3 y 4: Armando la Computadora ---");
let monitor1 = new Monitor("Samsung", "24 Pulgadas");
// Usamos los objetos creados en la prueba 2 para armar la compu:
let compu1 = new Computadora("PC Gamer", monitor1, teclado1, raton2); 
console.log(compu1.toString());


// ==========================================================================
// PASO 5: LA COLECCIÓN / LOGICA DE NEGOCIO (Orden)
// Conceptos: Arreglos de objetos
// ==========================================================================
class Orden {
    static contadorOrdenes = 0;

    constructor() {
        this._idOrden = ++Orden.contadorOrdenes;
        // Inicializamos '_computadoras' como un arreglo vacío [].
        // Aquí vamos a ir guardando las computadoras que agreguemos.
        this._computadoras = []; 
    }

    // Método para sumar una computadora al arreglo
    agregarComputadora(computadora) {
        this._computadoras.push(computadora);
    }

    // Método para imprimir el "ticket"
    mostrarOrden() {
        let computadorasOrden = '';
        // Recorremos el arreglo y juntamos el texto de cada computadora
        for (let computadora of this._computadoras) {
            computadorasOrden += `\n${computadora.toString()}`;
        }

        console.log(`\n========================================`);
        console.log(`Orden: ${this._idOrden}`);
        console.log(`Computadoras en la orden: ${computadorasOrden}`);
        console.log(`========================================`);
    }
}

// --- PRUEBA FINAL ---
console.log("\n--- Prueba Paso 5: Generando una Venta ---");
let orden1 = new Orden();
orden1.agregarComputadora(compu1); // Agregamos la PC Gamer

// Creamos otra PC rápida para la orden
let monitor2 = new Monitor("Dell", "27 Pulgadas");
let compu2 = new Computadora("PC Oficina", monitor2, teclado1, raton1);

orden1.agregarComputadora(compu2); // Agregamos la segunda PC a la misma orden
orden1.mostrarOrden(); // Imprimimos el resultado final