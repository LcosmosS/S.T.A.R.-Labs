scale: {
  mode: Phaser.Scale.FIT,          // letterbox: keep aspect, fit inside parent
  autoCenter: Phaser.Scale.CENTER_BOTH,
  width: 800, height: 600,         // your fixed design resolution
  parent: 'game',
  // min/max clamp the FIT scaling:
  min: { width: 400, height: 300 }, max: { width: 1600, height: 1200 }
}
