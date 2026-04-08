class DispositivoEntrada {
    constructor(tipoEntrada, marca) {
        this.tipoEntrada = tipoEntrada;
        this.marca = marca;
    }
    
    get tipoEntrada() {
        return this._tipoEntrada;
    }
    
    set tipoEntrada(tipoEntrada) {
        this._tipoEntrada = tipoEntrada;
    }
    
    get marca() {
        return this._marca; // CORRECCIÓN: Faltaba el guion bajo
    }
    
    set marca(marca) {
        this._marca = marca;
    }
}

class Raton extends DispositivoEntrada {
    static contadorRatones = 0;

    constructor(tipoEntrada, marca) {
        super(tipoEntrada, marca);
        this._idRaton = ++Raton.contadorRatones;
    }
    
    get idRaton() { // CORRECCIÓN: El getter no debe llevar guion bajo en el nombre
        return this._idRaton; 
    }
    
    toString() {
        return `Raton: [idRaton: ${this._idRaton}, tipoEntrada: ${this._tipoEntrada}, marca: ${this._marca}]`;
    }
}

let raton1 = new Raton('USB', 'HP');
console.log(raton1.toString()); // Raton: [idRaton: 1, tipoEntrada: USB, marca: HP]

let raton2 = new Raton('Bluetooth', 'Dell');
console.log(raton2.toString()); // Raton: [idRaton: 2, tipoEntrada: Bluetooth, marca: Dell]