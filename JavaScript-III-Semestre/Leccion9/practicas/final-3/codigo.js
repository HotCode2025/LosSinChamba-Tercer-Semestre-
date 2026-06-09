document.addEventListener("DOMContentLoaded", () => {
    // Capturamos el formulario por su ID
    const loginForm = document.getElementById("loginForm");

    // Escuchamos el evento 'submit' (cuando se presiona el botón Login)
    loginForm.addEventListener("submit", (event) => {
        // Evitamos que la página se recargue por defecto
        event.preventDefault(); 

        // Obtenemos los valores de los inputs
        const username = document.getElementById("username").value;
        const password = document.getElementById("password").value;

        // Validamos que los campos no estén vacíos
        if (username.trim() === "" || password.trim() === "") {
            alert("Por favor, ingresa tu usuario y contraseña.");
        } else {
            // Simulamos el inicio de sesión exitoso
            alert(`¡Bienvenido, ${username}! Has iniciado sesión correctamente.`);
            
            // Limpiamos los campos del formulario
            loginForm.reset(); 
        }
    });
});