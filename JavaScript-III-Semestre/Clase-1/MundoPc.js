class DispositivoEntrada {
    _tipoEntrada;
    _marca;

    constructor(tipoEntrada, marca) {
        this._tipoEntrada = tipoEntrada;
        this._marca = marca;
    }

    get tipoEntrada() {
        return this._tipoEntrada;
    }

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

class Raton extends DispositivoEntrada {
    static contadorRatones = 0;
    _idRaton;

    constructor(tipoEntrada, marca) {
        super(tipoEntrada, marca);
        Raton.contadorRatones++;
        this._idRaton = Raton.contadorRatones;
    }

    get idRaton() {
        return this._idRaton;
    }

    static get contadorRatones() {
        return Raton.contadorRatones;
    }

    toString() {
        return `Raton: [IdRaton: ${this._idRaton}, Tipo: ${this.tipoEntrada}, Marca: ${this.marca}]`;
    }
}

class Teclado extends DispositivoEntrada {
    static contadorTeclados = 0;
    _idTeclado;

    constructor(tipoEntrada, marca) {
        super(tipoEntrada, marca);
        Teclado.contadorTeclados++;
        this._idTeclado = Teclado.contadorTeclados;
    }

    get idTeclado() {
        return this._idTeclado;
    }

    static get contadorTeclados() {
        return Teclado.contadorTeclados;
    }

    toString() {
        return `Teclado [ID: ${this._idTeclado}, Tipo: ${this.tipoEntrada}, Marca: ${this.marca}]`;
    }
}

class Monitor {
    static contadorMonitores = 0;
    _idMonitor;
    _marca;
    _tamano;

    constructor(marca, tamano) {
        Monitor.contadorMonitores++;
        this._idMonitor = Monitor.contadorMonitores;
        this._marca = marca;
        this._tamano = tamano;
    }

    get idMonitor() {
        return this._idMonitor;
    }

    get marca() {
        return this._marca;
    }

    set marca(marca) {
        this._marca = marca;
    }

    get tamano() {
        return this._tamano;
    }

    set tamano(tamano) {
        this._tamano = tamano;
    }

    static get contadorMonitores() {
        return Monitor.contadorMonitores;
    }

    toString() {
        return `Monitor [ID: ${this._idMonitor}, Marca: ${this._marca}, Tamaño: ${this._tamano}]`;
    }
}

class Computadora {
    static contadorComputadoras = 0;
    _idComputadora;
    _nombre;
    _monitor;
    _teclado;
    _raton;

    constructor(nombre, monitor, teclado, raton) {
        Computadora.contadorComputadoras++;
        this._idComputadora = Computadora.contadorComputadoras;
        this._nombre = nombre;
        this._monitor = monitor;
        this._teclado = teclado;
        this._raton = raton;
    }

    get idComputadora() {
        return this._idComputadora;
    }

    get nombre() {
        return this._nombre;
    }

    set nombre(nombre) {
        this._nombre = nombre;
    }

    get monitor() {
        return this._monitor;
    }

    set monitor(monitor) {
        this._monitor = monitor;
    }

    get teclado() {
        return this._teclado;
    }

    set teclado(teclado) {
        this._teclado = teclado;
    }

    get raton() {
        return this._raton;
    }

    set raton(raton) {
        this._raton = raton;
    }

    static get contadorComputadoras() {
        return Computadora.contadorComputadoras;
    }

    toString() {
        return `Computadora [ID: ${this._idComputadora}, Nombre: ${this._nombre}\n` +
               `  ${this._monitor.toString()}\n` +
               `  ${this._teclado.toString()}\n` +
               `  ${this._raton.toString()}\n]`;
    }
}

class Orden {
    static contadorOrdenes = 0;
    _idOrden;
    _computadoras;

    constructor() {
        Orden.contadorOrdenes++;
        this._idOrden = Orden.contadorOrdenes;
        this._computadoras = [];
    }

    get idOrden() {
        return this._idOrden;
    }

    get computadoras() {
        return [...this._computadoras];
    }

    static get contadorOrdenes() {
        return Orden.contadorOrdenes;
    }

    agregarComputadora(computadora) {
        if (computadora instanceof Computadora) {
            this._computadoras.push(computadora);
        } else {
            console.error("Error: Solo se pueden agregar objetos de tipo Computadora");
        }
    }

    mostrarOrden() {
        console.log(`\n========== ORDEN #${this._idOrden} ==========`);
        console.log(`Total de computadoras: ${this._computadoras.length}`);
        
        if (this._computadoras.length === 0) {
            console.log("No hay computadoras en esta orden");
        } else {
            this._computadoras.forEach((computadora, index) => {
                console.log(`\n--- Computadora ${index + 1} ---`);
                console.log(computadora.toString());
            });
        }
        console.log("==========================================\n");
    }
}

// Crear dispositivos
const monitor1 = new Monitor("Samsung", "24 pulgadas");
const teclado1 = new Teclado("Mecánico", "Logitech");
const raton1 = new Raton("Óptico", "Razer");

const monitor2 = new Monitor("LG", "27 pulgadas");
const teclado2 = new Teclado("Membrana", "HP");
const raton2 = new Raton("Inalámbrico", "Logitech");

// Crear computadoras
const computadora1 = new Computadora("PC Gamer", monitor1, teclado1, raton1);
const computadora2 = new Computadora("PC Oficina", monitor2, teclado2, raton2);
const computadora3 = new Computadora("PC Diseño", monitor1, teclado2, raton1);

// Crear órdenes
const orden1 = new Orden();
const orden2 = new Orden();

// Agregar computadoras a las órdenes
orden1.agregarComputadora(computadora1);
orden1.agregarComputadora(computadora2);

orden2.agregarComputadora(computadora3);
orden2.agregarComputadora(computadora1);

// Mostrar órdenes
orden1.mostrarOrden();
orden2.mostrarOrden();

// Mostrar contadores
console.log("=== CONTADORES ESTÁTICOS ===");
console.log(`Monitores creados: ${Monitor.contadorMonitores}`);
console.log(`Teclados creados: ${Teclado.contadorTeclados}`);
console.log(`Ratones creados: ${Raton.contadorRatones}`);
console.log(`Computadoras creadas: ${Computadora.contadorComputadoras}`);
console.log(`Órdenes creadas: ${Orden.contadorOrdenes}`);
