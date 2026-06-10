// --- Authentication Check ---
const token = localStorage.getItem('unicampus_token');
// Only protect the main pages, skip login page
if (!token && !window.location.href.includes('login.html')) {
    window.location.href = 'login.html';
}

function logout() {
    localStorage.removeItem('unicampus_token');
    localStorage.removeItem('unicampus_user');
    window.location.href = 'login.html';
}

document.addEventListener('DOMContentLoaded', () => {
    const username = localStorage.getItem('unicampus_user');
    if (username) {
        const usernameDisplay = document.getElementById('displayUsername');
        if (usernameDisplay) usernameDisplay.innerText = username;
    }
});

// --- Navigation Logic ---
const navBtns = document.querySelectorAll('.nav-btn');
const views = document.querySelectorAll('.view-section');

navBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        navBtns.forEach(b => b.classList.remove('active'));
        views.forEach(v => v.classList.remove('active'));
        
        btn.classList.add('active');
        const targetId = btn.getAttribute('data-target');
        if(targetId) {
            document.getElementById(targetId).classList.add('active');
        }
    });
});

// --- Classwork Logic ---
function addTask() {
    const input = document.getElementById('taskInput');
    if (input.value.trim() === '') return;

    const taskList = document.getElementById('taskList');
    const div = document.createElement('div');
    div.className = 'task-item';
    div.innerHTML = `
        <label class="custom-checkbox">
            <input type="checkbox">
            <span class="checkmark"></span>
            <span class="task-text">${input.value}</span>
        </label>
        <span class="badge" style="background: var(--primary);">Nuevo</span>
    `;
    
    div.style.animation = 'slideUp 0.3s';
    taskList.insertBefore(div, taskList.firstChild);
    input.value = '';
}

// --- Grade Calculator ---
let gradeCount = 2;

function addGradeInput() {
    gradeCount++;
    const container = document.getElementById('gradesContainer');
    const newGroup = document.createElement('div');
    newGroup.className = 'input-group grade-entry';
    
    newGroup.innerHTML = `
        <label>Nota ${gradeCount}</label>
        <div class="grade-input-wrapper">
            <i class="ph ph-exam"></i>
            <input type="number" class="grade-val" placeholder="1-10" min="1" max="10">
        </div>
    `;
    container.appendChild(newGroup);
}

function calculateGrades() {
    const inputs = document.querySelectorAll('.grade-val');
    const courseSelect = document.getElementById('courseSelect');
    const resultBox = document.getElementById('gradeResult');
    const scoreDisplay = document.getElementById('scoreDisplay');
    const statusDisplay = document.getElementById('statusDisplay');
    const subjectResultName = document.getElementById('subjectResultName');
    
    let sum = 0;
    let validCount = 0;

    inputs.forEach(input => {
        const val = parseFloat(input.value);
        if (!isNaN(val)) {
            sum += val;
            validCount++;
        }
    });

    if (validCount === 0) {
        alert("Por favor ingresa al menos una nota válida.");
        return;
    }

    const average = sum / validCount;
    scoreDisplay.innerText = average.toFixed(1);

    if (courseSelect) {
        subjectResultName.innerText = courseSelect.value;
    }

    if (average >= 8) {
        statusDisplay.innerText = "PROMOCIONADO 🏆";
        statusDisplay.style.color = "var(--accent-2)";
        document.querySelector('.score-circle').style.borderColor = "var(--accent-2)";
    } else if (average >= 6) {
        statusDisplay.innerText = "REGULAR ✅";
        statusDisplay.style.color = "var(--accent-1)";
        document.querySelector('.score-circle').style.borderColor = "var(--accent-1)";
    } else {
        statusDisplay.innerText = "REPROBADO ❌";
        statusDisplay.style.color = "var(--accent-4)";
        document.querySelector('.score-circle').style.borderColor = "var(--accent-4)";
    }

    resultBox.classList.remove('hidden');
}

// --- Pomodoro Timer Logic ---
let timer;
let timeLeft = 1500; // 25 minutes in seconds
let isRunning = false;

function updateTimeDisplay() {
    const minutes = Math.floor(timeLeft / 60);
    const seconds = timeLeft % 60;
    document.getElementById('timeDisplay').innerText = 
        `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
}

function startTimer() {
    if (isRunning) return;
    isRunning = true;
    document.getElementById('startTimerBtn').innerHTML = '<i class="ph-fill ph-pause-circle"></i> En curso...';
    
    timer = setInterval(() => {
        if (timeLeft > 0) {
            timeLeft--;
            updateTimeDisplay();
        } else {
            clearInterval(timer);
            isRunning = false;
            alert("¡Tiempo cumplido! Gran sesión de enfoque. Tómate un descanso.");
            document.getElementById('startTimerBtn').innerHTML = '<i class="ph-fill ph-play-circle"></i> Iniciar Enfoque';
        }
    }, 1000);
}

function resetTimer() {
    clearInterval(timer);
    isRunning = false;
    timeLeft = 1500;
    updateTimeDisplay();
    document.getElementById('startTimerBtn').innerHTML = '<i class="ph-fill ph-play-circle"></i> Iniciar Enfoque';
}

// --- Account Management Logic ---
async function deleteAccount() {
    const confirmMsg = "¿Estás seguro de que deseas eliminar tu cuenta? Esta acción no se puede deshacer.";
    
    if (confirm(confirmMsg)) {
        try {
            const token = localStorage.getItem('unicampus_token');
            const response = await fetch('/api/user', {
                method: 'DELETE',
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });
            
            if (response.ok) {
                alert("Cuenta eliminada exitosamente.");
                logout();
            } else {
                const data = await response.json();
                alert("Error al eliminar la cuenta: " + (data.error || 'Error desconocido'));
            }
        } catch (error) {
            console.error('Delete account error:', error);
            alert("Error de conexión.");
        }
    }
}