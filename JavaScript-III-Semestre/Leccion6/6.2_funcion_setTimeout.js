const saludar = (nombre, edad) => {
    console.log(`Hola ${nombre}, tu edad es de ${edad} años.`);
};

setTimeout(saludar, 1000, 'Luis', 20);
/*
setTimeout(() => {
    saludar('Juan', 30);
}, 2000);
*/