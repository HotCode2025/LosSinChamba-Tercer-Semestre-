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

    set monitor(monitor

