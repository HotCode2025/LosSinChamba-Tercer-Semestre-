# Repaso

## Pag. 5: Conceptos tecnicos

 * 1 - Distribuida: b) Base de datos cuyos archivos estan dispersos en diferentes servidores o redes.
 * 2 - Booleano: a) Tipo de dato que solo acepta valores veradero o falso.
 * 3 - DBMS: c) Software para gestionar, modificar y extraer informacion.
 * 4 - Cadena: d) Conjunto de caracteres dispuestos de forma consecutiva entre comillas
 
## Pag. 11: Inicios de la Web

Pregunta 1:  
>Quién propuso formalmente el lenguaje HTML en el CERN?

HTML fue propuesto al CERN en 1989 por Tim Berners-Lee 
como parte de la propuesta "Information Management: A proposal"
 que tenia como objetivo facilitar el compartir informacion 
 dentro del CERN.
Esta propuesta incluia tambien el protocolo HTTP y el concepto
 de word wide web, hoy dia el fundamento del internet y las 
 arquitecturas cliente servidor distribuidas. 

Pregunta 2:  
>Cuál es el propósito principal de CSS en el desarrollo web?

CSS son las siglas en ingles de "hojas de estilo en cascada"
 (Cascading Style Sheets). Su proposito principal es controlar
 la apariencia y diseño visual de un documento HTML
 (aunque existen otros formatos que lo soportan total o parcialmente). 
Entre sus capacidades estan el control de: colores, layout (posición, padding, margenes),
tipografias, adaptacion de la pagina a distintas pantallas, animaciones y transisiones.
 Una de sus mayores ventaja es que separa la presentacion del contendio lo que lo hace 
mas reutilizable y mantenible que los estilos inline que se usaban antes de la creación
 de CSS.
 

Pregunta 3:  
>Qué arquitectura permite la comunicación entre el navegador y el almacenamiento de
datos?

A esa arquitectura se la conoce como Cliente-Servidor donde el Cliente es el navegador
que muestra Contenido + Presentación y se comunica con el Servidor mediante Requests (pedidos).
Es el Servidor luego el encargado de procesar dicha Request y, en caso de que sea necesario para
satisfacer la consulta, consulta a la Base de Datos para obtener la información que nesecite. 
Luego de terminar de procesar la Request el Servidor devuelve una Response (respuesta) al Cliente.

## Pag. 17: Persistencia

Pregunta:
>Si una red social permite guardar tus fotos para verlas mañana, ¿qué tecnología es la
responsable principal de que esa información no se pierda? 

Respuesta: 2) Base de Datos  
Aclaracion: Aunque es posible guardar las imagenes, multimedia y otros objetos binarios grandes
(BLOB) en la BD por lo general no se almacenan directamente como un campo en un registro de una 
tabla si no como una URI que apunta al archivo y el archivo en si se guarda en el servidor o en 
un almacenamiento externo (servidor especifico,CDN, bucket S3, etc.).

## Pag. 18: El futuro de los datos en Argentina

Pregunta:
>¿Cómo impacta la gestión de grandes
bases de datos en servicios locales
como Mercado Libre o el sistema de
salud pública?

Respuesta: 
La gestion de bases de datos es critica para estas organizaciones, no solo nivel de gestion 
de usuarios e inventarios si no tambien a nivel de planeamiento, toma de decisiones y 
soporte de operaciones. Por ejemplo en el caso de Mercado Libre la optimizacion de 
recomendaciones y del armado de pedidos es crucial para mantener la competitividad
de la compañia y nada de eso es posible sin la correcta organizacion de grandes
 volumenes de datos.
 
## Pag. 21: Vocabulario de HTML y estructura

* 1 - Alt Text: c) Atributo esencial para accesibilidad en imágenes.
* 2 - \<HEADER>: b) Contiene logotipos y navegación inicial del sitio.
* 3 - DOCTYPE: a) Declaración que indica la versión de HTML al
navegador. 
* 4 - \<BODY>: d) Sección que alberga todo el contenido visible por el
usuario. 