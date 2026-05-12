let relog = () => {
    let fecha = new Date();
    
    
    const formatoDosDigitos = (num) => num.toString().padStart(2, '0');

    let hora = formatoDosDigitos(fecha.getHours());
    let minutos = formatoDosDigitos(fecha.getMinutes());
    let segundos = formatoDosDigitos(fecha.getSeconds());

    
    document.getElementById('reloj').textContent = `${hora}:${minutos}:${segundos}`;
};


relog();

// Iniciamos el intervalo
setInterval(relog, 1000);