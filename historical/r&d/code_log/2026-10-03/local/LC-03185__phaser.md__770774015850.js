class GameScene extends Phaser.Scene {
  constructor() { super('game'); }          // unique string key
  init(data) {}      // (1) reset per-run state HERE, receives data from start/launch
  preload() {}       // (2) queue asset loads only
  create(data) {}    // (3) build objects; assets from preload are now ready
  update(time, delta){} // (4) every tick while RUNNING (delta in ms)
}
