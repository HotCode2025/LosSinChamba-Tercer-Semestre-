let ataqueJugador
let ataqueEnemigo

function iniciarJuego(){
    let botonPersonajeJugador = document.getElementById('boton-personaje');
    botonPersonajeJugador.addEventListener ('click', seleccionarPersonajeJugador);

    let botonPunio = document.getElementById('boton-punio') //Ahora creamos un escudo
    botonPunio.addEventListener('click', ataquePunio)
    let botonPatada = document.getElementById('boton-patada')
    botonPatada.addEventListener('click', ataquePatada)
    let botonBarrida = document.getElementById('boton-barrida')
    botonBarrida.addEventListener('click', ataqueBarrida)

}
//Tarea
function seleccionarPersonajeJugador() {
    let inputZuko = document.getElementById('zuko');
    let inputKatara = document.getElementById('katara');
    let inputAang = document.getElementById('aang');
    let inputToph = document.getElementById('toph');
    let spanPersonajeJugador = document.getElementById('personaje-jugador');

    // Modificación: Enviamos el nombre del personaje elegido por el jugador a la función del enemigo
    if (inputZuko.checked) {
        spanPersonajeJugador.innerHTML = 'Zuko';
        seleccionarPersonajeEnemigo('Zuko'); 
    } else if (inputKatara.checked) {
        spanPersonajeJugador.innerHTML = 'Katara';
        seleccionarPersonajeEnemigo('Katara');
    } else if (inputAang.checked) {
        spanPersonajeJugador.innerHTML = 'Aang';
        seleccionarPersonajeEnemigo('Aang');
    } else if (inputToph.checked) {
        spanPersonajeJugador.innerHTML = 'Toph';
        seleccionarPersonajeEnemigo('Toph');
    } else {
        alert('Por favor, selecciona un personaje primero.');
    }
}

//Tarea
// Modificación: La función ahora recibe el parámetro 'personajeJugador'
function seleccionarPersonajeEnemigo(personajeJugador) {
    let spanPersonajeEnemigo = document.getElementById('personaje-enemigo');
    
    let personajeAleatorio;
    let nombreEnemigo = "";

    // Usamos un bucle 'while' para asegurarnos de que el enemigo no sea igual al jugador
    while (nombreEnemigo === "" || nombreEnemigo === personajeJugador) {
        // Genera un número aleatorio entre 1 y 4 (Usando la función reutilizable de abajo)
        personajeAleatorio = aleatorio(1, 4);

        // Asigna temporalmente el nombre según el número
        if (personajeAleatorio == 1) {
            nombreEnemigo = 'Zuko';
        } else if (personajeAleatorio == 2) {
            nombreEnemigo = 'Katara';
        } else if (personajeAleatorio == 3) {
            nombreEnemigo = 'Aang';
        } else if (personajeAleatorio == 4) {
            nombreEnemigo = 'Toph';
        }
        // Si 'nombreEnemigo' es igual a 'personajeJugador', el bucle se repite y saca otro número
    }

    // Cuando encuentra uno diferente, sale del bucle y lo muestra en el HTML
    spanPersonajeEnemigo.innerHTML = nombreEnemigo;
}

function ataquePunio(){ //Modificamos la variable global ataqueJugador
    ataqueJugador = 'Punio'
    ataqueAleatorioEnemigo()
}

function ataquePatada(){ //Modificamos la variable global ataqueJugador
    ataqueJugador = 'Patada'
    ataqueAleatorioEnemigo()
}

function ataqueBarrida(){ //Modificamos la variable global ataqueJugador
    ataqueJugador = 'Barrida'
    ataqueAleatorioEnemigo()
}

function ataqueAleatorioEnemigo(){ //Ahora ocupando la variable global nueva le decimos el ataque y necesitamos la función aleatoria
    let ataqueAleatorio = aleatorio(1, 3)

    if(ataqueAleatorio == 1){
        ataqueEnemigo = 'Punio'
    } else if(ataqueAleatorio == 2){
        ataqueEnemigo = 'Patada'
    } else {
        ataqueEnemigo = 'Barrida'
    }
    combate()
}


function combate(){
    if(ataqueEnemigo == ataqueJugador){
        crearMensaje("EMPATE 🤝")
    } else if(ataqueJugador == 'Punio' && ataqueEnemigo == 'Barrida'){
        crearMensaje("GANASTE 🎉")
    } else if(ataqueJugador == 'Patada' && ataqueEnemigo == 'Punio'){
        crearMensaje("GANASTE 🎉")
    } else if(ataqueJugador == 'Barrida' && ataqueEnemigo == 'Patada'){
        crearMensaje("GANASTE 🎉")
    } else {
        crearMensaje("PERDISTE ❌")
    }
}


function crearMensaje(resultado){
    let sectionMensaje = document.getElementById('mensajes')
    let parrafo = document.createElement('p')

    parrafo.innerHTML = 'Tu personaje atacó con ' + ataqueJugador + ', el personaje del enemigo atacó con ' + ataqueEnemigo + ' ' + resultado

    sectionMensaje.appendChild(parrafo)
}

function aleatorio(min, max) {
    return Math.floor(Math.random() * (max - min + 1) + min);
}

window.addEventListener('load', iniciarJuego);