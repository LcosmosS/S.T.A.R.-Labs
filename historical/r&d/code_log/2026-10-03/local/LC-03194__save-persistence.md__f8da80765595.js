const SAVE_VERSION = 3;
function migrate(save) {
  let s = { ...save };
  if (s.version === 1) { s.coins = s.gold ?? 0; delete s.gold; s.version = 2; }
  if (s.version === 2) { s.settings = { ...defaults.settings, ...s.settings }; s.version = 3; }
  return s; // now at SAVE_VERSION
}
function loadSave(raw) {
  let save = raw ?? structuredClone(defaultSave);
  if (save.version !== SAVE_VERSION) save = migrate(save);
  return save;
}
