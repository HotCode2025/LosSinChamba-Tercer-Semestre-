🐴 El Salto del Caballo — Backtracking

Un proyecto desarrollado con JavaScript, HTML y CSS que resuelve y visualiza el clásico problema del Salto del Caballo, uno de los desafíos más conocidos dentro del campo de los algoritmos y la inteligencia computacional.

El objetivo consiste en encontrar un recorrido válido para una pieza de caballo en un tablero de ajedrez de 8×8, de manera que visite cada una de las 64 casillas exactamente una vez.

Este proyecto presenta dos versiones complementarias:

🖥️ Una versión de consola, centrada en la resolución algorítmica del problema.
🎨 Una versión visual interactiva, que permite observar paso a paso cómo el algoritmo encuentra la solución.

Además de resolver el desafío, el proyecto busca comprender conceptos fundamentales como la recursividad, el Backtracking, la optimización mediante heurísticas y la manipulación dinámica del DOM.

Objetivos del proyecto
Resolver el problema clásico del Salto del Caballo.
Implementar Backtracking mediante recursividad.
Optimizar la búsqueda utilizando la Heurística de Warnsdorff.
Comparar una implementación orientada a consola con una implementación visual.
Comprender cómo representar estructuras complejas mediante matrices.
Visualizar el proceso de toma de decisiones del algoritmo.
Utilizar JavaScript tanto para lógica algorítmica como para interfaces interactivas.
¿Qué es el Salto del Caballo?

El Knight's Tour es un problema matemático y computacional que consiste en determinar una secuencia de movimientos válidos del caballo en un tablero de ajedrez, de modo que:

El caballo visite todas las casillas del tablero exactamente una vez.

El caballo posee un movimiento característico:

Dos casillas en una dirección.
Una casilla en dirección perpendicular.

Desde cualquier posición puede tener hasta 8 movimientos posibles.

Versiones del proyecto
1. Versión Consola

Esta implementación está enfocada exclusivamente en la resolución del problema.

Características:

Calcula una solución completa.
Imprime el tablero resuelto mediante console.log().
Utiliza Backtracking recursivo.
Implementa la Regla de Warnsdorff para optimizar el recorrido.

Ejemplo de salida:

00 | 59 | 38 | ...
37 | 34 | 31 | ...
58 | 01 | 60 | ...
...
2. Versión Visual Interactiva

Representa gráficamente el proceso de resolución.

Características:

Genera un tablero de ajedrez dinámicamente.
Muestra el recorrido paso a paso.
Destaca visualmente la posición actual del caballo.
Permite observar el Backtracking en acción.
Incluye pausas artificiales para apreciar la animación.
Informa el estado del algoritmo al usuario.
Estructura del proyecto
EL SALTO DEL CABALLO/
├── consola/
│   └── caballo.js          → Implementación por consola
├── visual/
│   └── index.html          → Interfaz interactiva
├── README.md               → Documentación del proyecto
Explicación del algoritmo
Backtracking (Vuelta Atrás)

El Backtracking consiste en:

Tomar una decisión.
Avanzar.
Verificar si esa decisión permite continuar.
Si conduce a un callejón sin salida:
deshacer la decisión,
retroceder,
probar otra alternativa.

En este problema:

El caballo prueba un movimiento.
Si eventualmente queda atrapado:
elimina ese movimiento,
vuelve atrás,
intenta otro camino.
Heurística de Warnsdorff

El Backtracking puro puede explorar millones de caminos.

Para acelerar el proceso se utiliza la Regla de Warnsdorff, que establece:

Elegir primero la casilla que tenga la menor cantidad de movimientos futuros disponibles.

Esto reduce enormemente la probabilidad de que el caballo quede atrapado.

Gracias a esta optimización, el algoritmo encuentra soluciones prácticamente de manera instantánea.

Explicación del código (Versión Consola)
1. Tamaño del tablero
const N = 8;

Define un tablero de:

8 filas × 8 columnas

equivalente a un tablero de ajedrez tradicional.

2. Movimientos del caballo
const movX = [2, 1, -1, -2, -2, -1, 1, 2];
const movY = [1, 2, 2, 1, -1, -2, -2, -1];

Representan los ocho movimientos posibles del caballo.

Cada posición de ambos arreglos forma una pareja:

(2,1)
(1,2)
(-1,2)
(-2,1)
(-2,-1)
(-1,-2)
(1,-2)
(2,-1)
3. Validación de movimientos
function esMovimientoValido(x, y, tablero)

Comprueba que:

La posición esté dentro del tablero.
La casilla no haya sido visitada.

Retorna:

true

o

false

según corresponda.

4. Conteo de movimientos futuros
function contarMovimientosPosibles(x, y, tablero)

Cuenta cuántos movimientos válidos existen desde una posición.

Esta función implementa la optimización de Warnsdorff.

5. Backtracking recursivo
function resolverSaltoCaballo(...)

Es el núcleo del algoritmo.

Responsabilidades:

Detectar la condición de éxito.
Generar movimientos candidatos.
Ordenarlos.
Explorar caminos.
Retroceder cuando sea necesario.

Condición de éxito:

if (saltoActual === N * N)

Significa que:

El caballo logró visitar las 64 casillas.

6. Inicialización
function iniciarJuego()

Se encarga de:

Crear el tablero.
Inicializarlo con -1.
Ubicar al caballo en (0,0).
Lanzar la búsqueda.
Mostrar el resultado.
Explicación del código (Versión Visual)

La segunda implementación transforma el algoritmo en una experiencia interactiva.

1. Estructura HTML

El documento contiene:

Contenedor principal
<div class="container">

Agrupa toda la aplicación.

Botón de inicio
<button id="btnIniciar">

Permite comenzar la simulación.

Estado del algoritmo
<div id="status">

Muestra mensajes como:

Listo para comenzar
Calculando el camino óptimo...
¡Completado con éxito!
Tablero visual
<table id="tableroHTML">

Representa el tablero de ajedrez.

Estilos CSS

Se diseñó una interfaz limpia y moderna.

Incluye:

Colores del tablero
.casilla-clara
.casilla-oscura

Imitan un tablero real.

Casillas visitadas
.visitada

Se muestran en color verde.

Posición actual
.actual

Se resalta en naranja para seguir visualmente el movimiento del caballo.

Botones interactivos

Incluyen:

efectos hover,
sombras,
transiciones suaves.
Funciones visuales
Inicialización del tablero
inicializarTableroVisual()

Genera dinámicamente:

filas,
columnas,
celdas HTML.
Actualización de celdas
actualizarCeldaVisual(...)

Permite:

escribir el número del paso,
cambiar colores,
marcar la posición actual.
Pausas artificiales
const pausar = (ms) => ...

Utiliza:

Promise

y

setTimeout()

para ralentizar la ejecución.

Esto permite apreciar el recorrido del caballo.

Async / Await

El algoritmo visual utiliza:

async
await

para mantener la recursividad compatible con las pausas.

Sin estas herramientas, la animación sería instantánea.

Ejecución de la simulación
ejecutarSimulacion()

Orquesta todo el proceso:

deshabilita el botón,
actualiza el estado,
inicia el recorrido,
informa el resultado,
vuelve a habilitar la interfaz.
Conceptos practicados

Durante este proyecto se trabajaron los siguientes conceptos:

Algoritmos clásicos.
Backtracking.
Recursividad.
Heurísticas.
Regla de Warnsdorff.
Matrices bidimensionales.
Validación de movimientos.
Ordenamiento de arreglos.
Manipulación del DOM.
Generación dinámica de elementos HTML.
CSS responsivo.
Eventos.
Programación asíncrona.
Promesas.
Async/Await.
Animaciones mediante temporizadores.
Separación entre lógica e interfaz.
¿Cómo ejecutarlo?
Versión consola
Abrí el archivo JavaScript en Visual Studio Code.
Ejecutalo utilizando Node.js o desde la consola del navegador.
Observá la solución generada.
Versión visual
Abrí el archivo HTML en tu navegador.

o bien:

Abrí el proyecto en Visual Studio Code.
Instalá la extensión Live Server.
Ejecutá Open with Live Server.

No requiere dependencias externas.

Próximas mejoras
Permitir elegir la posición inicial del caballo.
Modificar la velocidad de la animación.
Incorporar controles de pausa y reanudación.
Mostrar estadísticas del algoritmo.
Comparar Backtracking puro contra Warnsdorff.
Visualizar los pasos descartados.
Adaptar la interfaz para dispositivos móviles.
Permitir tableros de diferentes tamaños.
Sobre este proyecto

Este proyecto fue desarrollado con fines educativos para comprender cómo un problema clásico puede resolverse mediante técnicas algorítmicas avanzadas y, posteriormente, transformarse en una experiencia visual accesible para cualquier usuario.

Más allá de obtener una solución correcta, el objetivo fue entender el razonamiento detrás del algoritmo y visualizar cómo toma decisiones durante su ejecución.

📝 Documentación del proyecto

La documentación técnica y descriptiva del desarrollo fue realizada por Mariano Rasgido, registrando:

El funcionamiento de cada componente.
La explicación de conceptos teóricos.
La evolución desde la versión consola hacia la visual.
La organización del README.
El proceso de aprendizaje y experimentación.

Esta documentación busca que cualquier persona pueda comprender no solamente qué hace el algoritmo, sino también por qué funciona y cómo fue construido.

📋 Metodología de trabajo

El proyecto fue desarrollado como una herramienta práctica de aprendizaje, documentando cada etapa del proceso y priorizando la comprensión profunda de los conceptos involucrados.

Además de implementar una solución eficiente, se buscó:

analizar alternativas,
optimizar el rendimiento,
visualizar el comportamiento del algoritmo,
registrar la evolución del desarrollo.
