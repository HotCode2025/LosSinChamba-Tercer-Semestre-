// Handle Registration
document.getElementById('registerForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const fullName = document.getElementById('registerFullName').value.trim();
    const email = document.getElementById('registerEmail').value.trim();
    const age = document.getElementById('registerAge').value.trim();
    const country = document.getElementById('registerCountry').value.trim();
    const password = document.getElementById('registerPassword').value.trim();
    
    const errorDiv = document.getElementById('registerError');
    const successDiv = document.getElementById('registerSuccess');
    const btn = document.getElementById('registerBtn');
    
    errorDiv.style.display = 'none';
    successDiv.style.display = 'none';
    btn.disabled = true;
    btn.innerText = 'Creando cuenta...';
    
    try {
        const response = await fetch('/api/register', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ fullName, email, password, age, country })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            successDiv.innerText = '¡Registro exitoso! Redirigiendo al login...';
            successDiv.style.display = 'block';
            document.getElementById('registerForm').reset();
            setTimeout(() => {
                window.location.href = 'login.html';
            }, 2000);
        } else {
            errorDiv.innerText = data.error || 'No se pudo crear la cuenta.';
            errorDiv.style.display = 'block';
        }
    } catch (err) {
        errorDiv.innerText = 'No se pudo conectar al servidor. Asegúrate de ejecutar "node server.js".';
        errorDiv.style.display = 'block';
    } finally {
        btn.disabled = false;
        btn.innerText = 'Registrarme';
    }
});
