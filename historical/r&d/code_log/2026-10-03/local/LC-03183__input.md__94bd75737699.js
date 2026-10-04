const keys = new Set();
addEventListener('keydown', e => { keys.add(e.code); if (GAME_KEYS.has(e.code)) e.preventDefault(); });
addEventListener('keyup',   e => keys.delete(e.code));
addEventListener('blur',    () => keys.clear());
