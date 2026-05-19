/* ═══════════════════════════════════════════
   1. PARTÍCULAS DE BRASA
═══════════════════════════════════════════ */
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

/* ═══════════════════════════════════════════
   2. DEFINICIÓN DE ARMAS
═══════════════════════════════════════════ */
const CHOICES = {
  piedra: { emoji: '🪨', name: 'Piedra', beats: 'tijera' },
  papel:  { emoji: '✋', name: 'Papel',  beats: 'piedra' },
  tijera: { emoji: '✂️', name: 'Tijera', beats: 'papel'  },
};

const COMBAT_LINES = {
  piedra_tijera: '🪨 Piedra aplasta Tijera',
  papel_piedra:  '✋ Papel envuelve Piedra',
  tijera_papel:  '✂️ Tijera corta Papel',
};

/* ═══════════════════════════════════════════
   3. ESTADO DEL JUEGO
═══════════════════════════════════════════ */
const MAX_HP = 4;
const state = {
  mode:     null, // 'pve' o 'pvp'
  hp:       { p1: MAX_HP, p2: MAX_HP },
  round:    1,
  phase:    'p1-choose',
  p1Choice: null,
  p2Choice: null,
  history:  [],
};

/* ═══════════════════════════════════════════
   4. REFERENCIAS AL DOM
═══════════════════════════════════════════ */
const $ = id => document.getElementById(id);

const startScreen = $('start-screen');
const btnPve      = $('btn-pve');
const btnPvp      = $('btn-pvp');
const nameP2      = $('name-p2');

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
const menuBtn     = $('menu-btn');
const resetBtn    = $('reset-btn');

/* ═══════════════════════════════════════════
   5. SELECCIÓN DE MODO Y ARRANQUE
═══════════════════════════════════════════ */
function startGame(mode) {
  state.mode = mode;
  startScreen.classList.remove('show');

  if (mode === 'pve') {
    nameP2.innerHTML = 'PC 🤖';
    nameP2.style.color = 'var(--gold)';
  } else {
    nameP2.innerHTML = 'Jugador 2 🩸';
    nameP2.style.color = 'var(--p2-color)';
  }

  resetGameUI();
}

btnPve.addEventListener('click', () => startGame('pve'));
btnPvp.addEventListener('click', () => startGame('pvp'));

/* ═══════════════════════════════════════════
   6. LÓGICA DE UI Y BARRAS DE VIDA
═══════════════════════════════════════════ */
function updateHPBars() {
  ['p1', 'p2'].forEach(p => {
    const pct = (state.hp[p] / MAX_HP) * 100;
    const bar = hpBar[p];
    bar.style.width = `${pct}%`;
    bar.className = 'hp-bar';
    if      (pct > 60) bar.classList.add('full');
    else if (pct > 30) bar.classList.add('medium');
    else               bar.classList.add('low');
  });
}

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
  av.classList.remove('reveal');
  void av.offsetWidth;
  av.classList.add('reveal');
}

function setAnnounce(text, color = '') {
  announceEl.textContent  = text;
  announceEl.style.color  = color || 'var(--gold)';
  announceEl.style.textShadow = color
    ? `0 0 10px ${color}, 0 0 25px ${color}66`
    : '0 0 10px var(--gold), 0 0 25px var(--fire-1)';
}

function shakeScreen() {
  document.body.classList.remove('shake');
  void document.body.offsetWidth;
  document.body.classList.add('shake');
  setTimeout(() => document.body.classList.remove('shake'), 550);
}

function triggerDamageFlash(player) {
  const wrap = hpWrap[player];
  wrap.classList.remove('damaged');
  void wrap.offsetWidth;
  wrap.classList.add('damaged');
  setTimeout(() => wrap.classList.remove('damaged'), 600);
}

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

function showResultFlash(text, cssClass) {
  resultFlash.textContent = text;
  resultFlash.className   = `show ${cssClass}`;
  setTimeout(() => {
    resultFlash.className   = '';
    resultFlash.textContent = '';
  }, 1800);
}

/* ═══════════════════════════════════════════
   7. IA DE LA MÁQUINA
═══════════════════════════════════════════ */
function getPcChoice() {
  const keys = Object.keys(CHOICES);
  return keys[Math.floor(Math.random() * keys.length)];
}

/* ═══════════════════════════════════════════
   8. RESOLVER COMBATE
═══════════════════════════════════════════ */
function resolveCombat() {
  state.phase = 'resolving';
  const p1c = state.p1Choice;
  const p2c = state.p2Choice;

  setAvatar('p1', p1c);
  setAvatar('p2', p2c);

  let winner = null;
  const p2Name = state.mode === 'pve' ? 'PC' : 'Jugador 2';

  if (p1c === p2c) {
    winner = 'draw';
    showResultFlash('⚔ EMPATE ⚔', 'draw');
    setAnnounce('¡Fuerzas iguales! ¡Nadie cae!', 'var(--gold)');
    combatLog.textContent = `${CHOICES[p1c].name} vs ${CHOICES[p2c].name} — Equilibrio perfecto`;
    shakeScreen();
  } else if (CHOICES[p1c].beats === p2c) {
    winner = 'p1';
    state.hp.p2 = Math.max(0, state.hp.p2 - 1);
    showResultFlash('⚡ Jugador 1 — VICTORIA', 'win-p1');
    setAnnounce(`¡Jugador 1 destruye a ${p2Name}!`, 'var(--p1-color)');
    combatLog.textContent = COMBAT_LINES[`${p1c}_${p2c}`] || `${CHOICES[p1c].name} vence`;
    shakeScreen();
    setTimeout(() => triggerDamageFlash('p2'), 150);
  } else {
    winner = 'p2';
    state.hp.p1 = Math.max(0, state.hp.p1 - 1);
    showResultFlash(`🩸 ${p2Name} — VICTORIA`, 'win-p2');
    setAnnounce(`¡${p2Name} aplasta a Jugador 1!`, state.mode === 'pve' ? 'var(--gold)' : 'var(--p2-color)');
    combatLog.textContent = COMBAT_LINES[`${p2c}_${p1c}`] || `${CHOICES[p2c].name} vence`;
    shakeScreen();
    setTimeout(() => triggerDamageFlash('p1'), 150);
  }

  if (winner !== 'draw') state.history.push(winner);
  addHistoryEntry(winner, p1c, p2c);
  updateHPBars();
  updatePips();

  setTimeout(() => {
    if (state.hp.p1 <= 0 || state.hp.p2 <= 0) {
      showGameOver();
    } else {
      nextRound();
    }
  }, 2000);
}

/* ═══════════════════════════════════════════
   9. FLUJO DEL JUEGO
═══════════════════════════════════════════ */
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

function showChoicesFor(player) {
  choicesRow.style.display = 'flex';
  waitingScr.classList.remove('show');

  if (player === 'p1') {
    turnLabel.textContent = '⚡ Jugador 1 — Elige tu destino ⚡';
    turnLabel.className   = 'player-turn-label p1-turn';
    setAnnounce('Jugador 1 — ¡Elige!', 'var(--p1-color)');
  } else {
    turnLabel.textContent = '🩸 Jugador 2 — Elige tu destino 🩸';
    turnLabel.className   = 'player-turn-label p2-turn';
    setAnnounce('Jugador 2 — ¡Elige!', 'var(--p2-color)');
  }
}

function showGameOver() {
  const winner = state.hp.p1 <= 0 ? 'p2' : 'p1';
  let winnerLbl = '';

  if (winner === 'p1') {
    winnerLbl = 'Jugador 1';
  } else {
    winnerLbl = state.mode === 'pve' ? 'PC' : 'Jugador 2';
  }

  gameoverWin.textContent = `${winnerLbl} GANA`;
  gameoverWin.className   = `${winner}-wins`;
  gameoverDiv.classList.add('show');
}

/* ═══════════════════════════════════════════
   10. LISTENERS & BOTONES RUNA
═══════════════════════════════════════════ */
document.querySelectorAll('.rune-btn').forEach(btn => {
  btn.addEventListener('click', function () {
    if (state.phase === 'resolving') return;

    const choice = this.dataset.choice;

    if (state.phase === 'p1-choose') {
      state.p1Choice = choice;
      setAvatar('p1', choice);
      choicesRow.style.display = 'none';

      if (state.mode === 'pve') {
        // MODO PC: La computadora elige inmediatamente
        state.phase = 'resolving';
        setAnnounce('La PC está decidiendo...', 'var(--fire-2)');
        combatLog.textContent = 'Las fuerzas del destino se alinean...';

        setTimeout(() => {
          state.p2Choice = getPcChoice();
          resolveCombat();
        }, 1200);

      } else {
        // MODO PvP: Oculta a P1 y espera a P2
        state.phase = 'waiting';
        waitingScr.classList.add('show');
        setTimeout(() => setAvatar('p1', null, true), 400);
        setAnnounce('Pasa el dispositivo a Jugador 2', 'var(--gold)');
        combatLog.textContent = 'Jugador 1 ha elegido. ¡Que el destino decida!';
      }

    } else if (state.phase === 'p2-choose') {
      // MODO PvP: Jugador 2 elige
      state.p2Choice = choice;
      setAvatar('p2', choice);
      setTimeout(() => resolveCombat(), 300);
    }
  });
});

/* ═══════════════════════════════════════════
   11. BOTÓN CONFIRMAR (PvP)
═══════════════════════════════════════════ */
confirmBtn.addEventListener('click', function () {
  state.phase = 'p2-choose';
  waitingScr.classList.remove('show');
  setAvatar('p1', null, true);
  setAvatar('p2', null, true);
  showChoicesFor('p2');
});

/* ═══════════════════════════════════════════
   12. RESET / REMATCH / MENÚ
═══════════════════════════════════════════ */
function resetGameUI() {
  Object.assign(state, {
    hp:       { p1: MAX_HP, p2: MAX_HP },
    round:    1,
    phase:    'p1-choose',
    p1Choice: null,
    p2Choice: null,
    history:  [],
  });
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
}

function volverAlMenu() {
  gameoverDiv.classList.remove('show');
  startScreen.classList.add('show');
  state.mode = null;
}

rematchBtn.addEventListener('click', resetGameUI);
menuBtn.addEventListener('click', volverAlMenu);
resetBtn.addEventListener('click', volverAlMenu);
