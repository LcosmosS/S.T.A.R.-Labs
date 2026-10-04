import { createWorld, addEntity, addComponent, query } from 'bitecs';
const world = createWorld({ Position:{x:new Float32Array(1e4),y:new Float32Array(1e4)}, Velocity:{x:[],y:[]} });
const { Position, Velocity } = world.components;
const eid = addEntity(world); addComponent(world,eid,Position); addComponent(world,eid,Velocity);
const moving = query(world,[Position,Velocity]);
for (const e of moving){ Position.x[e] += Velocity.x[e]*dt; Position.y[e] += Velocity.y[e]*dt; }
