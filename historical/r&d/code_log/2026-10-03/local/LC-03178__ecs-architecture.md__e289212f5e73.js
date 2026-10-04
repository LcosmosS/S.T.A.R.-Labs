import { World } from 'miniplex';
const world = new World();
const player = world.add({ position:{x:0,y:0}, velocity:{x:100,y:0}, health:{cur:100,max:100} });
const moving = world.with('position','velocity');   // live archetype query
function movementSystem(dt){ for (const e of moving){ e.position.x += e.velocity.x*dt; e.position.y += e.velocity.y*dt; } }
world.remove(player);
