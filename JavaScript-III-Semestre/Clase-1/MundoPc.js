class DispositivoEntrada {
    #tipoEntrada;
    #marca;

    constructor(tipoEntrada, marca) {
        this.#tipoEntrada = tipoEntrada;
        this.#marca = marca;
    }

    get tipoEntrada() {
        return this.#tipoEntrada;
    }

    set tipoEntrada(tipoEntrada) {
        this.#tipoEntrada = tipoEntrada;
    }

    get marca() {
        return this.#marca;
    }

    set marca(marca) {
        this.#marca = marca;
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
        return Teclado._contadorTeclados;
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

