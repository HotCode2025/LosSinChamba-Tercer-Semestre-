// Handle Login
document.getElementById('loginForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const email = document.getElementById('loginEmail').value.trim();
    const password = document.getElementById('loginPassword').value.trim();
    const errorDiv = document.getElementById('loginError');
    const btn = document.getElementById('loginBtn');
    
    errorDiv.style.display = 'none';
    btn.disabled = true;
    btn.innerText = 'Cargando...';
    
    try {
        const response = await fetch('/api/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            // Store token and name
            localStorage.setItem('unicampus_token', data.token);
            localStorage.setItem('unicampus_user', data.name);
            
            // Redirect to dashboard
            window.location.href = 'index.html';
        } else {
            errorDiv.innerText = data.error || 'Credenciales incorrectas';
            errorDiv.style.display = 'block';
        }
    } catch (err) {
        errorDiv.innerText = 'No se pudo conectar al servidor. Asegúrate de ejecutar "node server.js".';
        errorDiv.style.display = 'block';
    } finally {
        btn.disabled = false;
        btn.innerText = 'Iniciar Sesión';
    }
});
