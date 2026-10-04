agent-browser batch --bail <<'JSON'   # find's label is case-sensitive: copy it from `snapshot -i`
[["open","http://127.0.0.1:8080/"],
 ["find","text","Start","click"],
 ["eval","if (!window.__controlsTest?.setKeys) throw Error('no §5b probe: add setKeys')"],
 ["eval","__controlsTest.setKeys(['KeyW'])"],
 ["wait","600"],
 ["eval","if (__controlsTest.getSpeed() <= 0.1) throw Error('W: no move')"],
 ["eval","(async () => { const t = __controlsTest, y0 = t.getYaw(); t.setKeys(['KeyW','KeyA']); await new Promise(r => setTimeout(r, 300)); t.setKeys(['KeyW']); const d = t.getYaw() - y0, w = Math.atan2(Math.sin(d), Math.cos(d)); if (w < -0.05) throw Error('A turns RIGHT — inverted, got ' + w.toFixed(2)); if (w <= 0.05) throw Error('A barely turned (' + w.toFixed(2) + ') — hold longer or check the sim is running'); return 'A ok' })()"],
 ["eval","__controlsTest.setKeys([])"],
 ["screenshot","/workspace/screenshots/controls.png"],
 ["close"]]
JSON
