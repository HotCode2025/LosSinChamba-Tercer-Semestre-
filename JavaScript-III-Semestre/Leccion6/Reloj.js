let relog = () => {
    let fecha = new Date();
    let hora = fecha.getHours();
    let minutos = fecha.getMinutes();
    let segundos = fecha.getSeconds();
    console.log(`${hora}:${minutos}:${segundos}`);
};

setInterval(relog, 1000);