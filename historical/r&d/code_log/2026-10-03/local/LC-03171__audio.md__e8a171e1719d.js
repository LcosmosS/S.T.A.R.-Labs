const master = audioCtx.createGain();
const musicBus = audioCtx.createGain();
const sfxBus   = audioCtx.createGain();
musicBus.connect(master); sfxBus.connect(master); master.connect(audioCtx.destination);
