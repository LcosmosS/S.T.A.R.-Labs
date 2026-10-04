// BROKEN: gameOver stays true after restart → instant game over
class S extends Phaser.Scene { constructor(){ super('s'); this.gameOver = false; } }

// CORRECT: reset run state in init()
class S extends Phaser.Scene {
  constructor(){ super('s'); }
  init(){ this.gameOver = false; this.score = 0; }   // runs on every start
}
