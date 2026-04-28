'use strict';

// ── 4.1 try / catch / finally ──────────────────────────
try {
    let x = 10;
    miFuncion();
}
catch (error) {
    console.log(error);
}
finally {
    console.log('Termina la revisión de errores');
}

// ── 4.2 throw con números ───────────────────────────────

// Caso 1: no es número
let resultado = 'hola';

try {
    if (isNaN(resultado))       throw 'No es un número';
    else if (resultado >= 0)    throw 'Valor positivo';
    else if (resultado <= 0)    throw 'Valor negativo';
}
catch (error) {
    console.log(error);         // 'No es un número'
    console.log(error.name);    // undefined
    console.log(error.message); // undefined
}
finally {
    console.log('Termina la revisión de errores 2');
}

// Caso 2: número positivo
resultado = 10;

try {
    if (isNaN(resultado))       throw 'No es un número';
    else if (resultado >= 0)    throw 'Valor positivo';
    else if (resultado <= 0)    throw 'Valor negativo';
}
catch (error) {
    console.log(error);         // 'Valor positivo'
}

// Caso 3: número negativo
resultado = -5;

try {
    if (isNaN(resultado))       throw 'No es un número';
    else if (resultado >= 0)    throw 'Valor positivo';
    else if (resultado <= 0)    throw 'Valor negativo';
}
catch (error) {
    console.log(error);         // 'Valor negativo'
}