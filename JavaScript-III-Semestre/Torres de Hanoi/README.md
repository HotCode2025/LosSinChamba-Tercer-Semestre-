Torres de Hanoi — Recursividad en JavaScript

Un proyecto desarrollado con JavaScript para resolver el clásico problema de las Torres de Hanoi, uno de los ejercicios más representativos para comprender el funcionamiento de la recursividad en programación.

A través de una solución elegante y eficiente, el algoritmo muestra paso a paso cómo trasladar una torre de discos desde una varilla de origen hasta una varilla de destino, respetando las reglas del problema.

Este proyecto tiene como objetivo no solo obtener la solución correcta, sino también comprender el razonamiento lógico detrás de la recursividad y cómo un problema complejo puede descomponerse en subproblemas más pequeños.

🎯 Objetivos del proyecto
Comprender el concepto de recursividad.
Aplicar el uso de casos base y llamadas recursivas.
Resolver el problema clásico de las Torres de Hanoi.
Analizar cómo un algoritmo divide un problema complejo en tareas simples.
Visualizar el orden exacto de los movimientos necesarios.
Fortalecer el pensamiento lógico y algorítmico.
¿Qué son las Torres de Hanoi?

Las Torres de Hanoi son un rompecabezas matemático inventado por el matemático francés Édouard Lucas en 1883.

El desafío consiste en mover una pila de discos desde una varilla inicial hasta una varilla final utilizando una tercera varilla auxiliar.

El problema está compuesto por:
Tres varillas.
Una cantidad determinada de discos de distintos tamaños.
Todos los discos comienzan apilados en orden descendente.

Por ejemplo:

Varilla A       Varilla B       Varilla C

   ===
  =====
 =======
📋 Reglas del juego

Para resolver correctamente el problema deben respetarse tres reglas fundamentales:

1. Solo puede moverse un disco a la vez.
✔ Permitido
Mover únicamente el disco superior.
2. Solo puede moverse el disco que se encuentra arriba de una pila.
✔ Permitido

===

=====
No permitido

=====
===
3. Nunca puede colocarse un disco grande sobre uno más pequeño.
✔ Correcto

===
=====
=======
 Incorrecto

=======
===
=====
🧠 ¿Por qué este problema es importante?

Las Torres de Hanoi son uno de los ejemplos más utilizados para enseñar:

Recursividad.
División de problemas.
Pensamiento computacional.
Algoritmos matemáticos.
Complejidad algorítmica.

Su belleza radica en que una solución aparentemente compleja puede expresarse mediante unas pocas líneas de código.

 Estructura del proyecto
TORRES DE HANOI/
├── hanoi.js      → Implementación del algoritmo recursivo
└── README.md     → Documentación del proyecto
📄 Explicación del código
Función principal
function resolverTorresDeHanoi(
    n,
    origen,
    destino,
    auxiliar
)

Es la función encargada de resolver completamente el problema.

Recibe cuatro parámetros:

Parámetro	Descripción
n	Cantidad de discos a mover
origen	Varilla donde comienzan los discos
destino	Varilla donde deben terminar
auxiliar	Varilla utilizada como apoyo
🔹 Caso base

Toda función recursiva necesita una condición que detenga las llamadas infinitas.

En este caso:

if (n === 1) {
    console.log(
        `Mover disco 1 de la varilla ${origen} a la varilla ${destino}`
    );
    return;
}

Significa:

Si solo queda un disco, simplemente se mueve directamente al destino.

Este es el punto donde la recursividad deja de profundizar.

🔹 Paso 1: Liberar el disco más grande
resolverTorresDeHanoi(
    n - 1,
    origen,
    auxiliar,
    destino
);

Antes de mover el disco más grande, debemos quitar todos los discos que tiene encima.

Por eso:

Los n−1 discos superiores se trasladan a la varilla auxiliar.
La varilla destino se utiliza temporalmente como apoyo.
🔹 Paso 2: Mover el disco principal
console.log(
    `Mover disco ${n} de la varilla ${origen} a la varilla ${destino}`
);

Una vez despejado el camino:

El disco más grande puede moverse directamente hacia su destino final.

🔹 Paso 3: Reubicar los discos restantes
resolverTorresDeHanoi(
    n - 1,
    auxiliar,
    destino,
    origen
);

Finalmente:

Los discos almacenados en la varilla auxiliar se trasladan al destino.
La varilla origen pasa a funcionar como apoyo.
 ¿Cómo funciona la recursividad?

Supongamos:

resolverTorresDeHanoi(3, 'A', 'C', 'B');

El algoritmo piensa así:

Quiero mover 3 discos:
Mover 2 discos de A hacia B.
Mover disco 3 de A hacia C.
Mover 2 discos de B hacia C.

Pero mover 2 discos implica nuevamente:

Mover 1 disco.
Mover el disco grande.
Mover el disco restante.

La función continúa descomponiendo el problema hasta llegar al caso base.

 Ejemplo de ejecución

Con:

const cantidadDeDiscos = 3;

resolverTorresDeHanoi(
    cantidadDeDiscos,
    'A',
    'C',
    'B'
);

La salida será:

--- Iniciando Torres de Hanoi con 3 discos ---

Mover disco 1 de la varilla A a la varilla C
Mover disco 2 de la varilla A a la varilla B
Mover disco 1 de la varilla C a la varilla B
Mover disco 3 de la varilla A a la varilla C
Mover disco 1 de la varilla B a la varilla A
Mover disco 2 de la varilla B a la varilla C
Mover disco 1 de la varilla A a la varilla C
📐 Cantidad mínima de movimientos

Existe una fórmula matemática que determina el número mínimo de movimientos necesarios.

M=2
n
−1

Donde:

M = movimientos mínimos.
n = cantidad de discos.

Por ejemplo:

Discos	Movimientos mínimos
1	1
2	3
3	7
4	15
5	31
6	63
10	1023

Cada disco adicional duplica la cantidad de movimientos y suma uno más.

🧠 Conceptos practicados

Durante este proyecto se trabajaron los siguientes temas:

Recursividad.
Casos base.
Llamadas recursivas.
División de problemas.
Pensamiento algorítmico.
Parámetros de funciones.
Interpolación de cadenas (Template Literals).
Salida por consola.
Complejidad exponencial.
Resolución de problemas clásicos.
🚀 ¿Cómo ejecutarlo?
Utilizando Node.js
Guardá el archivo como hanoi.js.
Abrí una terminal.
Ejecutá:
node hanoi.js
Desde Visual Studio Code
Abrí el proyecto.
Instalá la extensión Code Runner (opcional).
Ejecutá el archivo JavaScript.
Desde la consola del navegador
Abrí las herramientas de desarrollador (F12).
Pegá el código.
Presioná Enter.
Observá los movimientos generados.
📌 Próximas mejoras

Algunas mejoras que podrían incorporarse en futuras versiones:

Visualización gráfica de las torres.
Animación automática del movimiento de los discos.
Selección dinámica de cantidad de discos.
Control de velocidad de la simulación.
Estadísticas de ejecución.
Comparación entre soluciones iterativas y recursivas.
Exportación del historial de movimientos.
 Sobre este proyecto

Este proyecto fue desarrollado como práctica para comprender uno de los conceptos más importantes de la programación: la recursividad.

Las Torres de Hanoi demuestran cómo un problema aparentemente complejo puede resolverse mediante una estrategia elegante basada en dividir la tarea en problemas más pequeños hasta alcanzar una solución simple.

Más allá de mover discos entre varillas, este ejercicio representa una forma de aprender a pensar como lo hacen muchos algoritmos: resolviendo primero aquello que parece imposible al transformarlo en algo manejable.

📝 Documentación del proyecto

La documentación técnica y descriptiva del desarrollo fue realizada por Mariano Rasgido, registrando:

El funcionamiento de cada parte del algoritmo.
La explicación de los conceptos teóricos involucrados.
El proceso de razonamiento recursivo.
La organización del README.
La evolución del aprendizaje durante el desarrollo del proyecto.

Esta documentación busca que cualquier persona pueda comprender no solamente qué hace el código, sino también por qué funciona y cuál es la lógica detrás de cada decisión tomada por el algoritmo.

📋 Metodología de trabajo

El proyecto fue desarrollado con un enfoque práctico y educativo, priorizando la comprensión profunda de la recursividad mediante la implementación de un problema clásico de la informática.

Además de construir una solución funcional, el objetivo fue:

comprender el razonamiento paso a paso,
fortalecer el pensamiento lógico,
documentar el proceso de aprendizaje,
registrar la evolución del desarrollo como material de consulta futura.
