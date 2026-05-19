function miFuncion1(){
    console.log('Función 1');
}

function miFuncion2(){
    console.log('Función 2');
}

miFuncion1();
miFuncion2();

// Función de tipo callback
let imp = function imprimir(mensaje){
    console.log(mensaje);
}

function sumar(op1, op2, funcionCallback){
    let res = op1 + op2;
    funcionCallback(`Resultado: ${res}`);
}

sumar(5, 3, imp);

//Llamadas asincronas con uso setTimeout
function miFuncionCallback(){
    console.log('Saludo asincrono despues de 3 segundos');
}

setTimeout(miFuncionCallback, 3000);

setTimeout( function() { console.log('Saludo asincrono 2')}, 4000);

setTimeout( () => console.log('Saludos Asincrono 3'), 5000);

let reloj = () => {
    let fecha = new Date();
    console.log(`${fecha.getHours()}:${fecha.getMinutes()}:${fecha.getSeconds()}`);
}

setInterval(reloj, 1000);//Cada 1 segundo se ejecuta