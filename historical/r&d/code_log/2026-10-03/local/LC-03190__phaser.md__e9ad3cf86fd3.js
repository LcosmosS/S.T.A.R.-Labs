// preload
this.load.image('tiles','tileset.png');
this.load.tilemapTiledJSON('map','level1.json');
// create
const map = this.make.tilemap({ key:'map' });
const tileset = map.addTilesetImage('tilesetNameInTiled','tiles');
const ground = map.createLayer('Ground', tileset, 0, 0);
ground.setCollisionByProperty({ collides:true });        // set per-tile in Tiled
this.physics.add.collider(player, ground);
// object layer for spawns/enemies:
const objs = map.getObjectLayer('Objects').objects;
