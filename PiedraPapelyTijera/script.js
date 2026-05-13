/* ═══════════════════════════════════════════════════════════
   script.js — PIEDRA · PAPEL · TIJERA : Mortal Edition
   Lógica de juego, sistema de turnos, resolución de combate
   y disparo de animaciones de daño
═══════════════════════════════════════════════════════════ */

/* ─────────────────────────────────────────
   1. PARTÍCULAS DE BRASA (Embers)
      Genera brasas animadas con CSS variables
      usando Object.assign para estilos dinámicos
───────────────────────────────────────── */
(function spawnEmbers() {
  const container = document.getElementById('embers');
  const EMBER_COUNT = 35;
  const COLORS = ['#ff4500', '#ff6a00', '#ff8c00', '#ffd700', '#ff2200'];

  for (let i = 0; i < EMBER_COUNT; i++) {
    const ember = document.createElement('div');
    ember.className = 'ember';

    const size     = Math.random() * 4 + 1.5;
    const left     = Math.random() * 100;
    const duration = Math.random() * 8 + 6;
    const delay    = Math.random() * 10;
    const dx       = (Math.random() - 0.5) * 120;
    const color    = COLORS[Math.floor(Math.random() * COLORS.length)];

    /* Object.assign para aplicar todos los estilos dinámicos de una vez */
    Object.assign(ember.style, {
      width:             `${size}px`,
      height:            `${size}px`,
      left:              `${left}%`,
      background:        color,
      boxShadow:         `0 0 ${size * 2}px ${color}`,
      '--dx':            `${dx}px`,
      animationDuration: `${duration}s`,
      animationDelay:    `${delay}s`,
    });

    container.appendChild(ember);
  }
})();


/* ─────────────────────────────────────────
   2. DEFINICIÓN DE ARMAS
      Cada arma tiene emoji, nombre y a quién vence
───────────────────────────────────────── */
const CHOICES = {
  piedra: { emoji: '🪨', name: 'Piedra', beats: 'tijera' },
  papel:  { emoji: '✋', name: 'Papel',  beats: 'piedra' },
  tijera: { emoji: '✂️', name: 'Tijera', beats: 'papel'  },
};

/* Mensajes de victoria según combinación ganadora */
const COMBAT_LINES = {
  piedra_tijera: '🪨 Piedra aplasta Tijera',
  papel_piedra:  '✋ Papel envuelve Piedra',
  tijera_papel:  '✂️ Tijera corta Papel',
};


/* ─────────────────────────────────────────
   3. ESTADO DEL JUEGO
      MAX_HP = 4 (cada derrota quita 1; llegar a 0 = fin)
───────────────────────────────────────── */
const MAX_HP = 4;

const state = {
  hp:       { p1: MAX_HP, p2: MAX_HP },
  round:    1,
  /* Fases: 'p1-choose' → 'waiting' → 'p2-choose' → 'resolving' */
  phase:    'p1-choose',
  p1Choice: null,
  p2Choice: null,
  history:  [],   // array de 'p1' | 'p2' | 'draw' por ronda
};


/* ─────────────────────────────────────────
   4. REFERENCIAS AL DOM
───────────────────────────────────────── */
const $ = id => document.getElementById(id);

const hpBar      = { p1: $('hp-bar-p1'),  p2: $('hp-bar-p2')  };
const hpWrap     = { p1: $('hp-wrap-p1'), p2: $('hp-wrap-p2') };
const avatar     = { p1: $('avatar-p1'),  p2: $('avatar-p2')  };
const choiceLbl  = { p1: $('label-p1'),   p2: $('label-p2')   };

const announceEl  = $('announce');
const turnLabel   = $('turn-label');
const choicesRow  = $('choices-row');
const waitingScr  = $('waiting-screen');
const confirmBtn  = $('confirm-btn');
const resultFlash = $('result-flash');
const roundNum    = $('round-number');
const roundPips   = $('round-pips');
const combatLog   = $('combat-log');
const historyBox  = $('history');
const gameoverDiv = $('gameover');
const gameoverWin = $('gameover-winner');
const rematchBtn  = $('rematch-btn');


/* ─────────────────────────────────────────
   5. ACTUALIZAR BARRAS DE VIDA
───────────────────────────────────────── */
function updateHPBars() {
  ['p1', 'p2'].forEach(p => {
    const pct = (state.hp[p] / MAX_HP) * 100;
    const bar = hpBar[p];
    bar.style.width = `${pct}%`;

    /* Cambio de color según HP restante */
    bar.className = 'hp-bar';
    if      (pct > 60) bar.classList.add('full');
    else if (pct > 30) bar.classList.add('medium');
    else               bar.classList.add('low');
  });
}


/* ─────────────────────────────────────────
   6. ACTUALIZAR PIPS DE RONDAS (HUD central)
───────────────────────────────────────── */
function updatePips() {
  roundPips.innerHTML = '';
  for (let i = 0; i < MAX_HP; i++) {
    const pip = document.createElement('div');
    pip.className = 'pip';
    const entry = state.history[i];
    if      (entry === 'p1') pip.classList.add('p1-win');
    else if (entry === 'p2') pip.classList.add('p2-win');
    roundPips.appendChild(pip);
  }
}


/* ─────────────────────────────────────────
   7. ACTUALIZAR AVATAR DE LUCHADOR
      hidden=true → muestra "?"
      hidden=false → muestra emoji + animación
───────────────────────────────────────── */
function setAvatar(player, choiceKey, hidden = false) {
  const av = avatar[player];

  if (hidden) {
    av.innerHTML = `<span class="hidden-choice">?</span>`;
    choiceLbl[player].textContent = '—';
    av.classList.remove('reveal');
    return;
  }

  const c = CHOICES[choiceKey];
  av.innerHTML = `<span class="choice-emoji">${c.emoji}</span>`;
  choiceLbl[player].textContent = c.name;

  /* Dispara animación de revelación con reflow forzado */
  av.classList.remove('reveal');
  void av.offsetWidth;
  av.classList.add('reveal');
}


/* ─────────────────────────────────────────
   8. ACTUALIZAR BANNER DE ANUNCIO
───────────────────────────────────────── */
function setAnnounce(text, color = '') {
  announceEl.textContent  = text;
  announceEl.style.color  = color || 'var(--gold)';
  announceEl.style.textShadow = color
    ? `0 0 10px ${color}, 0 0 25px ${color}66`
    : '0 0 10px var(--gold), 0 0 25px var(--fire-1)';
}


/* ─────────────────────────────────────────
   9. SCREEN SHAKE
      Añade clase CSS 'shake' en <body> y la quita
───────────────────────────────────────── */
function shakeScreen() {
  document.body.classList.remove('shake');
  void document.body.offsetWidth;   // reflow para reiniciar la animación
  document.body.classList.add('shake');
  setTimeout(() => document.body.classList.remove('shake'), 550);
}


/* ─────────────────────────────────────────
   10. FLASH DE DAÑO EN BARRA DE HP
───────────────────────────────────────── */
function triggerDamageFlash(player) {
  const wrap = hpWrap[player];
  wrap.classList.remove('damaged');
  void wrap.offsetWidth;
  wrap.classList.add('damaged');
  setTimeout(() => wrap.classList.remove('damaged'), 600);
}


/* ─────────────────────────────────────────
   11. AÑADIR ENTRADA AL HISTORIAL VISUAL
───────────────────────────────────────── */
function addHistoryEntry(winner, p1c, p2c) {
  const entry = document.createElement('div');
  const c1 = CHOICES[p1c], c2 = CHOICES[p2c];

  let cssClass = 'draw-h';
  let text     = `R${state.round} ${c1.emoji} ═ ${c2.emoji}`;

  if (winner === 'p1') { cssClass = 'p1w'; text = `R${state.round} ${c1.emoji} ▶ ${c2.emoji}`; }
  if (winner === 'p2') { cssClass = 'p2w'; text = `R${state.round} ${c1.emoji} ◀ ${c2.emoji}`; }

  entry.className   = `history-entry ${cssClass}`;
  entry.textContent = text;
  historyBox.appendChild(entry);
}


/* ─────────────────────────────────────────
   12. FLASH DE RESULTADO DE RONDA
───────────────────────────────────────── */
function showResultFlash(text, cssClass) {
  resultFlash.textContent = text;
  resultFlash.className   = `show ${cssClass}`;
  setTimeout(() => {
    resultFlash.className   = '';
    resultFlash.textContent = '';
  }, 1800);
}


/* ─────────────────────────────────────────
   13. RESOLVER COMBATE  ← función principal
      Compara las elecciones, aplica daño,
      dispara animaciones y avanza la ronda
───────────────────────────────────────── */
function resolveCombat() {
  state.phase = 'resolving';
  const p1c = state.p1Choice;
  const p2c = state.p2Choice;

  /* Revelar ambas elecciones simultáneamente */
  setAvatar('p1', p1c);
  setAvatar('p2', p2c);

  let winner = null;

  if (p1c === p2c) {
    /* ── EMPATE ── */
    winner = 'draw';
    showResultFlash('⚔ EMPATE ⚔', 'draw');
    setAnnounce('¡Fuerzas iguales! ¡Nadie cae!', 'var(--gold)');
    combatLog.textContent = `${CHOICES[p1c].name} vs ${CHOICES[p2c].name} — Equilibrio perfecto`;
    shakeScreen();

  } else if (CHOICES[p1c].beats === p2c) {
    /* ── PLAYER 1 GANA ── */
    winner = 'p1';
    state.hp.p2 = Math.max(0, state.hp.p2 - 1);
    showResultFlash('⚡ Player 1 — VICTORIA', 'win-p1');
    setAnnounce('¡Player 1 destruye a Player 2!', 'var(--p1-color)');
    combatLog.textContent = COMBAT_LINES[`${p1c}_${p2c}`] || `${CHOICES[p1c].name} vence`;
    shakeScreen();
    setTimeout(() => triggerDamageFlash('p2'), 150);

  } else {
    /* ── PLAYER 2 GANA ── */
    winner = 'p2';
    state.hp.p1 = Math.max(0, state.hp.p1 - 1);
    showResultFlash('🩸 Player 2 — VICTORIA', 'win-p2');
    setAnnounce('¡Player 2 aplasta a Player 1!', 'var(--p2-color)');
    combatLog.textContent = COMBAT_LINES[`${p2c}_${p1c}`] || `${CHOICES[p2c].name} vence`;
    shakeScreen();
    setTimeout(() => triggerDamageFlash('p1'), 150);
  }

  /* Registrar resultado en historial */
  if (winner !== 'draw') state.history.push(winner);
  addHistoryEntry(winner, p1c, p2c);

  updateHPBars();
  updatePips();

  /* Esperar antes de pasar a la siguiente ronda o mostrar Game Over */
  setTimeout(() => {
    if (state.hp.p1 <= 0 || state.hp.p2 <= 0) {
      showGameOver();
    } else {
      nextRound();
    }
  }, 2000);
}


/* ─────────────────────────────────────────
   14. SIGUIENTE RONDA
───────────────────────────────────────── */
function nextRound() {
  state.round++;
  state.p1Choice = null;
  state.p2Choice = null;
  state.phase    = 'p1-choose';
  roundNum.textContent = state.round;
  setAnnounce('⚔ Elige tu arma ⚔');
  setAvatar('p1', null, true);
  setAvatar('p2', null, true);
  showChoicesFor('p1');
}


/* ─────────────────────────────────────────
   15. MOSTRAR PANEL DE ELECCIÓN
      Alterna etiqueta y colores según el jugador en turno
───────────────────────────────────────── */
function showChoicesFor(player) {
  choicesRow.style.display = 'flex';
  waitingScr.classList.remove('show');

  if (player === 'p1') {
    turnLabel.textContent = '⚡ Player 1 — Elige tu destino ⚡';
    turnLabel.className   = 'player-turn-label p1-turn';
    setAnnounce('Player 1 — ¡Elige!', 'var(--p1-color)');
  } else {
    turnLabel.textContent = '🩸 Player 2 — Elige tu destino 🩸';
    turnLabel.className   = 'player-turn-label p2-turn';
    setAnnounce('Player 2 — ¡Elige!', 'var(--p2-color)');
  }
}


/* ─────────────────────────────────────────
   16. GAME OVER — Muestra overlay final
───────────────────────────────────────── */
function showGameOver() {
  const winner    = state.hp.p1 <= 0 ? 'p2' : 'p1';
  const winnerLbl = winner === 'p1' ? 'Player 1' : 'Player 2';

  gameoverWin.textContent = `${winnerLbl} WINS`;
  gameoverWin.className   = `${winner}-wins`;
  gameoverDiv.classList.add('show');
}


/* ─────────────────────────────────────────
   17. LISTENERS DE BOTONES DE ARMA
      Captura el clic, registra la elección
      y maneja la transición de fase
───────────────────────────────────────── */
document.querySelectorAll('.rune-btn').forEach(btn => {
  btn.addEventListener('click', function () {
    if (state.phase === 'resolving') return;   // bloquear durante resolución

    const choice = this.dataset.choice;        // 'piedra' | 'papel' | 'tijera'

    if (state.phase === 'p1-choose') {
      /* Player 1 elige */
      state.p1Choice = choice;
      state.phase    = 'waiting';

      /* Ocultar botones y mostrar pantalla de espera */
      choicesRow.style.display = 'none';
      waitingScr.classList.add('show');

      /* Mostrar brevemente la elección de P1 (0.4s) y luego ocultarla */
      setAvatar('p1', choice);
      setTimeout(() => setAvatar('p1', null, true), 400);

      setAnnounce('Pasa el dispositivo a Player 2', 'var(--gold)');
      combatLog.textContent = 'Player 1 ha elegido. ¡Que el destino decida!';

    } else if (state.phase === 'p2-choose') {
      /* Player 2 elige */
      state.p2Choice = choice;
      setAvatar('p2', choice);
      /* Pequeña pausa visual antes de resolver */
      setTimeout(() => resolveCombat(), 300);
    }
  });
});


/* ─────────────────────────────────────────
   18. BOTÓN "PLAYER 2 — LISTO"
      Confirma que P1 ya pasó el dispositivo
      y activa el turno de P2
───────────────────────────────────────── */
confirmBtn.addEventListener('click', function () {
  state.phase = 'p2-choose';
  waitingScr.classList.remove('show');
  setAvatar('p1', null, true);
  setAvatar('p2', null, true);
  showChoicesFor('p2');
});


/* ─────────────────────────────────────────
   19. BOTÓN REMATCH
      Reinicia todo el estado y la UI
      usando Object.assign para el estado
───────────────────────────────────────── */
rematchBtn.addEventListener('click', function () {
  /* Reiniciar estado completo con Object.assign */
  Object.assign(state, {
    hp:       { p1: MAX_HP, p2: MAX_HP },
    round:    1,
    phase:    'p1-choose',
    p1Choice: null,
    p2Choice: null,
    history:  [],
  });

  /* Reiniciar UI */
  updateHPBars();
  updatePips();
  roundNum.textContent    = '1';
  historyBox.innerHTML    = '';
  combatLog.textContent   = '';
  resultFlash.className   = '';
  resultFlash.textContent = '';
  setAvatar('p1', null, true);
  setAvatar('p2', null, true);
  setAnnounce('⚔ Elige tu arma ⚔');
  gameoverDiv.classList.remove('show');
  showChoicesFor('p1');
});


/* ─────────────────────────────────────────
   20. INICIALIZACIÓN
───────────────────────────────────────── */
updateHPBars();
updatePips();
showChoicesFor('p1');
