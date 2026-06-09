# 🔥 La Leyenda de Aang — Combate por Turnos

Un proyecto realizado con **HTML y JavaScript** inspirado en *Avatar: La Leyenda de Aang*. En esta versión del juego, el jugador puede elegir un personaje, enfrentarse a un enemigo seleccionado aleatoriamente y combatir mediante un sistema de ataques por turnos.

Este proyecto representa una evolución respecto de la primera versión, incorporando manipulación avanzada del DOM, eventos, generación aleatoria y lógica de combate.

---

## 🎮 ¿Qué hace esta versión?

* Permite elegir un personaje mediante botones de selección (`radio buttons`).
* Los personajes disponibles son:

  * Zuko 🔥
  * Katara 💧
  * Aang 🌪️
  * Toph 🌱
* Al presionar **Seleccionar**, el personaje elegido se muestra en pantalla.
* El enemigo es seleccionado automáticamente de forma aleatoria.
* El enemigo nunca puede ser el mismo personaje que el jugador.
* El jugador puede realizar tres ataques:

  * Punio 👊
  * Patada 🦵
  * Barrida 🦶
* El enemigo elige su ataque aleatoriamente.
* Cada ronda puede terminar en:

  * GANASTE 🎉
  * PERDISTE ❌
  * EMPATE 🤝
* Los resultados del combate se agregan dinámicamente al historial de mensajes.

---

## 📂 Estructura del proyecto

```text
LA LEYENDA DE AANG/
├── avatar.html      → Estructura e interfaz del juego
├── js/
│   └── avatar.js    → Lógica principal del juego
└── README.md        → Documentación del proyecto
```

---

# 📄 Explicación del código

## avatar.html

El archivo HTML contiene la estructura visual del juego.

---

### 1. Encabezado principal

```html
<h1>AVATAR 🔥 💧 🌱 🌪️</h1>
```

Es el título principal del proyecto.

> La etiqueta `<h1>` representa el encabezado más importante de la página y normalmente se utiliza una sola vez.

**Colaboraron:** Gabriel Maculus · Lautaro Martinez

---

### 2. Selección de personaje

```html
<section id="seleccionar-personaje">
```

Permite al jugador elegir uno de los cuatro personajes disponibles.

Ejemplo:

```html
<label for="zuko">Zuko</label>
<input type="radio" name="personaje" id="zuko"/>
```

Todos los inputs poseen:

```html
name="personaje"
```

Esto hace que pertenezcan al mismo grupo y solo pueda seleccionarse uno.

| Personaje | Elemento  |
| --------- | --------- |
| Zuko      | 🔥 Fuego  |
| Katara    | 💧 Agua   |
| Aang      | 🌪️ Aire  |
| Toph      | 🌱 Tierra |

El botón de selección:

```html
<button id="boton-personaje">
    Seleccionar
</button>
```

inicia la lógica del juego.

**Colaboraron:** Gabriel Maculus · Samira Baz

---

### 3. Sección de ataques

```html
<section id="seleccionar-ataque">
```

Contiene los botones de combate.

Ataques disponibles:

```html
<button id="boton-punio">Punio</button>
<button id="boton-patada">Patada</button>
<button id="boton-barrida">Barrida</button>
```

Cuando el jugador selecciona un ataque:

1. Se registra el ataque elegido.
2. El enemigo genera un ataque aleatorio.
3. Se ejecuta el combate.
4. Se muestra el resultado.

**Colaboraron:** Gabriel Maculus · Leandro Orozco
**Documentación y seguimiento:** Mariano Rasgido

---

### 4. Sección de mensajes

```html
<section id="mensajes">
```

Muestra el historial del combate.

Cada ronda genera automáticamente un nuevo mensaje indicando:

* Ataque del jugador.
* Ataque del enemigo.
* Resultado.

**Colaboraron:** Samira Baz · Leandro Orozco

---

### 5. Reiniciar partida

```html
<section id="reiniciar">
```

Contiene el botón destinado a reiniciar el juego en futuras versiones.

```html
<button id="boton-reiniciar">
    Reiniciar
</button>
```

Actualmente aún no posee funcionalidad.

**Colaboraron:** Gabriel Maculus
**Documentación y seguimiento:** Mariano Rasgido

---

# avatar.js

Este archivo contiene toda la lógica del juego.

---

## 1. Variables globales

```javascript
let ataqueJugador
let ataqueEnemigo
```

Almacenan los ataques elegidos por cada participante para poder compararlos durante el combate.

**Colaboraron:** Lautaro Martinez · Leandro Orozco
**Documentación y seguimiento:** Mariano Rasgido

---

## 2. Inicialización del juego

```javascript
function iniciarJuego()
```

Se ejecuta al cargar la página.

Registra los eventos de:

* Selección de personaje.
* Punio.
* Patada.
* Barrida.

Ejemplo:

```javascript
botonPunio.addEventListener('click', ataquePunio)
```

**Colaboraron:** Lautaro Martinez · Samira Baz

---

## 3. Selección del personaje del jugador

```javascript
function seleccionarPersonajeJugador()
```

Su función es:

* Detectar qué personaje eligió el jugador.
* Mostrarlo en pantalla.
* Enviar el nombre del personaje a la función del enemigo.

Ejemplo:

```javascript
spanPersonajeJugador.innerHTML = 'Zuko';
seleccionarPersonajeEnemigo('Zuko');
```

Si no se selecciona ningún personaje:

```javascript
alert('Por favor, selecciona un personaje primero.');
```

**Colaboraron:** Lautaro Martinez · Leandro Orozco
**Documentación y seguimiento:** Mariano Rasgido

---

## 4. Selección automática del enemigo

```javascript
function seleccionarPersonajeEnemigo(personajeJugador)
```

El enemigo es generado aleatoriamente.

Se utiliza un bucle:

```javascript
while (...)
```

para garantizar que nunca sea igual al personaje del jugador.

El resultado se muestra en:

```html
<span id="personaje-enemigo"></span>
```

**Colaboraron:** Leandro Orozco · Samira Baz

---

## 5. Sistema de ataques

Funciones disponibles:

```javascript
ataquePunio()
ataquePatada()
ataqueBarrida()
```

Ejemplo:

```javascript
function ataquePunio(){
    ataqueJugador = 'Punio'
    ataqueAleatorioEnemigo()
}
```

Cada función:

* Guarda el ataque del jugador.
* Genera el ataque enemigo.
* Inicia el combate.

**Colaboraron:** Lautaro Martinez · Gabriel Maculus
**Documentación y seguimiento:** Mariano Rasgido

---

## 6. Ataque aleatorio del enemigo

```javascript
function ataqueAleatorioEnemigo()
```

Genera un número aleatorio entre 1 y 3:

```javascript
aleatorio(1, 3)
```

Correspondencias:

| Número | Ataque  |
| ------ | ------- |
| 1      | Punio   |
| 2      | Patada  |
| 3      | Barrida |

Luego ejecuta:

```javascript
combate()
```

**Colaboraron:** Leandro Orozco · Samira Baz
**Documentación y seguimiento:** Mariano Rasgido

---

## 7. Sistema de combate

```javascript
function combate()
```

Compara ambos ataques para determinar el resultado.

Tabla de ventajas:

| Ataque     | Vence a    |
| ---------- | ---------- |
| Punio 👊   | Barrida 🦶 |
| Patada 🦵  | Punio 👊   |
| Barrida 🦶 | Patada 🦵  |

Si ambos ataques son iguales:

```javascript
EMPATE 🤝
```

En caso contrario:

```javascript
GANASTE 🎉
```

o

```javascript
PERDISTE ❌
```

**Colaboraron:** Lautaro Martinez · Leandro Orozco

---

## 8. Creación dinámica de mensajes

```javascript
function crearMensaje(resultado)
```

Crea un nuevo párrafo mediante:

```javascript
document.createElement('p')
```

y lo agrega a la sección de mensajes usando:

```javascript
appendChild()
```

Ejemplo:

> Tu personaje atacó con Punio, el personaje del enemigo atacó con Patada PERDISTE ❌

**Colaboraron:** Samira Baz · Gabriel Maculus
**Documentación y seguimiento:** Mariano Rasgido

---

## 9. Función reutilizable de números aleatorios

```javascript
function aleatorio(min, max)
```

Permite generar números enteros dentro de un rango.

Ejemplos:

```javascript
aleatorio(1, 4)
```

para personajes.

```javascript
aleatorio(1, 3)
```

para ataques.

**Colaboraron:** Lautaro Martinez

---

## 10. Inicio automático del juego

```javascript
window.addEventListener('load', iniciarJuego);
```

Garantiza que todos los elementos del HTML estén cargados antes de ejecutar la lógica del programa.

**Colaboraron:** Lautaro Martinez · Samira Baz
**Documentación y seguimiento:** Mariano Rasgido

---

## 🧠 Conceptos practicados

Durante esta etapa del proyecto se trabajaron los siguientes conceptos:

* HTML semántico.
* Formularios y radio buttons.
* Manipulación del DOM.
* `document.getElementById()`.
* `innerHTML`.
* Eventos con `addEventListener()`.
* Variables globales.
* Funciones y parámetros.
* Condicionales.
* Bucles `while`.
* Generación de números aleatorios.
* Creación dinámica de elementos.
* `appendChild()`.
* Simulación de combate por turnos.

**Colaboraron:** Todo el equipo.
**Documentación y seguimiento:** Mariano Rasgido

---

## 🚀 ¿Cómo ejecutarlo?

1. Descargá o cloná el proyecto.
2. Abrí `avatar.html` en tu navegador.

O bien:

1. Abrí la carpeta con Visual Studio Code.
2. Instalá la extensión **Live Server**.
3. Ejecutá **Open with Live Server**.

No requiere dependencias externas.

**Colaboraron:** Todo el equipo.
**Documentación y seguimiento:** Mariano Rasgido

---

## 📌 Próximas mejoras

* Implementar contador de vidas.
* Mostrar un ganador final.
* Incorporar reinicio funcional.
* Deshabilitar ataques al finalizar la partida.
* Agregar estilos visuales mediante CSS.
* Incorporar sonidos y animaciones.
* Adaptar el diseño para dispositivos móviles.

**Colaboraron:** Todo el equipo.

---

## 💙 Sobre este proyecto

Este proyecto fue desarrollado como práctica para aprender los fundamentos del desarrollo web con JavaScript.

Además de construir una aplicación funcional, el objetivo fue comprender cómo conectar una interfaz HTML con lógica interactiva, documentar el proceso de aprendizaje y evolucionar progresivamente hacia un juego más completo.

---

## 📝 Documentación del proyecto

La documentación técnica y descriptiva fue realizada por **Mariano Rasgido**, registrando:

* El funcionamiento de cada sección del código.
* Los conceptos utilizados durante el aprendizaje.
* La evolución del proyecto entre versiones.
* La organización del README.
* El seguimiento del proceso de desarrollo como material de consulta futura.

Esta documentación busca explicar no solo qué hace el código, sino también por qué fue construido de esa manera.

---

## 📋 Metodología de trabajo

El proyecto fue desarrollado de manera colaborativa, compartiendo conocimientos, resolviendo problemas en conjunto y documentando cada avance.

Se utilizó como herramienta de aprendizaje para reforzar:

* Trabajo colaborativo.
* Organización del código.
* Resolución de problemas.
* Validación del funcionamiento.
* Documentación técnica.

---

## 👥 Equipo y colaboradores

| Rol                                        | Integrante       | Participación                                                                                                         |
| ------------------------------------------ | ---------------- | --------------------------------------------------------------------------------------------------------------------- |
| Developer                                  | Lautaro Martinez | Desarrollo de funcionalidades y lógica del juego                                                                      |
| Developer                                  | Samira Baz       | Implementación, pruebas y validación de componentes                                                                   |
| Developer                                  | Gabriel Maculus  | Desarrollo y colaboración en la estructura del proyecto                                                               |
| Developer                                  | Leandro Orozco   | Participación en la lógica y validación del funcionamiento                                                            |
| Documentación y seguimiento del desarrollo | Mariano Rasgido  | Documentación del proyecto, registro del proceso de aprendizaje, organización del desarrollo y elaboración del README |

---
